import numpy as np
from ktangdt import ktangdt
from bstdst import bstdst

def segop(k, Q, x0):
    '''
    This function finds the optimum distances for a segment.

    @param k: Knot vector.
    @param Q: Knot points.
    @param x0: Initial guess for the distances.

    @return SOC: The optimum distances for a segment.
    '''

    # Separates the vector x0 into its subcomponents.
    P, ang, dt = ktangdt(x0)

    # Call to the function which finds the optimum distances for a segment.
    bdt = bstdst(dt, Q, P, ang, k)
    print("bdt: ", bdt)

    bdt1 = [] # Empty list
    # PROBLEMA TA ACIMA DAQUI bdt VEM ERRADO

    for i in range(2):
        bdt1.extend(bdt[i, :])

    # Assemble the vector of parameters for the curve.
    SOC = np.concatenate([P[0, :], P[1, :], ang, bdt1])
    return SOC