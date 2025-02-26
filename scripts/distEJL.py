import numpy as np

# function dt = dist(P). This function computes the initial
# distances from the knot points to their adjacent control
# points for the initial guess curve. It returns the vector
# of distances to iguess.m. The function was written by
# E. J. Lane.
# https://gitlab.com/erehm/PiecewiseG1BezierFit/-/blob/master/distEJL.m


def distEJL(knots_positions, n_knots):
    """
    @brief Computes the initial distances from the knot points to their adjacent control points for the initial guess curve.
    
    @param P: numpy array of shape (2, n), where n is the number of knot points.
    @param n: integer, the number of knot points.
    @return dt: numpy array of shape (2*(n-1), ), containing the vector of distances.
    """

    # Calculates inter-knot x and y difference values.
    d1 = knots_positions[:, :-1] - knots_positions[:, 1:n_knots]
    
    # Computes the initial distances.
    d2 = np.sqrt(np.sum(d1 ** 2, axis=0)) / 3  
    
    # Assembles the vector of distances.
    dt = np.concatenate((d2, d2))  
    
    dt = np.reshape(dt, (2, n_knots - 1))
    dt = np.round(dt, 4)
    return dt
