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

def BezierFitDemo():
    '''
    Main function to demonstrate the Bezier curve fitting.
    Replace data_points with your data, if you do that, you will need to
    adjust n = number of knots
    '''
    # Set demo to 1, 2, or 3 to choose a demo
    demo = 1
    
    if demo == 1:
        # The 'ctrl_points' variable is the control points of a cubic Bezier curve
        ctrl_points = np.array([[0, 0],
                      [1, 2],
                      [ 3, 3],
                      [ 4, 2]])
        
        # The 'data_points' variable is the set of points that will be used to fit the curve
        # n = 65 represents the number of points in the polyline
        data_points = cubicBezierToPolyline(ctrl_points, 65)
        
        # Starting number of knot points
        n_knots = 3 
    elif demo == 2:
        # Or, try a Lissajous figure:
        theta = np.arange(0, 2*np.pi, 0.05)
        x = np.sin(2*theta)
        y = np.cos(theta)
        data_points = np.column_stack((x, y))
        
        # Starting number of knot points
        n_knots = 3  
    elif demo == 3:
        # Or two cycles of a sine wave
        theta = np.arange(0, 4*np.pi, 0.05)
        x = theta
        y = np.cos(theta)
        data_points = np.column_stack((x, y))
        
        # Starting number of knot points
        n_knots = 5  

    # Now try to do a piecewise cubic Bézier fit to Q starting with n knot points
    # This computes the globally optimized only (GOO) curve.
    # (The plotting of the IG curve in iguess0.m can be commented out.)
    data_points_transpose = data_points.T
    IG, k, dpkpc = iguess0(data_points_transpose, n_knots)
    # Improve the fit: Segmentally Optimum Only Curve (SOO)
    SOC = segop(k, data_points_transpose, IG)

    # Improve it again: Segmentally then Globally Optimized Curve (SGO)
    GOC = globop(SOC, data_points_transpose, 0, k, dpkpc)

    # plot SGO curve using internal routine
    plt.figure()
    poplt(GOC, data_points_transpose)
    plt.title('Plot of SGO curve')

    # This section of code simply repeats the plot above (poplt) in a
    # manner that makes it easier to see the piecewise cubic Bézier sections

    # Get the Bézier control points of the curve fit
    Cnew = cpoints(GOC).T
    P = knots(data_points_transpose, k)

    # Plot fitted, segment by segment using Geom2D toolkit
    plt.figure()
    for i in range(0, len(Cnew)-2, 3):
        drawBezierCurve(Cnew[i:i+4])   # Fitted cubic Bézier segment
    hc = plt.plot(Cnew[:,0], Cnew[:,1], 'o-', label='New control points')
    ho = plt.plot(data_points[:,0], data_points[:,1], 'k.', label='Original data')
    hn = plt.plot(P[:,0], P[:,1], 'kx', markersize=10, label='Original knot points')
    plt.legend([ho[0], hn[0], hc[0]], ['Original data',
                                        f'Original guess n = {n} knots',
                                        'New control points'])
    plt.gca().set_aspect('equal')
    plt.gca().set_facecolor('white')
    plt.show()

if __name__ == '__main__':
    BezierFitDemo()