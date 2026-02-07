# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

from benchmarker import ScientificBenchmark
import re
import math

# Safe evaluation helper to guard domain/overflow issues
def safe_eval(f, x):
    try:
        y = f(x)
        y = float(y)
        if math.isfinite(y):
            return y
        return None
    except Exception:
        return None
    
def HtrisectionFalseMS(f, a, b, tol, max_iter=10000, delta=1e-4):
    fa, fb = f(a), f(b)
    eps = 1e-15
    
    # Check if either bound is a root
    if abs(fa) <= tol:
        return 1, a, fa, a, b
    if abs(fb) <= tol:
        return 1, b, fb, a, b
    
    if fa * fb >= 0:
        return None, None, None, None, None
    for n in range(1, max_iter + 1):
        diff = b - a
        x1 = a + diff/3
        x2 = b - diff/3
        fx1, fx2 = f(x1), f(x2)
        if abs(fx1) <= tol: return n, x1, fx1, a, b
        if abs(fx2) <= tol: return n, x2, fx2, a, b

        if fa * fx1 < 0:
            b, fb = x1, fx1
        elif fx1 * fx2 < 0:
            a, b, fa, fb = x1, x2, fx1, fx2
        else:
            a, fa = x2, fx2    
        try:
            dx = (a * fb) - (b * fa)
            fp = dx / (fb - fa )
            ffp = f(fp)
        except (ValueError, OverflowError, ZeroDivisionError):
            fp = dx / ((fb - fa) + eps)
            ffp = f(fp)
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp

        if abs(ffp) <= tol:
            return n, fp, ffp, a, b
        delta=1e-8* max(1, abs(fp)) + 1e-15
        try:
            xS = fp - delta * ffp / (f(fp + delta) - ffp)

        except (ValueError, OverflowError, ZeroDivisionError):
            xS = fp - delta * ffp / ((f(fp + delta) - ffp) + eps)
            
        if (a < xS< b):
            fxS = f(xS)
            if abs(fxS) < abs(ffp):
                if fa * fxS < 0:
                    b, fb = xS, fxS
                else:
                    a, fa = xS, fxS
                if abs(fxS) <= tol:
                    return n, xS, fxS, a, b

    # Fallback to best estimate
    final_x = (a + b) * 0.5
    return max_iter, final_x, f(final_x), a, b

if __name__ == "__main__":
    # A. Setup Database (Optional if already exists)
    ScientificBenchmark.rest_data()

    # B. Initialize & Run
    # The class now auto-loads 'dataset.json' because we didn't pass a dataset!
    bench = ScientificBenchmark('config.json')
    
    results = bench.run(
        algorithm_func=HtrisectionFalseMS, 
        method_name='Opt.TFMS',
        tol=1e-14
    )
    
    # C. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")