import numpy as np
import matplotlib.pyplot as plt

from poplt import poplt
from segop import segop
from knots import knots
from globop import globop
from cpoints import cpoints
from iguess0 import iguess0
from DrawBezierCurve import drawBezierCurve
from cubicBezierToPolyline import cubicBezierToPolyline

def BezierFitDemo_clean():
    # Demonstrate Bezier curve fit
    demo = 1
    k = None

    if demo == 1:
        C = np.array([[0, 0],
                      [1, 2],
                      [3, 3],
                      [4, 2]])
        Q = cubicBezierToPolyline(C, 65)
        n = 3  # Starting number of knot points
        
    print(f"Demo: {demo}, n: {n}")
    print(f"Q shape: {Q.shape[0]}x{Q.shape[1]}")

    # Now try to do a piecewise cubic Bézier fit to Q starting with n knot points
    Qt = Q.T
    IG, k, dpkpc = iguess0(Qt, n, k)
    print(f"Initial guess completed, k: {k}")

    # Improve the fit: Segmentally Optimum Only Curve (SOO)
    SOC = segop(k, Qt, IG)
    print(f"Segmental optimization completed")

    # Improve it again: Segmentally then Globally Optimized Curve (SGO)
    GOC = globop(SOC, Qt, 0, k, dpkpc)
    print(f"Global optimization completed")

    # plot SGO curve using internal routine
    plt.figure(figsize=(10, 8))
    poplt(GOC, Qt)
    plt.title('Python: Plot of SGO curve')
    plt.savefig('/home/jardeldyonisio/PiecewiseG1BezierFit/python_sgo_curve_clean.png', dpi=300, bbox_inches='tight')
    print("Saved Python SGO curve plot")

    # Get the Bézier control points of the curve fit
    Cnew = cpoints(GOC).T  # Cnew will be Nx2 for plotting
    P = knots(Qt, k).T     # P will be Nx2 for plotting (transpose from 2xN)

    # Plot fitted, segment by segment
    plt.figure(figsize=(12, 8))
    for i in range(0, len(Cnew)-2, 3):
        if i+3 < len(Cnew):
            drawBezierCurve(Cnew[i:i+4])   # Fitted cubic Bézier segment
    
    ho = plt.plot(Q[:,0], Q[:,1], 'k.', label='Original data', markersize=3)
    hn = plt.plot(P[:,0], P[:,1], 'kx', markersize=10, markeredgewidth=3, label=f'Original guess n = {n} knots')
    hc = plt.plot(Cnew[:,0], Cnew[:,1], 'o-', label='New control points', linewidth=2, markersize=6)
    
    plt.legend(['Original data', f'Original guess n = {n} knots', 'New control points'])
    plt.title('Python: Detailed Bézier Curve Fit')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.savefig('/home/jardeldyonisio/PiecewiseG1BezierFit/python_detailed_fit_clean.png', dpi=300, bbox_inches='tight')
    print("Saved Python detailed fit plot")

if __name__ == '__main__':
    BezierFitDemo_clean()
