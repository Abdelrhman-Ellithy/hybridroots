# -*- coding: utf-8 -*-
"""
Quadratic Interval Refinement (QIR) implementation (derivation-free interval refinement)
Implements a robust variant that falls back to bisection when needed.
Author: Added to repository for reviewer-requested comparison
"""
from benchmarker import ScientificBenchmark
import re
import math


def safe_eval(f, x):
    try:
        y = f(x)
        y = float(y)
        if math.isfinite(y):
            return y
        return None
    except Exception:
        return None

def QIR(f, a, b, tol, max_iter=10000):
    """A direct and robust implementation of Abbott's QIR."""
    fa = safe_eval(f, a)
    fb = safe_eval(f, b)

    if fa is None or fb is None or fa * fb > 0:
        return None, None, None, None, None

    if abs(fa) < tol: return 1, a, fa, a, b
    if abs(fb) < tol: return 1, b, fb, a, b

    for n in range(1, max_iter + 1):
        if abs(b - a) < tol:
            return n, a, fa, a, b
        
        m = 0.5 * (a + b)
        fm = safe_eval(f, m)

        if fm is None or abs(fm) < tol:
            return n, m, fm, a, b

        # Calculate coefficients for y = Ax^2 + Bx + C
        # Using divided differences for better stability
        f_am = (fa - fm) / (a - m)
        f_mb = (fm - fb) / (m - b)
        
        A = (f_am - f_mb) / (a - b)
        B = f_am - A * (a + m)
        C = fa - A * a**2 - B * a
        
        # Use a numerically stable quadratic formula to find the root
        xq = None
        if abs(A) > 1e-12: # Check if it's genuinely quadratic
            discriminant = B**2 - 4*A*C
            if discriminant >= 0:
                # Stable formula avoids subtracting nearly equal numbers
                term = -0.5 * (B + math.copysign(math.sqrt(discriminant), B))
                r1 = term / A
                r2 = C / term if abs(term) > 1e-12 else None
                
                # Choose the root that is inside the current interval [a,b]
                candidates = [r for r in (r1, r2) if r is not None and min(a, b) < r < max(a, b)]
                if candidates:
                    # Pick candidate closest to midpoint m
                    xq = min(candidates, key=lambda r: abs(r - m))

        # --- Fallback Logic ---
        # If quadratic step failed or is unreasonable, try secant
        if xq is None:
            if abs(fb - fa) > 1e-12:
                x_sec = b - fb * (b - a) / (fb - fa)
                if min(a,b) < x_sec < max(a,b):
                    xq = x_sec

        # If all else fails, fallback to bisection
        if xq is None:
            xq = m

        fxq = safe_eval(f, xq)
        if fxq is None: # If evaluation fails, default to bisection
            xq, fxq = m, fm
        
        if abs(fxq) < tol:
            return n, xq, fxq, a, b
        
        # Update the interval
        if fa * fxq < 0:
            b, fb = xq, fxq
        else:
            a, fa = xq, fxq
            
    return max_iter, b, fb, a, b


if __name__ == "__main__":
    # A. Setup Database (Optional if already exists)
    ScientificBenchmark.rest_data()

    # B. Initialize & Run
    # The class now auto-loads 'dataset.json' because we didn't pass a dataset!
    bench = ScientificBenchmark('config.json')
    
    results = bench.run(
        algorithm_func=QIR, 
        method_name='12-Quadratic-Interval-Refinement',
        tol=1e-14
    )
    
    # C. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")