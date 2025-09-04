import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

from poplt import poplt
from segop import segop
from knots import knots
from globop import globop
from cpoints import cpoints
from iguess0 import iguess0
from DrawBezierCurve import drawBezierCurve

def getControlPoints():
    '''
    @brief Retrieve control points from the Bezier curve fitting process.
    '''
    pass

def getKnots():
    '''
    @brief Retrieve knot points from the Bezier curve fitting process.
    '''
    pass

def getBezierPoints():
    '''
    @brief Retrieve Bezier points from the Bezier curve fitting process.
    '''
    pass

def getError():
    '''
    @brief Retrieve error metrics from the Bezier curve fitting process.
    '''
    pass

def adaptiveKnotsPlacement(Q, 
                           initial_knots: int = 3, 
                           max_knots: int = 20, 
                           error_threshold: float = 0.2, 
                           max_iterations: int = 10):
    '''
    @brief Adaptive knot placement algorithm that iteratively adds knots where error is highest.
    
    @param Q: trajectory points (Nx2)
    @param initial_knots: starting number of knots
    @param max_knots: maximum number of knots allowed
    @param error_threshold: target error threshold to stop iteration
    @param max_iterations: maximum number of iterations to prevent infinite loops
    
    @return best_k: optimal knot indices (1-based for MATLAB compatibility)
    @return error_history: history of errors for analysis
    @return iteration_info: detailed information about each iteration
    '''
    
    Qt = Q.T  # Transpose for algorithm compatibility
    error_history = []
    iteration_info = []
    
    # Start with uniform distribution
    current_knots = np.linspace(1, len(Q), initial_knots).astype(int)
    
    for iteration in range(max_iterations):
        try:
            # Run full Bezier fitting pipeline
            IG, k_out, dpkpc = iguess0(Qt, len(current_knots), current_knots)
            SOC = segop(current_knots, Qt, IG)
            GOC = globop(SOC, Qt, 0, current_knots, dpkpc)
            
            # Calculate error for each segment
            segment_errors = calculateSegmentErrors(GOC, Qt, current_knots, dpkpc)
            total_error = np.sum(segment_errors)
            
            print(f"Total error: {total_error:.6f}")
            print(f"Segment errors: {segment_errors}")
            
            error_history.append(total_error)
            iteration_info.append({
                'iteration': iteration + 1,
                'knots': current_knots.copy(),
                'total_error': total_error,
                'segment_errors': segment_errors.copy(),
                'GOC': GOC.copy()
            })
            
            # Check convergence
            if total_error < error_threshold:
                print(f"✅ Converged! Error {total_error:.6f} < threshold {error_threshold}")
                break
                
            if len(current_knots) >= max_knots:
                print(f"⚠️  Reached maximum knots ({max_knots})")
                break
            
            # Find segment with highest error and add knot in middle
            worst_segment = np.argmax(segment_errors)
            
            # Calculate position for new knot (middle of worst segment)
            if worst_segment < len(current_knots) - 1:
                start_idx = current_knots[worst_segment] - 1  # Convert to 0-based
                end_idx = current_knots[worst_segment + 1] - 1
                new_knot_idx = (start_idx + end_idx) // 2 + 1  # Convert back to 1-based
                
                # Insert new knot
                insert_pos = worst_segment + 1
                current_knots = np.insert(current_knots, insert_pos, new_knot_idx)
                
                print(f"Added knot at index {new_knot_idx} (segment {worst_segment} had error {segment_errors[worst_segment]:.6f})")
            else:
                print("Cannot add more knots - reached trajectory end")
                break
                
        except Exception as e:
            print(f"❌ Error in iteration {iteration + 1}: {str(e)}")
            if iteration == 0:
                # If first iteration fails, fall back to simple uniform distribution
                current_knots = np.linspace(1, len(Q), min(8, max_knots)).astype(int)
                print(f"Falling back to uniform distribution: {current_knots}")
            break
    
    print(f"\n=== ADAPTIVE PLACEMENT COMPLETE ===")
    print(f"Final knots: {current_knots}")
    print(f"Final error: {error_history[-1] if error_history else 'N/A'}")
    print(f"Iterations completed: {len(error_history)}")
    
    return current_knots, error_history, iteration_info

def calculateSegmentErrors(GOC, 
                           Q, 
                           k, 
                           dpkpc):
    '''
    @brief Calculate the error for each Bezier segment.

    @param GOC: Global control points
    @param Q: Data points
    @param k: Knot vector
    @param dpkpc: Derivative control points
    '''
    try:
        # Get control points
        from cpoints import cpoints
        C = cpoints(GOC)
        
        # Calculate error for each segment
        segment_errors = []
        
        for i in range(len(k) - 1):
            # Get data points for this segment
            start_idx = k[i] - 1  # Convert to 0-based
            end_idx = k[i + 1] - 1
            
            # Get control points for this segment (4 points per cubic Bezier)
            ctrl_start = i * 3
            if ctrl_start + 3 < C.shape[1]:
                ctrl_points = C[:, ctrl_start:ctrl_start + 4]
                segment_data = Q[:, start_idx:end_idx + 1]
                
                # Calculate sum of distances for this segment
                if segment_data.shape[1] > 0:
                    error = calculateSegmentDistanceError(ctrl_points, segment_data)
                    segment_errors.append(error)
                else:
                    segment_errors.append(0.0)
            else:
                segment_errors.append(0.0)
        
        return np.array(segment_errors)
        
    except Exception as e:
        print(f"Error calculating segment errors: {str(e)}")
        return np.array([1.0] * (len(k) - 1))  # Return uniform error as fallback

def calculateSegmentDistanceError(ctrl_points, data_points):
    '''
    @brief Calculate the sum of minimum distances from data points to Bezier curve segment.

    @param ctrl_points: Control points of the Bezier curve segment.
    @param data_points: Data points to measure distances from.
    '''
    try:
        # Generate points on the Bezier curve
        t_vals = np.linspace(0, 1, 50)
        bezier_points = []
        
        for t in t_vals:
            # Cubic Bezier formula: B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
            b = ((1-t)**3 * ctrl_points[:, 0:1] + 
                 3*(1-t)**2*t * ctrl_points[:, 1:2] + 
                 3*(1-t)*t**2 * ctrl_points[:, 2:3] + 
                 t**3 * ctrl_points[:, 3:4])
            bezier_points.append(b.flatten())
        
        bezier_points = np.array(bezier_points)  # Shape: (50, 2)
        
        # Calculate minimum distances from each data point to Bezier curve
        distances = []
        for i in range(data_points.shape[1]):
            point = data_points[:, i].reshape(1, -1)  # Shape: (1, 2)
            dists = cdist(point, bezier_points)
            min_dist = np.min(dists)
            distances.append(min_dist)
        
        return np.sum(distances)
        
    except Exception as e:
        print(f"Error in distance calculation: {str(e)}")
        return 1.0  # Return default error

def bezierFit(plot: bool = False):
    '''
    @brief Demonstrate Bezier curve fitting with adaptive knot placement.

    @param plot: Flag to indicate whether to plot the results.
    '''
    # Demonstrate Bezier curve fit with adaptive knot placement
    demo = 1
    k = None

    if demo == 1:
        # Create a more complex trajectory with 200 points for robotics testing
        t = np.linspace(0, 4*np.pi, 200)
        
        # Create a spiral-like trajectory with some noise (simulating real robot data)
        np.random.seed(42)  # For reproducible results
        noise_x = np.random.normal(0, 0.02, 200)
        noise_y = np.random.normal(0, 0.02, 200)

        x = t * np.cos(t) * 0.3 + noise_x
        y = t * np.sin(t) * 0.3 + noise_y
        
        Q = np.column_stack([x, y])
        
        # Adaptive knot placement - automatically determines optimal number and positions
        k_adaptive, error_history, iteration_info = adaptiveKnotsPlacement(
            Q, 
            initial_knots=3, 
            max_knots=15, 
            error_threshold=0.01,
            max_iterations=8
        )
        
        k = k_adaptive  # Use adaptively determined knots
        n = len(k)      # Number of knots determined adaptively
        
    # Now run the final optimization with the adaptively chosen knots
    Qt = Q.T
    IG, k_out, dpkpc = iguess0(Qt, n, k)

    # Improve the fit: Segmentally Optimum Only Curve (SOO)
    SOC = segop(k, Qt, IG)

    # Improve it again: Segmentally then Globally Optimized Curve (SGO)
    GOC = globop(SOC, Qt, 0, k, dpkpc)

    # plot SGO curve using internal routine
    plt.figure(figsize=(10, 8))
    poplt(GOC, Qt)
    plt.title('Python: Plot of SGO curve')

    # Get the Bézier control points of the curve fit
    Cnew = cpoints(GOC).T  # Cnew will be Nx2 for plotting
    P = knots(Qt, k).T     # P will be Nx2 for plotting (transpose from 2xN)

    # Plot fitted, segment by segment
    plt.figure(figsize=(12, 8))
    for i in range(0, len(Cnew)-2, 3):
        if i+3 < len(Cnew):
            drawBezierCurve(Cnew[i:i+4])   # Fitted cubic Bézier segment

    plt.plot(Cnew[:,0], Cnew[:,1], 'o-', label='New control points', linewidth=2, markersize=6)
    plt.plot(Q[:,0], Q[:,1], 'k.', label='Original data', markersize=3)
    plt.plot(P[:,0], P[:,1], 'kx', markersize=10, markeredgewidth=3, label=f'Original guess n = {n} knots')

    plt.legend()
    plt.title('Python: Detailed Bézier Curve Fit (Adaptive Knots)')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    # Plot adaptive algorithm analysis
    plt.figure(figsize=(15, 10))
    
    # Top subplot: Error convergence
    plt.subplot(2, 3, 1)
    if len(error_history) > 0:
        plt.plot(range(1, len(error_history) + 1), error_history, 'bo-', linewidth=2, markersize=8)
        plt.xlabel('Iteration')
        plt.ylabel('Total Error')
        plt.title('Adaptive Algorithm Convergence')
        plt.grid(True, alpha=0.3)
        
        # Show error threshold
        if len(error_history) > 0:
            plt.axhline(y=0.01, color='r', linestyle='--', alpha=0.7, label='Target threshold')
            plt.legend()
    
    # Middle subplot: Number of knots evolution
    plt.subplot(2, 3, 2)
    if len(iteration_info) > 0:
        knot_counts = [len(info['knots']) for info in iteration_info]
        plt.plot(range(1, len(knot_counts) + 1), knot_counts, 'go-', linewidth=2, markersize=8)
        plt.xlabel('Iteration')
        plt.ylabel('Number of Knots')
        plt.title('Knot Count Evolution')
        plt.grid(True, alpha=0.3)
    
    # Right subplot: Final trajectory with knot evolution
    plt.subplot(2, 3, 3)
    plt.plot(Q[:,0], Q[:,1], 'k-', alpha=0.5, linewidth=1, label='Original trajectory')
    
    # Show knot evolution with different colors
    colors = plt.cm.viridis(np.linspace(0, 1, len(iteration_info)))
    for i, info in enumerate(iteration_info):
        knot_positions = info['knots'] - 1  # Convert to 0-based
        plt.scatter(Q[knot_positions, 0], Q[knot_positions, 1], 
                   c=[colors[i]], s=50, alpha=0.7, 
                   label=f'Iter {i+1} (n={len(info["knots"])})')
    
    plt.title('Knot Placement Evolution')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    # Bottom subplots: Segment error analysis
    plt.subplot(2, 3, 4)
    if len(iteration_info) > 0:
        final_info = iteration_info[-1]
        segment_errors = final_info['segment_errors']
        segments = range(1, len(segment_errors) + 1)
        bars = plt.bar(segments, segment_errors, alpha=0.7, color='orange')
        plt.xlabel('Segment Number')
        plt.ylabel('Segment Error')
        plt.title('Final Segment Errors')
        plt.grid(True, alpha=0.3)
        
        # Highlight the worst segment
        if len(segment_errors) > 0:
            worst_idx = np.argmax(segment_errors)
            bars[worst_idx].set_color('red')
    
    # Bottom middle: Comparison of iterations
    plt.subplot(2, 3, 5)
    if len(iteration_info) >= 2:
        first_iter = iteration_info[0]
        last_iter = iteration_info[-1]
        
        categories = ['Initial', 'Final']
        errors = [first_iter['total_error'], last_iter['total_error']]
        knot_counts = [len(first_iter['knots']), len(last_iter['knots'])]
        
        x = np.arange(len(categories))
        width = 0.35
        
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        
        bars1 = ax1.bar(x - width/2, errors, width, alpha=0.7, color='blue', label='Error')
        bars2 = ax2.bar(x + width/2, knot_counts, width, alpha=0.7, color='green', label='Knots')
        
        ax1.set_xlabel('Algorithm Stage')
        ax1.set_ylabel('Total Error', color='blue')
        ax2.set_ylabel('Number of Knots', color='green')
        ax1.set_title('Initial vs Final Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        
        # Add value labels on bars
        for bar, value in zip(bars1, errors):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(errors)*0.02,
                    f'{value:.4f}', ha='center', va='bottom')
        for bar, value in zip(bars2, knot_counts):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(knot_counts)*0.02,
                    f'{value}', ha='center', va='bottom')
    
    # Bottom right: Algorithm summary
    plt.subplot(2, 3, 6)
    plt.axis('off')
    
    if iteration_info:
        improvement = ((iteration_info[0]['total_error'] - iteration_info[-1]['total_error']) / iteration_info[0]['total_error'] * 100)
        status = '✅ Converged' if len(error_history) > 0 and error_history[-1] < 0.01 else '⚠️ Max iterations reached'
        
        summary_text = f'''
ADAPTIVE ALGORITHM SUMMARY

Initial knots: {iteration_info[0]['knots']}
Final knots: {iteration_info[-1]['knots']}

Initial error: {iteration_info[0]['total_error']:.6f}
Final error: {iteration_info[-1]['total_error']:.6f}

Iterations: {len(iteration_info)}
Improvement: {improvement:.1f}%

Status: {status}
        '''
    else:
        summary_text = "No iteration data available"
    
    plt.text(0.05, 0.95, summary_text, transform=plt.gca().transAxes, 
             fontsize=10, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    bezierFit()