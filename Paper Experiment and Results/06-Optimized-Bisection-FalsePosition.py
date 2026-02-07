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
# Define the bisection function
def HbisectionFalse(f, a, b, tol, max_iter=10000):
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
        mid = 0.5 * (a + b)
        fmid = f(mid)
        if abs(fmid) <= tol:
            return n, mid, fmid, a, b
        
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
        dx = ((a * fb) - (b * fa))
        try:
            fp = dx / (fb - fa)
        except (ValueError, OverflowError, ZeroDivisionError):
            fp = dx / ((fb - fa)+eps)        
        ffp = f(fp)
        if abs(ffp) <= tol:
            return n, fp, ffp, a, b
        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp
    # Max iterations reached
    final_x = 0.5 * (a + b)
    return max_iter, final_x, f(final_x), a, b


if __name__ == "__main__":
    # A. Setup Database (Optional if already exists)
    ScientificBenchmark.rest_data()

    # B. Initialize & Run
    # The class now auto-loads 'dataset.json' because we didn't pass a dataset!
    bench = ScientificBenchmark('config.json')
    
    results = bench.run(
        algorithm_func=HbisectionFalse, 
        method_name='Opt.BF',
        tol=1e-14
    )
    
    # C. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")