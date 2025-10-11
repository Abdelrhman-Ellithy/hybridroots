# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 08:54:54 2024

@author: Abdelrahman Ellithy
"""

# Import modules
import sympy as sp
import time
import math
import sqlite3
def rest_data():
    con = sqlite3.connect('Results.db')
    cursor = con.cursor()
    cursor.execute(""" 
            create table IF NOT EXISTS results(
            id Integer PRIMARY KEY not null,
            problemId Integer problemId not null,
            method_name text,
            CPU_Time REAL
            )""")
    con.commit()
    con.close()
def record_speeds(records):
    try:
        with sqlite3.connect('Results.db') as con:
            cursor = con.cursor()
            cursor.executemany("INSERT INTO results (problemId, method_name, CPU_Time) VALUES (?, ?, ?)", records)
            con.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
import json
import os


def _load_iters_from_config(cfg_file='config.json'):
    try:
        if os.path.exists(cfg_file):
            with open(cfg_file, 'r', encoding='utf-8') as fh:
                cfg = json.load(fh)
            outer = int(cfg.get('outer_iterations', 100))
            inner = int(cfg.get('inner_iterations', 100))
        else:
            outer, inner = 100, 100
    except Exception:
        outer, inner = 100, 100
    return outer, inner


OUTER_ITERS, INNER_ITERS = _load_iters_from_config()
# Function to load dataset from JSON file
def load_dataset(file_path='dataset.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)
    dataset = []
    for item in data:
        expr = sp.sympify(item['expression'])
        a = item['a']
        b = item['b']
        dataset.append((expr, a, b))
    return dataset

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
    
def blendTF(f, a, b, tol, max_iter=10000):
    """
    Implements Badr-2021-A Comparative Study among New Hybrid Root Finding Algorithms and Traditional Method (Trisection + False Position), Algorithm 7, page 8.
    This function implements the Hybrid Method of Trisection and False-Position to find
    a root  of the function (f) within the interval [a, b] with a given tolerance (tol).
    
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
    
    # Define the trisection interval [a1, b1]
    a1 = a
    b1 = b
    
    # Define the false-position interval [a2, b2]
    a2 = a
    b2 = b
    
    # Iterate until maximum iterations reached, or |f(x)| <= tol
    while n < max_iter:
        # Increment the iteration counter by 1
        n += 1
        
        # Calculate f(a) and f(b)
        fa = f(a)
        fb = f(b)
        
        # Calculate xT1 and xT2 using the trisection method
        xT1 = (b + 2*a) / 3
        xT2 = (2*b + a) / 3
        fxT1 = f(xT1)
        fxT2 = f(xT2)
        
        # Calculate xF using the false-position method
        try:
            xF = a - (fa*(b-a)) / (fb-fa)
        except (ValueError, OverflowError, ZeroDivisionError):
            eps = 1e-20
            xF = a - (fa*(b-a)) / ((fb-fa) + eps)
        fxF = f(xF)
        
        # Choose the root with the smaller error
        x = xT1
        fx = fxT1
        
        if abs(fxT2) < abs(fx):
            x = xT2
            fx = fxT2
        
        if abs(fxF) < abs(fx):
            x = xF
            fx = fxF
        
        # Check if the absolute value of f(x) is smaller than the tolerance
        if abs(fx) <= tol:
            break
        
        # Determine the new trisection interval [a1, b1]
        if fa * fxT1 < 0:
            b1 = xT1
        elif fxT1 * fxT2 < 0:
            a1 = xT1
            b1 = xT2
        else:
            a1 = xT2
        
        # Determine the new false-position interval [a2, b2]
        if fa * fxF < 0:
            b2 = xF
        else:
            a2 = xF
        
        # Take the intersection between [a1, b1] and [a2, b2]
        a = max(a1, a2)
        b = min(b1, b2)
    
    # Return the number of iterations, estimated root, function value, lower bound, and upper bound
    return n, x, fx, a, b



# Define the symbolic variable x
x = sp.Symbol('x')
# Load the dataset from JSON
dataset = load_dataset()
tol = 1e-14
method='04-Badr-2021-A Comparative Study among New Hybrid Root Finding Algorithms-Hybrid-Blend-Trisection-Falseposition'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for c in range(OUTER_ITERS):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(INNER_ITERS):
            n, x_val, fx, a_val, b_val = blendTF(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        if None in (n, x_val, fx, a_val, b_val):
            print(f"problem{i+1}| \tFailed: No root found in interval")
        else:
            print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

if records:
    record_speeds(records)