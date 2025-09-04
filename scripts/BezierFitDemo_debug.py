import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from iguess0 import iguess0
from segop import segop  
from globop import globop
from cubicBezierToPolyline import cubicBezierToPolyline

def BezierFitDemo_debug():
    print("=== PYTHON DEBUG ===")
    
    demo = 1
    k = None

    if demo == 1:
        C = np.array([[0, 0],
                      [1, 2],
                      [3, 3],
                      [4, 2]])
        Q = cubicBezierToPolyline(C, 65)
        n = 3  # Starting number of knot points
        
    print(f"Demo: {demo}, n: {n}")
    print(f"Q shape: {Q.shape[0]}x{Q.shape[1]}")
    print("Q first 5 points:")
    print(Q[:5,:])

    # Now try to do a piecewise cubic Bézier fit to Q starting with n knot points
    Qt = Q.T
    print(f"Qt shape: {Qt.shape[0]}x{Qt.shape[1]}")

    IG, k, dpkpc = iguess0(Qt, n, k)

    print("=== AFTER IGUESS0 ===")
    print(f"IG length: {len(IG)}")
    print("k:", k)
    print("IG:", IG)

    # Improve the fit: Segmentally Optimum Only Curve (SOO)
    SOC = segop(k, Qt, IG)

    print("=== AFTER SEGOP ===")
    print(f"SOC length: {len(SOC)}")
    print("SOC:", SOC)

    # Improve it again: Segmentally then Globally Optimized Curve (SGO)
    GOC = globop(SOC, Qt, 0, k, dpkpc)

    print("=== AFTER GLOBOP ===")
    print(f"GOC length: {len(GOC)}")
    print("GOC:", GOC)

    print("=== PYTHON DEBUG END ===")

if __name__ == '__main__':
    BezierFitDemo_debug()
