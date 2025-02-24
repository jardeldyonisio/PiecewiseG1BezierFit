import math
import numpy as np

# TODO: Apontar P e dt direto para esse arquivo, não precisar calcular novamente aqui 

def ktangdt(x):
    '''
    This function separates the vector x into the knot points, the angles of the 
    unit tangent vectors, and the distances between the knot points.

    @return P: Knot points.
    @return ang: Angles of the unit tangent vectors.
    @return dt: Distances between the knot points.
    '''
    m = len(x)
    n = math.ceil(m/5)

    P = np.zeros((2, n))
    P[0, :] = x[:n]
    P[1, :] = x[n:2*n]

    ang = x[2*n:3*n]

    dt = np.zeros((2, n-1))
    dt[0, :] = x[3*n:4*n-1]
    dt[1, :] = x[4*n-1:m]
    ang = np.round(ang, 4)
    dt = np.round(dt, 4)
    return P, ang, dt
