# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

def f(x):
    return x**2 - x - 2

def mpbf(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Bisection-False-Position root finder.

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
    eps = 1e-15
    nfe = 2
    # Check if either bound is a root
    if abs(fa) <= tol:
        return a, {'iterations': 1, 'function_calls': nfe, 'converged': True}
    if abs(fb) <= tol:
        return b, {'iterations': 1, 'function_calls': nfe, 'converged': True}
    
    if fa * fb >= 0:
        return None, None, None, None, None
    for n in range(1, max_iter + 1):
        mid = 0.5 * (a + b)
        fmid = float(f(mid))
        nfe += 1
        if abs(fmid) <= tol:
            return mid, {'iterations': n, 'function_calls': nfe, 'converged': True}
                
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
        dx = ((a * fb) - (b * fa))
        try:
            fp = dx / (fb - fa)
        except (ValueError, OverflowError, ZeroDivisionError):
            fp = dx / ((fb - fa)+eps)        
        ffp = float(f(fp))
        nfe += 1
        if abs(ffp) <= tol:
            return fp, {'iterations': n, 'function_calls': nfe, 'converged': True}
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp

    final_x = 0.5 * (a + b)
    f_final = float(f(final_x))
    nfe += 1
    return final_x, {'iterations': max_iter, 'function_calls': nfe, 'converged': abs(f_final) <= tol}


if __name__ == "__main__":
    a = 1
    b = 4
    tol = 1e-14
    root, info = mpbf(f, a, b, tol)
    if root is not None:
        f_root = f(root)
        print(f"Root found: {root} with f(root) = {f_root}")
        print(f"Iterations: {info['iterations']}, Function calls: {info['function_calls']}, Converged: {info['converged']}")
    else:
        print("No root found in the given interval.")