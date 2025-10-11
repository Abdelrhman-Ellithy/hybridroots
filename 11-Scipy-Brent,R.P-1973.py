# -*- coding: utf-8 -*-
"""
scipy Brent's Method 
@author: Abdelrahman Ellithy (adapted for comparison)
"""
from scipy import optimize
import sympy as sp
import time
import sqlite3
import json
import math
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

x = sp.Symbol('x')
# Load the dataset from JSON
dataset = load_dataset()
tol = 1e-14
method = '11-Scipy-Brent,R.P-1973'
print(method)
rest_data()
print("\t\tIter\t\t Time")
records = []
for c in range(OUTER_ITERS):
    for i, (func, a, b) in enumerate(dataset):
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(INNER_ITERS):
            try:
                z = optimize.brentq(f=f, a=a, b=b,rtol= tol,xtol=tol, maxiter=10000, full_output=True)
            except Exception:
                z = None
        t2 = time.perf_counter()
        t = t2 - t1
        records.append((i+1, method, t))
        print(f"problem{i+1}| \t{t}")
if records:
    record_speeds(records)