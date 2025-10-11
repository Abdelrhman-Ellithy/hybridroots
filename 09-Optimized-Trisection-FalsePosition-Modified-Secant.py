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
    
def HtrisectionFalseMS(f, a, b, tol, max_iter=10000, delta=1e-4):
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

# Define the symbolic variable x
x = sp.Symbol('x')
# Load the dataset from JSON
dataset = load_dataset()
tol = 1e-14
method='09-Optimized_Trisection-FalsePosition-Modified Secant.py'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for c in range(OUTER_ITERS):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(INNER_ITERS):
            n, x_val, fx, a_val, b_val = HtrisectionFalseMS(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        if None in (n, x_val, fx, a_val, b_val):
            print(f"problem{i+1}| \tFailed: No root found in interval")
        else:
            print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

if records:
    record_speeds(records)