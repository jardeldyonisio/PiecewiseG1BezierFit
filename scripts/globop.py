import numpy as np
from scipy.optimize import minimize
from objf2 import objf2

def globop(xi, Q, t, k, dpkpc):
    '''
    This function finds the global optimum for the curve.

    @param xi: Initial guess for the curve.
    @param Q: Knot points.
    @param t: Tangent angles.
    @param k: Indices of the points in the polyline that will be used to calculate the tangent angles.
    @param dpkpc: Position of the knot points passed globally.
    @return: The global optimum for the curve.
    '''

    options = {'disp': False, 'xtol': 0.01, 'ftol': 0.01}
    GOC = minimize(objf2, xi, args=(Q, t, k, dpkpc), method='Nelder-Mead', options=options)
    return GOC.x
