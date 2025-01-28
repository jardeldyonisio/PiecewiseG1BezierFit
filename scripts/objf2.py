import numpy as np
import math
from ktangdt import ktangdt
from ctpts import ctpts
from newk import newk
from sod import sod

def objf2(x, Q, t, k, dpkpc):
    # Loop to change dpkpc if a knot was inserted or removed.
    if t == 1:
        dpkpc = k
        t = n
    
    if t == 0:
        r, s = Q.shape
        P, ang, dt = ktangdt(x)  # Call to separate x into its subcomponents.
        C = ctpts(P, ang, dt)    # Call to compute control points.
        dpkpc = newk(Q, P, dpkpc)       # Call function computes the new dividing point positions.
        m = len(x)
        n = round(m / 5)

        fp = P[:, 0] - Q[:, 0]    # Compute the distance squared from the first data point to the first knot point.
        lp = P[:, n - 1] - Q[:, s - 1]    # Compute the distance squared from the last data point to the last knot point.
        
        # Calls the function that computes the sums of the square
        # of the distances from the data points to the nearest point
        # on the cubic segment.
        se = sod(C, Q, dpkpc) + np.dot(fp, fp) + np.dot(lp, lp)
        
        return se
