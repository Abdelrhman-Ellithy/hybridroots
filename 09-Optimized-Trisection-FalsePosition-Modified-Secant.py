# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

def f(x):
    return x**2 - x - 2

    
def mptfms(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Trisection-False-Position-Modified-Secant root finder.

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
        return None, {'iterations': 0, 'function_calls': nfe, 'converged': False}
    for n in range(1, max_iter + 1):
        diff = b - a
        x1 = a + diff/3
        x2 = b - diff/3
        fx1, fx2 = float(f(x1)), float(f(x2))
        nfe += 2
        if abs(fx1) <= tol: return x1, {'iterations': n, 'function_calls': nfe, 'converged': True}
        if abs(fx2) <= tol: return x2, {'iterations': n, 'function_calls': nfe, 'converged': True}

        if fa * fx1 < 0:
            b, fb = x1, fx1
        elif fx1 * fx2 < 0:
            a, b, fa, fb = x1, x2, fx1, fx2
        else:
            a, fa = x2, fx2    
        try:
            dx = (a * fb) - (b * fa)
            fp = dx / (fb - fa )
            ffp = float(f(fp))
        except (ValueError, OverflowError, ZeroDivisionError):
            fp = dx / ((fb - fa) + eps)
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
            xS = fp - delta * ffp / (float(f(fp + delta)) - ffp)
        except (ValueError, OverflowError, ZeroDivisionError):
            xS = fp - delta * ffp / ((float(f(fp + delta)) - ffp) + eps)
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
    return final_x, {'iterations': max_iter, 'function_calls': nfe, 'converged': abs(f_final) <= tol}

if __name__ == "__main__":
    a = 1
    b = 4
    tol = 1e-14
    root, info = mptfms(f, a, b, tol)
    if root is not None:
        f_root = f(root)
        print(f"Root found: {root} with f(root) = {f_root}")
        print(f"Iterations: {info['iterations']}, Function calls: {info['function_calls']}, Converged: {info['converged']}")
    else:
        print("No root found in the given interval.")