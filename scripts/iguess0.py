import numpy as np
import matplotlib.pyplot as plt

from pltC import pltC
from defk import defk
from tang import tang
from ctpts import ctpts
from knots import knots
from distEJL import distEJL

# function [IG,k]=iguess(Q). This routine takes a set of data points, Q;
# picks out subset of the data point for knot points, P; computes the
# position of the knot points,k; computes the initial distances, dt, to
# place the interior control points, C, which are also computed; compute
# the angles, ang, of the unit tangent vectors at each knot point; and
# assembles the vector IG of paramaters P, ang, and dt, for the curve.
# The routine returns the "vector" of parmeters and plots the curve,
# its polygon, and the data points in Q. It was written by M. R. Holmes
# and revised by E. J. Lane.
# https://gitlab.com/erehm/PiecewiseG1BezierFit/-/blob/master/iguess0.m

def iguess0(data_points, n_knots):
    '''
    This function computes the initial guess curve parameters.

    @param set_points: Data points to be fitted.
    @param n_knots: Number of knot points.
    
    @return IG: Initial guess curve parameters.
    @return k: Indices of the points in the polyline that will be used to calculate
    the tangent angles.
    @return dpkpc: Position of the knot points passed globally.
    '''

    # TODO: Automatically set the number of knots.
    n_knots : int = 3
    default_knots_position : bool = True
    knots_index = None
    knots_sequence = None # [1, 4, 8, ..., n]

    # Set of points size
    _, data_point_size = data_points.shape

    if default_knots_position:
        # Calls the function to get the knots indices.
        knots_index = defk(data_point_size, n_knots)

    # TODO: If 'default_knots_position == False', 'knots_sequence' has to be defined.
    
    # Position of knot points passed globally.
    dpkpc = knots_index
    
    # Call the function to get the knots positions
    knots_positions = knots(data_points, knots_index)  
    
    # Call to compute the distance between successive knot points.
    dt = distEJL(knots_positions, knots_index, n_knots)  
    
    # Call to compute the angles for the unit tangent vectors.
    ang = tang(data_points, knots_index)  
    
    # Call to compute the control points for the curve.
    C = ctpts(knots_positions, ang, dt)  

    pltC(C, data_points, knots_positions)  # Call to plot the initial guess curve, its control polygon, and points in Q.
    plt.gcf()
    plt.title('Plot of Initial Guess curve')
    plt.show()

    # Assemble the composite vector of the initial guess curve parameters
    #IG = np.concatenate((P[0], P[1], ang, dt[0], dt[1]))
    nonzero_ang = np.nonzero(ang)[0]
    IG = np.concatenate((knots_positions[0, :], knots_positions[1, :], ang[nonzero_ang], dt[0, :], dt[1, :]), axis=0)
    # 3 termos de P, 3 termos de P, 3 termos de ang, 2 termos de dt
    return IG, knots_index, dpkpc

