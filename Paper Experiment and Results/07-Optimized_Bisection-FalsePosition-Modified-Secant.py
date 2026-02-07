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
    
def HbisectionFalseMS(f, a, b, tol, max_iter=10000, delta=1e-4):
    fa, fb = f(a), f(b)
    n = 0
    eps = 1e-15
    
    # Check if either bound is a root
    if abs(fa) <= tol:
        return 1, a, fa, a, b
    if abs(fb) <= tol:
        return 1, b, fb, a, b
        
    if fa * fb >= 0:
        return None, None, None, None, None
    while n < max_iter:
        n += 1
        mid = (a + b) * 0.5
        fmid = f(mid)
        
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid

        dx = (a * fb) - (b * fa)
        try:
            fp = dx / (fb - fa )
        except (ValueError, OverflowError, ZeroDivisionError):
            fp = dx / ((fb - fa)+eps)
        ffp = f(fp)

        if fa * ffp < 0:
            b, fb = fp, ffp
        else:
            a, fa = fp, ffp

        if abs(ffp) <= tol:
            return n, fp, ffp, a, b
        
        delta=1e-8* max(1, abs(fp)) + 1e-15
        try:
            xS = fp - (delta * ffp) / (f(fp + delta) - ffp)
        except (ValueError, OverflowError, ZeroDivisionError):
            xS = fp - (delta * ffp) / ((f(fp + delta) - ffp)+eps)
        if (a < xS< b):
            fxS = f(xS)
            if abs(fxS) < abs(ffp):
                if fa * fxS < 0:
                    b, fb = xS, fxS
                else:
                    a, fa = xS, fxS
                if abs(fxS) <= tol:
                    return n, xS, fxS, a, b

    final_x = (a + b) * 0.5
    return n, final_x, f(final_x), a, b

if __name__ == "__main__":
    # A. Setup Database (Optional if already exists)
    ScientificBenchmark.rest_data()

    # B. Initialize & Run
    # The class now auto-loads 'dataset.json' because we didn't pass a dataset!
    bench = ScientificBenchmark('config.json')
    
    results = bench.run(
        algorithm_func=HbisectionFalseMS, 
        method_name='Opt.BFMS',
        tol=1e-14
    )
    
    # C. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")