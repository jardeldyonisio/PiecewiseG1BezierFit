#!/usr/bin/env python3
from iguess0 import iguess0

def BezierFitDemo(Q, n):
    k = None
    Qt = Q.T
    ctrl_pts = iguess0(Qt, n, k)
    return ctrl_pts

if __name__ == '__main__':
    BezierFitDemo()