import numpy as np
import ctpts
import pltC
import tang
import distEJL
import defk
import knots
import matplotlib.pyplot as plt

def iguess(Q):
    '''
    This function computes the initial guess curve parameters.

    @param Q: Data points to be fitted.
    @return IG: Initial guess curve parameters.
    @return k: Indices of the points in the polyline that will be used to calculate
    the tangent angles.
    @return dpkpc: Position of the knot points passed globally.
    '''
    r, m = Q.shape

    # Prompt user to input the number of knot points and the type of knot position
    n = int(input())
    h = int(input())

    if h == 1:
        k = defk(m, n)  # Calls for default knot position.
    elif h == 2:
        print('Input initial knot sequence as follows "[1 4 8 ... n]".')
        k = np.array(input())
    else:
        print('Error! Start over and choose "1" or "2".')
        return

    dpkpc = k  # Position of knot points passed globally.
    P = knots(Q, k)  # Call to compute the knot points.
    dt = distEJL(P)  # Call to compute the distance between successive knot points.
    ang = tang(Q, k)  # Call to compute the angles for the unit tangent vectors.
    C = ctpts(P, ang, dt)  # Call to compute the control points for the curve.

    # Call to plot the initial guess curve, its control polygon, and points in Q.
    pltC(C, Q, P)

    # Assemble the composite vector of the initial guess curve parameters
    IG = np.concatenate((P[0], P[1], ang, dt[0], dt[1]))

    return IG, k, dpkpc