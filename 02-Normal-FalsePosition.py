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
    
def false_position(f, a, b, tol, max_iter=10000):
    """
    This function implements the False Position method to find a root of the function (f)
    within the interval [a, b] with a given tolerance (tol).
    
    Parameters:
        f (function): The function for which we want to find a root.\n
        a    (float): The left endpoint of the initial interval.\n
        b    (float): The right endpoint of the initial interval.\n
        tol  (float): The desired tolerance.
                     
    Returns:
        x (float): The estimated root of the function f within the interval [a, b].
    """
    i = 0
    fx=0
    eps = 1e-20
    fa = f(a)
    fb = f(b)
    while i < max_iter:
        i += 1
        try:
            x = (a*fb - b*fa) / (fb - fa)
        except Exception:
            x = (a*fb - b*fa) / ((fb - fa) + eps)
        fx = f(x)
        if abs(fx) <= tol:
            break
        elif fa * fx < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    
    # Return the estimated root
    return i, x, fx, a, b



if __name__ == "__main__":
    # A. Setup Database (Optional if already exists)
    ScientificBenchmark.rest_data()

    # B. Initialize & Run
    # The class now auto-loads 'dataset.json' because we didn't pass a dataset!
    bench = ScientificBenchmark('config.json')
    
    results = bench.run(
        algorithm_func=false_position, 
        method_name='false_position ',
        tol=1e-14
    )
    
    # C. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")