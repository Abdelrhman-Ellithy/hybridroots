# -*- coding: utf-8 -*-
"""
Brent's Method (Corrected)
@author: Abdelrahman Ellithy (adapted for comparison)
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

def BrentsMethod(f, a, b, tol, max_iter=10000):
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        return max_iter, (a + b) * 0.5, f((a + b) * 0.5), a, b
    if abs(fa) < abs(fb):
        a, b, fa, fb = b, a, fb, fa
    c, fc = a, fa
    mflag = True
    n = 0
    delta = 1e-4  # Small step to avoid division by zero
    eps = 1e-20
    while n < max_iter:
        n += 1
        prev_b = b
        # Inverse Quadratic Interpolation
        if fa != fc and fb != fc:
            try:
                s = a * fb * fc / ((fa - fb) * (fa - fc)) + b * fa * fc / ((fb - fa) * (fb - fc)) + c * fa * fb / ((fc - fa) * (fc - fb))
                # Ensure s is within acceptable bounds
                if not ((3*a + b)/4 < s < b or b < s < (3*a + b)/4) or \
                   (mflag and abs(s - b) >= abs(b - c) / 2) or \
                   (not mflag and abs(s - b) >= abs(c - prev_c) / 2):
                    s = (a + b) * 0.5
                    mflag = True
                else:
                    mflag = False
            except (ValueError, OverflowError, ZeroDivisionError):
                s = (a + b) * 0.5
                mflag = True
        else:
            # Secant
            try:
                s = b - fb * (b - a) / (fb - fa)
                if not ((3*a + b)/4 < s < b or b < s < (3*a + b)/4) or \
                   (mflag and abs(s - b) >= abs(b - c) / 2) or \
                   (not mflag and abs(s - b) >= abs(c - prev_c) / 2):
                    s = (a + b) * 0.5
                    mflag = True
                else:
                    mflag = False
            except (ValueError, OverflowError, ZeroDivisionError):
                s = (a + b) * 0.5
                mflag = True
        fs = f(s)
        if abs(fs) <= tol or abs(b - a) <= tol:
            return n, s, fs, a, b
        prev_c = c
        c, fc = a, fa
        a, fa = b, fb
        b, fb = s, fs
        if fa * fb >= 0:
            a, fa = c, fc
        if abs(fa) < abs(fb):
            a, b, fa, fb = b, a, fb, fa
        # Ensure minimum step size
        if abs(b - a) < delta:
            return n, b, fb, a, b
    final_x = (a + b) * 0.5
    return n, final_x, f(final_x), a, b

if __name__ == "__main__":
    # A. Setup Database (Optional if already exists)
    ScientificBenchmark.rest_data()

    # B. Initialize & Run
    # The class now auto-loads 'dataset.json' because we didn't pass a dataset!
    bench = ScientificBenchmark('config.json')
    
    results = bench.run(
        algorithm_func=BrentsMethod, 
        method_name='Brent (Impl.)',
        tol=1e-14
    )
    
    # C. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")