import numpy as np
from scipy.optimize import minimize
from objf2 import objf2

def globop(xi, Q, t, k, dpkpc):
    print("=== GLOBOP DEBUG ===")
    print(f"Testing objf2 before optimization:")
    obj_value = objf2(xi, Q, t, k, dpkpc)
    print(f"Initial objective value: {obj_value:.6f}")
    
    options = {'disp': False, 'xatol': 0.01, 'fatol': 0.01}
    GOC = minimize(objf2, xi, args=(Q, t, k, dpkpc), method='Nelder-Mead', options=options)
    
    obj_value_final = objf2(GOC.x, Q, t, k, dpkpc)
    print(f"Final objective value: {obj_value_final:.6f}")
    print("=== GLOBOP DEBUG END ===")
    
    return GOC.x
