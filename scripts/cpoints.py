from ktangdt import ktangdt
from ctpts import ctpts

def cpoints(x):
    '''
    The function cpoints computes the control points of a curve defined by the
    knot points, the angles of the unit tangent vectors, and the distances between
    the knot points.

    @param x: numpy array of shape (2*(n+1) + 2*(n-1), ), where n is the number of knot points.
    @return C: numpy array of shape (2, 3*n), containing the control points of the curve.
    '''
    P, ang, dt = ktangdt(x)  # Separate vector x
    C = ctpts(P, ang, dt)  # Compute the control points
    return C
