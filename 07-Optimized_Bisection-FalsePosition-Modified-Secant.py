# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

def f(x):
    return x**2 - x - 2
    
def mpbfms(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Bisection-False-Position-Modified-Secant root finder.

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
    n = 0
    eps = 1e-15
    nfe = 2
    # Check if either bound is a root
    if abs(fa) <= tol:
        return a, {'iterations': 1, 'function_calls': nfe, 'converged': True}
    if abs(fb) <= tol:
        return b, {'iterations': 1, 'function_calls': nfe, 'converged': True}
        
    if fa * fb >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    while n < max_iter:
        n += 1
        mid = (a + b) * 0.5
        fmid = float(f(mid))
        nfe += 1
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
        dx = (a * fb) - (b * fa)
        try:
            fp = dx / (fb - fa )
        except (ValueError, OverflowError, ZeroDivisionError):
            fp = dx / ((fb - fa)+eps)
        ffp = float(f(fp))
        nfe += 1
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp

        if abs(ffp) <= tol:
            return fp, {'iterations': n, 'function_calls': nfe, 'converged': True}
    
        delta=1e-8* max(1, abs(fp)) + 1e-15
        try:
            xS = fp - (delta * ffp) / (float(f(fp + delta)) - ffp)
            nfe += 1
        except (ValueError, OverflowError, ZeroDivisionError):
            xS = fp - (delta * ffp) / ((float(f(fp + delta)) - ffp)+eps)
            nfe += 1
        if (a < xS< b):
            fxS = float(f(xS))
            nfe += 1
            if abs(fxS) < abs(ffp):
                if fa * fxS < 0:
                    b, fb = xS, fxS
                else:
                    a, fa = xS, fxS
                if abs(fxS) <= tol:
                    return xS, {'iterations': n, 'function_calls': nfe, 'converged': True}
    final_x = (a + b) * 0.5
    f_final = float(f(final_x))
    nfe += 1
    return final_x, {'iterations': n, 'function_calls': nfe, 'converged': abs(f_final) <= tol}

if __name__ == "__main__":
    a = 1
    b = 4
    tol = 1e-14
    root, info = mpbfms(f, a, b, tol)
    if root is not None:
        f_root = f(root)
        print(f"Root found: {root} with f(root) = {f_root}")
        print(f"Iterations: {info['iterations']}, Function calls: {info['function_calls']}, Converged: {info['converged']}")
    else:
        print("No root found in the given interval.")