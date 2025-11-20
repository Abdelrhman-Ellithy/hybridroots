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
    
def bisection(f, a, b, tol, max_iter=10000):
    """
    This function implements the Bisection method to find a root of the
    function (f) within the interval [a, b] with a given tolerance (tol).
    
    Parameters:
        f   (function): The function for which we want to find a root.\n
        a      (float): The lower bound of the initial interval.\n
        b      (float): The upper bound of the initial interval.\n
        tol    (float): The desired tolerance.\n
        max_iter (int): The maximum number of iterations.
                     
    Returns:
        n    (int): The number of iterations.\n
        x  (float): The estimated root of the function f within the interval [a, b].\n
        fx (float): The function value at the estimated root.\n
        a  (float): The lower bound of the final interval.\n
        b  (float): The upper bound of the final interval.
    """
    
    # Initialize the iteration counter
    n = 0
    
    # Iterate until maximum iterations reached, or |f(x)| <= tol
    while n < max_iter:
        # Increment the iteration counter by 1
        n += 1
        
        # Calculate the midpoint of the interval
        x = (a + b) / 2
        
        # Calculate f(x) and f(a)
        fx = f(x)
        fa = f(a)
        
        # Check if the absolute value of f(x) is smaller than the tolerance
        if abs(fx) <= tol:
            break
        # Determine the new interval [a, b]
        if fa * fx < 0:
            b = x
        else:
            a = x
    # Return the number of iterations, estimated root, function value, lower bound, and upper bound
    return n, x, fx, a, b



if __name__ == "__main__":
    # A. Setup Database (Optional if already exists)
    ScientificBenchmark.rest_data()

    # B. Initialize & Run
    # The class now auto-loads 'dataset.json' because we didn't pass a dataset!
    bench = ScientificBenchmark('config.json')
    
    results = bench.run(
        algorithm_func=bisection, 
        method_name='01-Normal-Bisection',
        tol=1e-14
    )
    
    # C. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")