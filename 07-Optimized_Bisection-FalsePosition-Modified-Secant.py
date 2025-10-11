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
    
def HbisectionFalseMS(f, a, b, tol, max_iter=10000, delta=1e-4):
    fa, fb = f(a), f(b)
    n = 0
    eps = 1e-20
    
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
        p1=fp - delta * ffp
        p2=(f(fp + delta) - ffp)
        try:
            xS = p1 / p2
        except (ValueError, OverflowError, ZeroDivisionError):
            xS = p1 / (p2 + eps)
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

# Define the symbolic variable x
x = sp.Symbol('x')
# Load the dataset from JSON
dataset = load_dataset()
tol = 1e-14
method='07-Optimized-Bisection-FalsePosition-Modified Secant.py'
print(method)
rest_data()
print("\t\tIter\t\t Root\t\tFunction Value\t\t Lower Bound\t\t Upper Bound\t\t Time")
records = []
for c in range(OUTER_ITERS):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(INNER_ITERS):
            n, x_val, fx, a_val, b_val = HbisectionFalseMS(f, a, b, tol)
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        if None in (n, x_val, fx, a_val, b_val):
            print(f"problem{i+1}| \tFailed: No root found in interval")
        else:
            print(f"problem{i+1}| \t{n} \t {x_val:.16f} \t {fx:.16f} \t {a_val:.16f} \t {b_val:.16f} \t {t:.20f}")

if records:
    record_speeds(records)