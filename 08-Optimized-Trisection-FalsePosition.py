# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

def f(x):
    return x**2 - x - 2

def mptf(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Trisection-False-Position root finder.

    Parameters
    ----------
    f : callable
        Function to find root of.
    a, b : float
        Bracketing interval with opposite signs.
    tol : float, optional
        Absolute tolerance (default 1e-14).
    max_iter : int, optional
        Maximum iterations (default 10000).

    Returns
    -------
    root : float
        Approximate root.
    info : dict
        {'iterations': int, 'function_calls': int, 'converged': bool}
    """
    fa, fb = float(f(a)), float(f(b))
    nfe = 2
    # Check if either bound is a root
    if abs(fa) <= tol:
        return a, {'iterations': 1, 'function_calls': nfe, 'converged': True}
    if abs(fb) <= tol:
        return b, {'iterations': 1, 'function_calls': nfe, 'converged': True}
    eps = 1e-15
    for n in range(1, max_iter + 1):
        # less +-/
        diff = b - a
        x1 = a + diff/3
        x2 = b - diff/3
        fx1, fx2 = float(f(x1)), float(f(x2))
        nfe += 2
        if abs(fx1) <= tol: return x1, {'iterations': n, 'function_calls': nfe, 'converged': True}
        if abs(fx2) <= tol: return x2, {'iterations': n, 'function_calls': nfe, 'converged': True}
        if fa * fx1 < 0:
            a, b, fb = a, x1, fx1
        elif fx1 * fx2 < 0:
            a, b, fa, fb = x1, x2, fx1, fx2
        else:
            a, fa = x2, fx2            
        try:
            dx = (a * fb - b * fa)
            dd = fb - fa  
            x = dx / dd
        except (ValueError, OverflowError, ZeroDivisionError):
            x = dx / (dd + eps)
        fx = float(f(x))
        nfe += 1
        if abs(fx) <= tol:
            return x, {'iterations': n, 'function_calls': nfe, 'converged': True}
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
    final_x=(a+b)/2
    f_final = float(f(final_x))
    nfe += 1
    return final_x, {'iterations': max_iter, 'function_calls': nfe, 'converged': abs(f_final) <= tol}

if __name__ == "__main__":
    a = 1
    b = 4
    tol = 1e-14
    root, info = mptf(f, a, b, tol)
    if root is not None:
        f_root = f(root)
        print(f"Root found: {root} with f(root) = {f_root}")
        print(f"Iterations: {info['iterations']}, Function calls: {info['function_calls']}, Converged: {info['converged']}")
    else:
        print("No root found in the given interval.")