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
    """Quadratic Interval Refinement following Abbott (2012).

    This implementation follows the algorithmic idea in John Abbott,
    "Quadratic Interval Refinement for Real Roots" (arXiv:1203.1227 /
    ACM Comm. in Comp. Algebra 2014). The method fits a quadratic
    interpolant to (a,m,b) where m is the midpoint and attempts to
    take the root of that interpolant inside the interval. If the
    quadratic step fails to provide an interior point or does not
    improve over the midpoint, the algorithm falls back to bisection.

    Notes:
    - Abbott's analysis assumes arbitrary-precision rationals; here
      we use floating evaluation with safety fallbacks.
    - We require a sign change on [a,b] for classical convergence.

    Returns: n, x, fx, a, b (or None...,...) on failure to evaluate)
    """
    eps = 1e-20

    fa = safe_eval(f, a)
    fb = safe_eval(f, b)
    if fa is None or fb is None:
        return None, None, None, None, None

    # Immediate roots at endpoints
    if abs(fa) <= tol:
        return 1, a, fa, a, b
    if abs(fb) <= tol:
        return 1, b, fb, a, b

    # Require sign change for guaranteed bracketing refinement
    if fa * fb > 0:
        return None, None, None, None, None

    for n in range(1, max_iter+1):
        m = 0.5*(a+b)
        fm = safe_eval(f, m)
        if fm is None:
            return None, None, None, None, None

        # If midpoint is already good, return it
        if abs(fm) <= tol:
            return n, m, fm, a, b

        # Build quadratic interpolant q(x) through (a,fa),(m,fm),(b,fb)
        xa, xm, xb = a, m, b
        try:
            # Lagrange basis coefficients expansion to produce quadratic coefficients
            A = fa/((xa-xm)*(xa-xb)) + fm/((xm-xa)*(xm-xb)) + fb/((xb-xa)*(xb-xm))
            B = - (fa*(xm+xb)/((xa-xm)*(xa-xb)) + fm*(xa+xb)/((xm-xa)*(xm-xb)) + fb*(xa+xm)/((xb-xa)*(xb-xm)))
            C = fa*(xm*xb)/((xa-xm)*(xa-xb)) + fm*(xa*xb)/((xm-xa)*(xm-xb)) + fb*(xa*xm)/((xb-xa)*(xb-xm))
        except Exception:
            # numerical degeneracy: fallback to secant between endpoints
            try:
                xsec = b - fb*(b-a)/(fb-fa)
                fxsec = safe_eval(f, xsec)
                if fxsec is None:
                    return None, None, None, None, None
                if abs(fxsec) <= tol:
                    return n, xsec, fxsec, a, b
                # update bracket
                if fa * fxsec < 0:
                    b, fb = xsec, fxsec
                else:
                    a, fa = xsec, fxsec
                continue
            except Exception:
                # give up
                return None, None, None, None, None

        # Solve quadratic A x^2 + B x + C = 0 (coeffs in standard basis)
        xq = None
        if abs(A) < eps:
            # Linear case: B x + C = 0
            if abs(B) >= eps:
                xq = -C / B
        else:
            disc = B*B - 4*A*C
            if disc >= 0:
                sqrt_d = math.sqrt(disc)
                r1 = (-B + sqrt_d) / (2*A)
                r2 = (-B - sqrt_d) / (2*A)
                # choose root inside (a,b) and closest to midpoint if possible
                candidates = [r for r in (r1, r2) if a < r < b]
                if candidates:
                    # choose candidate closest to midpoint
                    xq = min(candidates, key=lambda r: abs(r - m))

        # If quadratic didn't produce a good interior root, try secant between endpoints
        if xq is None or not (a < xq < b):
            try:
                xsec = b - fb*(b-a)/(fb-fa)
                if a < xsec < b:
                    xq = xsec
            except Exception:
                xq = None

        # Fallback to midpoint (bisection) if no acceptable candidate
        if xq is None or not (a < xq < b):
            xq = m

        fxq = safe_eval(f, xq)
        if fxq is None:
            return None, None, None, None, None

        # Accept quadratic/secant step only if it reduces the function magnitude
        # compared to midpoint (heuristic from Abbott: require improvement)
        if abs(fxq) > abs(fm):
            # do bisection instead
            xq = m
            fxq = fm

        if abs(fxq) <= tol:
            return n, xq, fxq, a, b

        # Update bracket
        if fa * fxq < 0:
            b, fb = xq, fxq
        else:
            a, fa = xq, fxq

        # If interval width is small enough, return midpoint
        if abs(b - a) <= tol:
            final = 0.5*(a+b)
            ffinal = safe_eval(f, final)
            return n, final, ffinal, a, b

    # Max iterations reached
    final = 0.5*(a+b)
    ffinal = safe_eval(f, final)
    return max_iter, final, ffinal, a, b

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
        f = sp.lambdify('x', func)
        t1 = time.perf_counter()
        for j in range(INNER_ITERS):
            n, x_val, fx, a_val, b_val = QIR(f, a, b, tol)
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
