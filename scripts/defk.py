import numpy as np

# Computes default knot positions for iguess.m based on a
# formula to equally disperse the knots throughout the data.
# https://gitlab.com/erehm/PiecewiseG1BezierFit/-/blob/master/defk.m

def defk(data_point_size, n_knots):
    '''
    This function defines the indices of the knots points.

    @param m: Number of positions to be fitted.
    @param n: Number of knots points.

    @return k: The indices of the knots points.
    '''

    k = np.round(((data_point_size-1)/(n_knots-1)) * np.arange(n_knots)) + np.ones(n_knots).astype(int)
    k = k.astype(int)
    return k