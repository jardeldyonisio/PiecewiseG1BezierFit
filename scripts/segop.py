import numpy as np
from ktangdt import ktangdt
from bstdst import bstdst

def segop(k, Q, x0):
    print("=== SEGOP DEBUG ===")
    print("k:", k)
    print(f"Q shape: {Q.shape[0]}x{Q.shape[1]}")
    print(f"x0 length: {len(x0)}")
    print("x0:", x0)
    
    # Separates the vector x0 into its subcomponents.
    P, ang, dt = ktangdt(x0)

    print("After ktangdt:")
    print(f"P shape: {P.shape[0]}x{P.shape[1]}")
    print("P:", P)
    print(f"ang length: {len(ang)}")
    print("ang:", ang)
    print(f"dt shape: {dt.shape[0]}x{dt.shape[1]}")
    print("dt:", dt)

    # Call to the function which finds the optimum distances for a segment.
    bdt = bstdst(dt, Q, P, ang, k)

    print("After bstdst:")
    print(f"bdt shape: {bdt.shape[0]}x{bdt.shape[1]}")
    print("bdt:", bdt)

    bdt1 = [] # Empty list

    for i in range(2):
        bdt1.extend(bdt[i, :])

    print(f"bdt1 length: {len(bdt1)}")
    print("bdt1:", bdt1)

    # Assemble the vector of parameters for the curve.
    SOC = np.concatenate([P[0, :], P[1, :], ang, bdt1])
    
    print(f"SOC length: {len(SOC)}")
    print("SOC:", SOC)
    print("=== SEGOP DEBUG END ===")
    
    return SOC