import numpy as np

def knots(data_points, knots_index):
    '''
    This function defines the indices of the points in the polyline that will
    be used to calculate the tangent angles.

    @param Q: Data points to be fitted.
    @param k: Indices of the points in the polyline that will be used to calculate
    the tangent angles.
    @return P: The indices of the points in the polyline that will be used to
    calculate the tangent angles.
    '''
    knots_positions = np.empty((2, 0))
    knots_positions = np.hstack((knots_positions, data_points[:, knots_index - 1]))
    return knots_positions
