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
    # Demonstrate two different Bezier curve fits
    # Array Q is the set of data points to which we want to fit
    # a piecewise G1 continuous cubic Bezier curve
    # (Replace Q with your data.  You will need to adjust n = number of knots)

    demo = 1
    k = None

    if demo == 1:

        C = np.array([[0, 0],
                      [1, 2],
                      [ 3, 3],
                      [ 4, 2]])
        Q = cubicBezierToPolyline(C, 65)
        
        n = 3 # Starting number of kno,t points
    elif demo == 2:
        # Or, try a Lissajous figure:,
        theta = np.arange(0, 2*np.pi, 0.05)
        x = np.sin(2*theta)
        y = np.cos(theta)
        Q = np.column_stack((x, y))
        n = 3  # Starting number of knot points
    elif demo == 3:
        # Or two cycles of a sine wave
        theta = np.arange(0, 4*np.pi, 0.05)
        x = theta
        y = np.cos(theta)
        Q = np.column_stack((x, y))
        n = 5  # Starting number of knot points

    # Now try to do a piecewise cubic Bézier fit to Q starting with n knot points
    # This computes the globally optimized only (GOO) curve.
    # (The plotting of the IG curve in iguess0.m can be commented out.)
    Qt = Q.T
    IG, k, dpkpc = iguess0(Qt, n, k)
    # Improve the fit: Segmentally Optimum Only Curve (SOO)
    SOC = segop(k, Qt, IG)

    # Improve it again: Segmentally then Globally Optimized Curve (SGO)
    GOC = globop(SOC, Qt, 0, k, dpkpc)

    # plot SGO curve using internal routine
    plt.figure()
    poplt(GOC, Qt)
    plt.title('Plot of SGO curve')

    # This section of code simply repeats the plot above (poplt) in a
    # manner that makes it easier to see the piecewise cubic Bézier sections

    # Get the Bézier control points of the curve fit
    Cnew = cpoints(GOC).T
    P = knots(Qt, k)

    # Plot fitted, segment by segment using Geom2D toolkit
    plt.figure()
    for i in range(0, len(Cnew)-2, 3):
        drawBezierCurve(Cnew[i:i+4])   # Fitted cubic Bézier segment
    hc = plt.plot(Cnew[:,0], Cnew[:,1], 'o-', label='New control points')
    ho = plt.plot(Q[:,0], Q[:,1], 'k.', label='Original data')
    hn = plt.plot(P[:,0], P[:,1], 'kx', markersize=10, label='Original knot points')
    plt.legend([ho[0], hn[0], hc[0]], ['Original data',
                                        f'Original guess n = {n} knots',
                                        'New control points'])
    plt.gca().set_aspect('equal')
    plt.gca().set_facecolor('white')
    plt.show()

if __name__ == '__main__':
    BezierFitDemo()