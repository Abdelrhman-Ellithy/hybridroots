"""
Core implementations of multi-phase hybrid bracketing root-finding algorithms.

This module provides four novel root-finding algorithms that combine classical
bracketing methods (bisection, trisection, false position) with modified secant
for efficient and reliable convergence.

All algorithms guarantee convergence for continuous functions with a valid bracket
(f(a) and f(b) have opposite signs).

Reference:
    Ellithy, A. (2026). Four New Multi-Phase Hybrid Bracketing Algorithms
    for Numerical Root Finding. Journal of the Egyptian Mathematical Society, 34.
"""

__all__ = ["mpbf", "mpbfms", "mptf", "mptfms"]

# Small epsilon for numerical stability
_EPS = 1e-15


def mpbf(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Bisection-False Position root finder (Opt.BF).
    
    Combines bisection and false position methods in each iteration for
    reliable convergence with improved efficiency over pure bisection.
    
    Parameters
    ----------
    f : callable
        A continuous function for which to find a root.
        Must satisfy f(a) * f(b) < 0.
    a : float
        Left endpoint of the bracketing interval.
    b : float
        Right endpoint of the bracketing interval.
    tol : float, optional
        Absolute tolerance for |f(x)|. Default is 1e-14.
    max_iter : int, optional
        Maximum number of iterations. Default is 10000.
    
    Returns
    -------
    root : float
        The approximate root.
    info : dict
        Dictionary containing:
        - 'iterations': Number of iterations performed
        - 'function_calls': Total number of function evaluations
        - 'converged': Boolean indicating if tolerance was achieved
    
    Raises
    ------
    ValueError
        If f(a) and f(b) do not have opposite signs.
    
    Notes
    -----
    Algorithm per iteration:
    1. Bisection step: compute midpoint and narrow bracket
    2. False position step: compute regula falsi estimate and narrow bracket
    
    Average performance: ~6.7 iterations, 2 NFE/iteration on standard benchmarks.
    
    Examples
    --------
    >>> def f(x): return x**3 - x - 2
    >>> root, info = mpbf(f, 1, 2)
    >>> abs(f(root)) < 1e-14
    True
    >>> info['converged']
    True
    """
    fa, fb = float(f(a)), float(f(b))
    nfe = 2
    
    # Check if endpoints are roots
    if abs(fa) <= tol:
        return a, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    if abs(fb) <= tol:
        return b, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    
    # Validate bracket
    if fa * fb >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    for n in range(1, max_iter + 1):
        # Phase 1: Bisection
        mid = 0.5 * (a + b)
        fmid = float(f(mid))
        nfe += 1
        
        if abs(fmid) <= tol:
            return mid, {'iterations': n, 'function_calls': nfe, 'converged': True}
        
        # Update bracket based on bisection
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
        
        # Phase 2: False Position (Regula Falsi)
        denom = fb - fa
        if abs(denom) < _EPS:
            denom = denom + _EPS if denom >= 0 else denom - _EPS
        
        fp = (a * fb - b * fa) / denom
        ffp = float(f(fp))
        nfe += 1
        
        if abs(ffp) <= tol:
            return fp, {'iterations': n, 'function_calls': nfe, 'converged': True}
        
        # Update bracket based on false position
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp
    
    # Max iterations reached, return best estimate
    final_x = 0.5 * (a + b)
    f_final = float(f(final_x))
    nfe += 1
    return final_x, {'iterations': max_iter, 'function_calls': nfe, 'converged': abs(f_final) <= tol}


def mpbfms(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Bisection-False Position-Modified Secant root finder (Opt.BFMS).
    
    Combines bisection, false position, and modified secant with adaptive 
    step size for superlinear convergence while maintaining guaranteed bracketing.
    
    Parameters
    ----------
    f : callable
        A continuous function for which to find a root.
        Must satisfy f(a) * f(b) < 0.
    a : float
        Left endpoint of the bracketing interval.
    b : float
        Right endpoint of the bracketing interval.
    tol : float, optional
        Absolute tolerance for |f(x)|. Default is 1e-14.
    max_iter : int, optional
        Maximum number of iterations. Default is 10000.
    
    Returns
    -------
    root : float
        The approximate root.
    info : dict
        Dictionary containing:
        - 'iterations': Number of iterations performed
        - 'function_calls': Total number of function evaluations
        - 'converged': Boolean indicating if tolerance was achieved
    
    Raises
    ------
    ValueError
        If f(a) and f(b) do not have opposite signs.
    
    Notes
    -----
    Algorithm per iteration:
    1. Bisection step: compute midpoint and narrow bracket
    2. False position step: compute regula falsi estimate and narrow bracket
    3. Modified secant step: use adaptive δ for derivative-free Newton-like update
       Only applied if the new point lies within the bracket and improves the solution.
    
    The adaptive δ is computed as: δ = 1e-8 * max(1, |x|) + 1e-15
    
    Average performance: ~2.8 iterations, 3-4 NFE/iteration on standard benchmarks.
    
    Examples
    --------
    >>> def f(x): return x**3 - x - 2
    >>> root, info = mpbfms(f, 1, 2)
    >>> abs(f(root)) < 1e-14
    True
    >>> info['iterations']
    3
    """
    fa, fb = float(f(a)), float(f(b))
    nfe = 2
    
    # Check if endpoints are roots
    if abs(fa) <= tol:
        return a, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    if abs(fb) <= tol:
        return b, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    
    # Validate bracket
    if fa * fb >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    for n in range(1, max_iter + 1):
        # Phase 1: Bisection
        mid = 0.5 * (a + b)
        fmid = float(f(mid))
        nfe += 1
        
        # Update bracket based on bisection
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
        
        # Phase 2: False Position
        denom = fb - fa
        if abs(denom) < _EPS:
            denom = denom + _EPS if denom >= 0 else denom - _EPS
        
        fp = (a * fb - b * fa) / denom
        ffp = float(f(fp))
        nfe += 1
        
        # Update bracket based on false position
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp
        
        if abs(ffp) <= tol:
            return fp, {'iterations': n, 'function_calls': nfe, 'converged': True}
        
        # Phase 3: Modified Secant with adaptive delta
        delta = 1e-8 * max(1.0, abs(fp)) + _EPS
        
        f_delta = float(f(fp + delta))
        nfe += 1
        
        denom_secant = f_delta - ffp
        if abs(denom_secant) < _EPS:
            denom_secant = denom_secant + _EPS if denom_secant >= 0 else denom_secant - _EPS
        
        xS = fp - (delta * ffp) / denom_secant
        
        # Only use modified secant if within bracket and improves solution
        if a < xS < b:
            fxS = float(f(xS))
            nfe += 1
            
            if abs(fxS) < abs(ffp):
                if fa * fxS < 0:
                    b, fb = xS, fxS
                else:
                    a, fa = xS, fxS
                
                if abs(fxS) <= tol:
                    return xS, {'iterations': n, 'function_calls': nfe, 'converged': True}
    
    # Max iterations reached
    final_x = 0.5 * (a + b)
    f_final = float(f(final_x))
    nfe += 1
    return final_x, {'iterations': max_iter, 'function_calls': nfe, 'converged': abs(f_final) <= tol}


def mptf(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Trisection-False Position root finder (Opt.TF).
    
    Uses trisection (dividing interval into thirds) for faster interval
    reduction, followed by false position refinement.
    
    Parameters
    ----------
    f : callable
        A continuous function for which to find a root.
        Must satisfy f(a) * f(b) < 0.
    a : float
        Left endpoint of the bracketing interval.
    b : float
        Right endpoint of the bracketing interval.
    tol : float, optional
        Absolute tolerance for |f(x)|. Default is 1e-14.
    max_iter : int, optional
        Maximum number of iterations. Default is 10000.
    
    Returns
    -------
    root : float
        The approximate root.
    info : dict
        Dictionary containing:
        - 'iterations': Number of iterations performed
        - 'function_calls': Total number of function evaluations
        - 'converged': Boolean indicating if tolerance was achieved
    
    Raises
    ------
    ValueError
        If f(a) and f(b) do not have opposite signs.
    
    Notes
    -----
    Algorithm per iteration:
    1. Trisection step: compute two points at 1/3 and 2/3 of interval,
       reduce to the third containing the root
    2. False position step: compute regula falsi estimate and narrow bracket
    
    Trisection provides faster interval reduction (factor of 3 vs 2 for bisection)
    at the cost of one additional function evaluation per iteration.
    
    Average performance: ~5.3 iterations, 3 NFE/iteration on standard benchmarks.
    
    Examples
    --------
    >>> def f(x): return x**3 - x - 2
    >>> root, info = mptf(f, 1, 2)
    >>> abs(f(root)) < 1e-14
    True
    """
    fa, fb = float(f(a)), float(f(b))
    nfe = 2
    
    # Check if endpoints are roots
    if abs(fa) <= tol:
        return a, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    if abs(fb) <= tol:
        return b, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    
    # Validate bracket
    if fa * fb >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    for n in range(1, max_iter + 1):
        # Phase 1: Trisection
        diff = b - a
        x1 = a + diff / 3.0
        x2 = b - diff / 3.0
        
        fx1 = float(f(x1))
        fx2 = float(f(x2))
        nfe += 2
        
        if abs(fx1) <= tol:
            return x1, {'iterations': n, 'function_calls': nfe, 'converged': True}
        if abs(fx2) <= tol:
            return x2, {'iterations': n, 'function_calls': nfe, 'converged': True}
        
        # Determine which third contains the root
        if fa * fx1 < 0:
            b, fb = x1, fx1
        elif fx1 * fx2 < 0:
            a, b, fa, fb = x1, x2, fx1, fx2
        else:
            a, fa = x2, fx2
        
        # Phase 2: False Position
        denom = fb - fa
        if abs(denom) < _EPS:
            denom = denom + _EPS if denom >= 0 else denom - _EPS
        
        x = (a * fb - b * fa) / denom
        fx = float(f(x))
        nfe += 1
        
        if abs(fx) <= tol:
            return x, {'iterations': n, 'function_calls': nfe, 'converged': True}
        
        # Update bracket
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
    
    # Max iterations reached
    final_x = 0.5 * (a + b)
    f_final = float(f(final_x))
    nfe += 1
    return final_x, {'iterations': max_iter, 'function_calls': nfe, 'converged': abs(f_final) <= tol}


def mptfms(f, a, b, tol=1e-14, max_iter=10000):
    """
    Multi-Phase Trisection-False Position-Modified Secant root finder (Opt.TFMS).
    
    Combines trisection, false position, and modified secant with adaptive
    step size for fast convergence.
    
    Parameters
    ----------
    f : callable
        A continuous function for which to find a root.
        Must satisfy f(a) * f(b) < 0.
    a : float
        Left endpoint of the bracketing interval.
    b : float
        Right endpoint of the bracketing interval.
    tol : float, optional
        Absolute tolerance for |f(x)|. Default is 1e-14.
    max_iter : int, optional
        Maximum number of iterations. Default is 10000.
    
    Returns
    -------
    root : float
        The approximate root.
    info : dict
        Dictionary containing:
        - 'iterations': Number of iterations performed
        - 'function_calls': Total number of function evaluations
        - 'converged': Boolean indicating if tolerance was achieved
    
    Raises
    ------
    ValueError
        If f(a) and f(b) do not have opposite signs.
    
    Notes
    -----
    Algorithm per iteration:
    1. Trisection step: divide interval into thirds, keep third with root
    2. False position step: regula falsi refinement
    3. Modified secant step: adaptive δ for superlinear convergence
       Only applied if point is within bracket and improves solution.
    
    Average performance: ~2.4 iterations, 4-5 NFE/iteration on standard benchmarks.
    
    Examples
    --------
    >>> def f(x): return x**3 - x - 2
    >>> root, info = mptfms(f, 1, 2)
    >>> abs(f(root)) < 1e-14
    True
    >>> info['iterations']
    2
    """
    fa, fb = float(f(a)), float(f(b))
    nfe = 2
    
    # Check if endpoints are roots
    if abs(fa) <= tol:
        return a, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    if abs(fb) <= tol:
        return b, {'iterations': 0, 'function_calls': nfe, 'converged': True}
    
    # Validate bracket
    if fa * fb >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    for n in range(1, max_iter + 1):
        # Phase 1: Trisection
        diff = b - a
        x1 = a + diff / 3.0
        x2 = b - diff / 3.0
        
        fx1 = float(f(x1))
        fx2 = float(f(x2))
        nfe += 2
        
        if abs(fx1) <= tol:
            return x1, {'iterations': n, 'function_calls': nfe, 'converged': True}
        if abs(fx2) <= tol:
            return x2, {'iterations': n, 'function_calls': nfe, 'converged': True}
        
        # Determine which third contains the root
        if fa * fx1 < 0:
            b, fb = x1, fx1
        elif fx1 * fx2 < 0:
            a, b, fa, fb = x1, x2, fx1, fx2
        else:
            a, fa = x2, fx2
        
        # Phase 2: False Position
        denom = fb - fa
        if abs(denom) < _EPS:
            denom = denom + _EPS if denom >= 0 else denom - _EPS
        
        fp = (a * fb - b * fa) / denom
        ffp = float(f(fp))
        nfe += 1
        
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp
        
        if abs(ffp) <= tol:
            return fp, {'iterations': n, 'function_calls': nfe, 'converged': True}
        
        # Phase 3: Modified Secant with adaptive delta
        delta = 1e-8 * max(1.0, abs(fp)) + _EPS
        
        f_delta = float(f(fp + delta))
        nfe += 1
        
        denom_secant = f_delta - ffp
        if abs(denom_secant) < _EPS:
            denom_secant = denom_secant + _EPS if denom_secant >= 0 else denom_secant - _EPS
        
        xS = fp - (delta * ffp) / denom_secant
        
        # Only use modified secant if within bracket and improves solution
        if a < xS < b:
            fxS = float(f(xS))
            nfe += 1
            
            if abs(fxS) < abs(ffp):
                if fa * fxS < 0:
                    b, fb = xS, fxS
                else:
                    a, fa = xS, fxS
                
                if abs(fxS) <= tol:
                    return xS, {'iterations': n, 'function_calls': nfe, 'converged': True}
    
    # Max iterations reached
    final_x = 0.5 * (a + b)
    f_final = float(f(final_x))
    nfe += 1
    return final_x, {'iterations': max_iter, 'function_calls': nfe, 'converged': abs(f_final) <= tol}
