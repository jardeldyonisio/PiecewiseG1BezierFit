import numpy as np
import matplotlib.pyplot as plt

from pltC import pltC
from defk import defk
from tang import tang
from ctpts import ctpts
from knots import knots
from distEJL import distEJL

def iguess0(Q, n, k):
    r, m = Q.shape

    print("=== IGUESS0 DEBUG ===")
    print(f"Q shape: {r}x{m}")
    print(f"n: {n}")

    # Q = datapoints (2xm)
    # n = The number of knotpoints
    # k = default knot positions (indices 1...m)
    if k is None:
        k = defk(m, n)  # Calls for default knot position.
        
    print("k after defk:", k)
    
    dpkpc = k  # Position of knot points passed globally.
    P = knots(Q, k)  # call to compute the knotpoints.
    
    print(f"P shape: {P.shape[0]}x{P.shape[1]}")
    print("P:", P)
    
    dt = distEJL(P, n)  # Call to compute the distance between successive knot points.
    
    print(f"dt shape: {dt.shape[0]}x{dt.shape[1]}")
    print("dt:", dt)
    
    ang = tang(Q, k)  # Call to compute the angles for the unit tangent vectors.
    
    print(f"ang length: {len(ang)}")
    print("ang:", ang)
    
    C = ctpts(P, ang, dt)  # Call to compute the control points for the curve.

    print(f"C shape: {C.shape[0]}x{C.shape[1]}")
    print("C first 5 points:")
    if C.shape[0] >= 5:
        print(C[:5,:])
    else:
        print(C)

    # Skip plotting for debug
    # pltC(C, Q, P)  # Call to plot the initial guess curve, its control polygon, and points in Q.
    # plt.gcf()
    # plt.title('Plot of Initial Guess curve')
    # plt.show()

    # Assemble the composite vector of the initial guess curve parameters
    #IG = np.concatenate((P[0], P[1], ang, dt[0], dt[1]))
    nonzero_ang = np.nonzero(ang)[0]
    IG = np.concatenate((P[0, :], P[1, :], ang[nonzero_ang], dt[0, :], dt[1, :]), axis=0)
    # 3 termos de P, 3 termos de P, 3 termos de ang, 2 termos de dt
    
    print(f"IG length: {len(IG)}")
    print("IG:", IG)
    print("=== IGUESS0 DEBUG END ===")
    
    return IG, k, dpkpc

