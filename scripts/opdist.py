import numpy as np

from ctpts import ctpts
from NearestPoint import NearestPoint

# TODO: In the else condition, the subtraction is not working properly because the round 
# difference between the original code.

def opdist(id, Q, P, ang):
    """
    This function is the objective function to be minimized during segment optimization.
    It receives subcomponents from a curve's composite vector, a segment at a time.
    It returns the sum error for a segment.

    @param id: Initial guess for the distances.
    @param Q: Knot points.
    @param P: Control points.
    @param ang: Angles between the control points.
    
    @return se2: The sum of the square of the distances from the data points to the nearest point
    on the cubic segment.
    """
    n = len(Q[0])
    id = np.reshape(id, (-1, 1))

    # Call to compute the segments control points.
    # ctpts has round issues, so we need to fix it.
    C = ctpts(P, ang, id) 
    se2 = 0
    cont = 0

    # print("id: ", id)
    # print("Q: ", Q)
    # print("P: ", P)
    # print("ang: ", ang)

    # ERRO DAQUI PRA BAIXO

    # Loop to find distance error in a segment.
    for j in range(n):
        npoints = NearestPoint(C.T, np.transpose((Q[:,j])))
        if (j == 0) and np.all(npoints == np.transpose(tuple(C[:, 0]))):
            d = np.zeros(2)
        elif (j == n - 1) and np.all(npoints == np.transpose(tuple(C[:, 3]))):
            d = np.zeros(2)
        else:
            # TODO: Here in the equation below, the subtraction is not working
            # properly because the round difference between the original code.
            d = np.transpose(((Q[:,j])) - npoints)
            print("np.transpose(((Q[:,j]))", np.transpose(((Q[:,j]))))
            print("npoints", npoints)
            print("d: ", d)
        se2 = se2 + np.dot(d, d.T)
        cont += 1
        # print("se2: ", se2)
        # print("d: ", d)
    return se2