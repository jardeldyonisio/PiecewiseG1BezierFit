import numpy as np
from unitv import unitv

def tang(Q, k):
    '''
    This function calculates the tangent angles of the control points.

    @param Q: Knot points.
    @param k: Indices of the points in the polyline that will be used to calculate the tangent angles.
    
    @return ang: The tangent angles of the control points.
    '''
    u = unitv(Q, k)
    ang = np.arctan2(u[1,:], u[0,:])
    ang = np.round(ang, 4)

    return ang
