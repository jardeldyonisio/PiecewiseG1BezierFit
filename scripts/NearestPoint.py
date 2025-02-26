from cubicBezierToPolyline import cubicBezierToPolyline
from findClosestPoint import findClosestPoint

def NearestPoint(C, P):
    # Compute complete Bezier
    Q = cubicBezierToPolyline(C, 128)

    # Find nearest point on Bezier
    ind = findClosestPoint(P, Q)
    ind = ind[0]
    ind = int(ind[0])

    np = Q[ind]
    return np