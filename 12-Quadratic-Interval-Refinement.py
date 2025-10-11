# -*- coding: utf-8 -*-
"""
Quadratic Interval Refinement (QIR) implementation (derivation-free interval refinement)
Implements a robust variant that falls back to bisection when needed.
Author: Added to repository for reviewer-requested comparison
"""

import re
import sympy as sp
import time
import math
import sqlite3
import json
import os


def _load_iters_from_config(cfg_file='config.json'):
    # config keys: outer_iterations, inner_iterations (fallback to 100)
    try:
        if os.path.exists(cfg_file):
            with open(cfg_file, 'r', encoding='utf-8') as fh:
                cfg = json.load(fh)
            outer = int(cfg.get('outer_iterations', cfg.get('outer', cfg.get('c_iterations', 100))))
            inner = int(cfg.get('inner_iterations', cfg.get('inner', cfg.get('j_iterations', 100))))
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

def load_dataset(file_path='dataset.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)
    dataset = []
    for item in data:
        expr = sp.sympify(item['expression'])
        a = float(item['a'])
        b = float(item['b'])
        dataset.append((expr, a, b))
    return dataset

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


x = sp.Symbol('x')
tol = 1e-14
method = '12-Quadratic-Interval-Refinement'
print(method)
dataset = load_dataset()
tol = 1e-14
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
rest_data()
for c in range(OUTER_ITERS):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func, 'numpy')
        t1 = time.perf_counter()
        # Create copies of a and b for each inner loop to reset the interval
        a_start, b_start = a, b
        for j in range(INNER_ITERS):
            n, x_val, fx, a_val, b_val = QIR(f, a_start, b_start, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        if None in (n, x_val, fx, a_val, b_val):
            print(f"problem{i+1}| \tFailed: No root found in interval")
        else:
            print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

# Batch insert all records at once
if records:
    record_speeds(records)