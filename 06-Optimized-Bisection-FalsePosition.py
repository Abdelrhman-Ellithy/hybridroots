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
# Function to load dataset from JSON file
def load_dataset(file_path='dataset.json'):
    """
    Load and validate dataset from JSON file with comprehensive error handling.
    
    Returns:
        list: List of tuples (expression, a, b) for each problem
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Dataset file '{file_path}' not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in dataset file: {e}")
        return []
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return []
    
    dataset = []
    for i, item in enumerate(data):
        try:
            # Validate required fields
            if not all(key in item for key in ['expression', 'a', 'b']):
                print(f"Warning: Problem {i+1} missing required fields (expression, a, b). Skipping.")
                continue
            
            # Parse expression
            expr = sp.sympify(item['expression'])
            
            # Validate bounds
            a = float(item['a'])
            b = float(item['b'])
            
            if not math.isfinite(a) or not math.isfinite(b):
                print(f"Warning: Problem {i+1} has non-finite bounds. Skipping.")
                continue
                
            if a >= b:
                print(f"Warning: Problem {i+1} has invalid interval [a={a}, b={b}]. Skipping.")
                continue
            
            dataset.append((expr, a, b))
            
        except (ValueError, TypeError, sp.SympifyError) as e:
            print(f"Warning: Problem {i+1} has invalid data: {e}. Skipping.")
            continue
        except Exception as e:
            print(f"Warning: Unexpected error processing problem {i+1}: {e}. Skipping.")
            continue
    
    print(f"Loaded {len(dataset)} valid problems from dataset.")
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
# Define the bisection function
def HbisectionFalse(f, a, b, tol, max_iter=10000):
    fa, fb = f(a), f(b)
    eps = 1e-20
    
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
        dx = (a * fb - b * fa)
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


# Define the symbolic variable x
x = sp.Symbol('x')
# Load the dataset from JSON
dataset = load_dataset()
tol = 1e-14
method='06-Optimized-Bisection-FalsePosition'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for c in range(OUTER_ITERS):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(INNER_ITERS):
            n, x_val, fx, a_val, b_val = HbisectionFalse(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        if None in (n, x_val, fx, a_val, b_val):
            print(f"problem{i+1}| \tFailed: No root found in interval")
        else:
            print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

if records:
    record_speeds(records)