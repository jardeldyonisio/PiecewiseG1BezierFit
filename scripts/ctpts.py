import numpy as np

def ctpts(P, ang, dt):
    '''
    This function computes the control points of a segment of a curve.

    @param P: Knot points.
    @param ang: Angles of the unit tangent vectors.
    @param dt: Distances between the knot points.
    @return: The control points of the segment.

    Obs: There are small round differences between the original code result 
    and this one, the last decimal place is sometimes different.
    '''

    # print("P: ", P)
    # print("ang: ", ang)
    # print("dt: ", dt)

    P = np.atleast_2d(P)  # Garantir que P seja uma matriz bidimensional
    n = len(P[0])
    T = np.empty((2,0))

    for k in range(1, n-1): # n = 2, (1, 1)
        # Converts the interior angles into their x and y components.
        u = np.array([[np.cos(ang[k])], [np.sin(ang[k])]])

        #Assembles the vector knot points with their
        #adjacent interior control points.
        T = np.concatenate((T, P[:, [k]] - u * dt[1, k - 1], P[:, [k]], 
                            P[:, [k]] + u * dt[0, k]), axis = 1)

    u1 = np.array([[np.cos(ang[0])], [np.sin(ang[0])]])
    un = np.array([[np.cos(ang[n-1])], [np.sin(ang[n-1])]])  # angles into their x and y components.

    # Assembles the vector of all control points
    
    C = np.hstack([P[:,[0]], P[:, [0]] + u1 * dt[0,0], T, P[:,[n-1]] - un * dt[1,n-2], P[:,[n-1]]])
    C = np.round(C, 4)
    return C
