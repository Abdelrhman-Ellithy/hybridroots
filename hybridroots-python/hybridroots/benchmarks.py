"""
Benchmark suite for hybridroots algorithms.

Contains 48 standard benchmark functions from the paper with their intervals,
and comparison utilities against SciPy's brentq.

Reference:
    Ellithy, A. (2026). Four New Multi-Phase Hybrid Bracketing Algorithms
    for Numerical Root Finding. Journal of the Egyptian Mathematical Society, 34.

Usage:
    python -m hybridroots.benchmarks
"""

import math
import time
from typing import Callable, Dict, List, Tuple

from .core import mpbf, mpbfms, mptf, mptfms

__all__ = ["BENCHMARK_FUNCTIONS", "run_benchmarks", "compare_with_scipy"]


# Mathematical functions
def _exp(x):
    return math.exp(x)

def _sin(x):
    return math.sin(x)

def _cos(x):
    return math.cos(x)

def _log(x):
    return math.log(x)

def _log10(x):
    return math.log10(x)

def _sqrt(x):
    return math.sqrt(x)


# 48 Benchmark Functions from the Paper
BENCHMARK_FUNCTIONS: List[Dict] = [
    # Problem 1
    {"name": "f1", "func": lambda x: x * _exp(x) - 7, "a": 1, "b": 2,
     "description": "x*exp(x) - 7"},
    
    # Problem 2
    {"name": "f2", "func": lambda x: x**3 - x - 1, "a": 1, "b": 2,
     "description": "x^3 - x - 1"},
    
    # Problem 3
    {"name": "f3", "func": lambda x: x**2 - x - 2, "a": 1, "b": 4,
     "description": "x^2 - x - 2"},
    
    # Problem 4
    {"name": "f4", "func": lambda x: x - _cos(x), "a": 0, "b": 1,
     "description": "x - cos(x)"},
    
    # Problem 5
    {"name": "f5", "func": lambda x: x**2 - 10, "a": 3, "b": 4,
     "description": "x^2 - 10"},
    
    # Problem 6
    {"name": "f6", "func": lambda x: _sin(x) - x**2, "a": 0.5, "b": 1,
     "description": "sin(x) - x^2"},
    
    # Problem 7
    {"name": "f7", "func": lambda x: x + _log(x), "a": 0.1, "b": 1,
     "description": "x + ln(x)"},
    
    # Problem 8
    {"name": "f8", "func": lambda x: _exp(x) - 3*x - 2, "a": 2, "b": 3,
     "description": "exp(x) - 3x - 2"},
    
    # Problem 9
    {"name": "f9", "func": lambda x: x**2 + _exp(x/2) - 5, "a": 1, "b": 2,
     "description": "x^2 + exp(x/2) - 5"},
    
    # Problem 10
    {"name": "f10", "func": lambda x: x * _sin(x) - 1, "a": 0, "b": 2,
     "description": "x*sin(x) - 1"},
    
    # Problem 11
    {"name": "f11", "func": lambda x: x * _cos(x) + 1, "a": -2, "b": 4,
     "description": "x*cos(x) + 1"},
    
    # Problem 12
    {"name": "f12", "func": lambda x: x**10 - 1, "a": 0, "b": 1.3,
     "description": "x^10 - 1"},
    
    # Problem 13
    {"name": "f13", "func": lambda x: x**2 + 2*x - 7, "a": 1, "b": 3,
     "description": "x^2 + 2x - 7"},
    
    # Problem 14
    {"name": "f14", "func": lambda x: x**3 - 2*x - 5, "a": 2, "b": 3,
     "description": "x^3 - 2x - 5"},
    
    # Problem 15
    {"name": "f15", "func": lambda x: _exp(x) - 3*x**2, "a": 0, "b": 1,
     "description": "exp(x) - 3x^2"},
    
    # Problem 16
    {"name": "f16", "func": lambda x: _sin(10*x) - 0.5*x, "a": 0.1, "b": 0.4,
     "description": "sin(10x) - 0.5x"},
    
    # Problem 17
    {"name": "f17", "func": lambda x: x - 0.8*_sin(x) - 1.2, "a": 1, "b": 3,
     "description": "x - 0.8*sin(x) - 1.2"},
    
    # Problem 18
    {"name": "f18", "func": lambda x: x**2 - _exp(x) - 3*x + 2, "a": 0, "b": 1,
     "description": "x^2 - exp(x) - 3x + 2"},
    
    # Problem 19
    {"name": "f19", "func": lambda x: (x - 1)**3 + 4*(x - 1)**2 - 10, "a": 0, "b": 3,
     "description": "(x-1)^3 + 4(x-1)^2 - 10"},
    
    # Problem 20
    {"name": "f20", "func": lambda x: _exp(x**2) - _exp(_sqrt(2)*x), "a": 0.5, "b": 1.5,
     "description": "exp(x^2) - exp(sqrt(2)*x)"},
    
    # Problem 21
    {"name": "f21", "func": lambda x: (x**2 - 4)*(x + 1.5)*(x - 0.5), "a": 0, "b": 2,
     "description": "(x^2-4)(x+1.5)(x-0.5)"},
    
    # Problem 22
    {"name": "f22", "func": lambda x: x**3 - 3*x**2 - 4*x + 13, "a": -3, "b": -2,
     "description": "x^3 - 3x^2 - 4x + 13"},
    
    # Problem 23
    {"name": "f23", "func": lambda x: -0.9*x**2 + 1.7*x + 2.5, "a": 2.8, "b": 3.0,
     "description": "-0.9x^2 + 1.7x + 2.5"},
    
    # Problem 24
    {"name": "f24", "func": lambda x: 1 - 0.61*x, "a": 1.5, "b": 2.0,
     "description": "1 - 0.61x (linear)"},
    
    # Problem 25
    {"name": "f25", "func": lambda x: x**2 * abs(_sin(x)) - 4.1, "a": 0, "b": 4,
     "description": "x^2*|sin(x)| - 4.1"},
    
    # Problem 26
    {"name": "f26", "func": lambda x: x**5 - 3*x**4 + 25, "a": -3, "b": -1,
     "description": "x^5 - 3x^4 + 25"},
    
    # Problem 27
    {"name": "f27", "func": lambda x: x**4 - 2*x**2 - 4, "a": 1, "b": 3,
     "description": "x^4 - 2x^2 - 4"},
    
    # Problem 28
    {"name": "f28", "func": lambda x: x - 0.5*_sin(x) - 1, "a": 0, "b": 3,
     "description": "x - 0.5*sin(x) - 1"},
    
    # Problem 29
    {"name": "f29", "func": lambda x: _exp(-x) - _cos(3*x) - 0.5, "a": 0, "b": 1,
     "description": "exp(-x) - cos(3x) - 0.5"},
    
    # Problem 30 - High-degree polynomial (Wilkinson-like)
    {"name": "f30", "func": lambda x: (x-1)*(x-2)*(x-3)*(x-4)*(x-5)*(x-6)*(x-7)*(x-8)*(x-9)*(x-10)*(x-11)*(x-12)*(x-13)*(x-14)*(x-15)*(x-16)*(x-17)*(x-18)*(x-19)*(x-20), 
     "a": 0, "b": 1.5, "description": "Wilkinson-like deg-20 polynomial"},
    
    # Problem 31 - High-degree polynomial root at 20
    {"name": "f31", "func": lambda x: (x-1)*(x-2)*(x-3)*(x-4)*(x-5)*(x-6)*(x-7)*(x-8)*(x-9)*(x-10)*(x-11)*(x-12)*(x-13)*(x-14)*(x-15)*(x-16)*(x-17)*(x-18)*(x-19)*(x-20),
     "a": 19, "b": 21, "description": "Wilkinson-like deg-20 at root 20"},
    
    # Problem 32
    {"name": "f32", "func": lambda x: x**4 + 2*x**2 - x - 1, "a": -0.5, "b": 0,
     "description": "x^4 + 2x^2 - x - 1"},
    
    # Problem 33
    {"name": "f33", "func": lambda x: x**4 - 10*x**3 + 35*x**2 - 50*x + 24, "a": 0, "b": 1.5,
     "description": "x^4 - 10x^3 + 35x^2 - 50x + 24"},
    
    # Problem 34
    {"name": "f34", "func": lambda x: 4*_sin(x) - x + 1, "a": -1, "b": 0,
     "description": "4sin(x) - x + 1"},
    
    # Problem 35
    {"name": "f35", "func": lambda x: x**25 - 1, "a": 0, "b": 2,
     "description": "x^25 - 1"},
    
    # Problem 36 - Near multiple root
    {"name": "f36", "func": lambda x: (x - 1.8)**6 * (x - 1.81), "a": 0, "b": 2,
     "description": "(x-1.8)^6*(x-1.81) - near multiple root"},
    
    # Problem 37
    {"name": "f37", "func": lambda x: _sin(20*x) - 0.3*x, "a": 0.05, "b": 0.25,
     "description": "sin(20x) - 0.3x"},
    
    # Problem 38
    {"name": "f38", "func": lambda x: x**4 + 2*x**3 - 13*x**2 - 14*x + 24, "a": -3, "b": 1,
     "description": "x^4 + 2x^3 - 13x^2 - 14x + 24"},
    
    # Problem 39
    {"name": "f39", "func": lambda x: _exp(x**2) - _exp(1.2*x), "a": 0, "b": 2,
     "description": "exp(x^2) - exp(1.2x)"},
    
    # Problem 40
    {"name": "f40", "func": lambda x: x**5 - 3*x**4 + 2*x**3 - x + 0.1, "a": -1, "b": 3,
     "description": "x^5 - 3x^4 + 2x^3 - x + 0.1"},
    
    # Problem 41
    {"name": "f41", "func": lambda x: (x + 0.3)**7 - 0.01, "a": -2, "b": 1,
     "description": "(x+0.3)^7 - 0.01"},
    
    # Problem 42
    {"name": "f42", "func": lambda x: x**6 - 8*x**5 + 24*x**4 - 32*x**3 + 16*x**2, "a": 0, "b": 4,
     "description": "x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2"},
    
    # Problem 43 - Colebrook-White equation
    {"name": "f43", "func": lambda x: -2*_log10(0.000027027 + 2.51/(10000000*_sqrt(x))) - 1/_sqrt(x),
     "a": 0.008, "b": 0.03, "description": "Colebrook-White friction factor"},
    
    # Problem 44 - Kepler equation
    {"name": "f44", "func": lambda x: x - 0.99*_sin(x) - 2.0, "a": 2.0, "b": 3.0,
     "description": "Kepler equation (e=0.99)"},
    
    # Problem 45 - Van der Waals equation
    {"name": "f45", "func": lambda x: (10.0 + 3.592/x**2)*(x - 0.04267) - 0.08206*300,
     "a": 2.0, "b": 3.0, "description": "Van der Waals (CO2)"},
    
    # Problem 46 - Financial/transcendental
    {"name": "f46", "func": lambda x: x*_exp(x/2) - 1.5, "a": 0.0, "b": 1.0,
     "description": "x*exp(x/2) - 1.5"},
    
    # Problem 47 - Beam deflection
    {"name": "f47", "func": lambda x: _cos(x) + 1.0*(1 - _cos(x))**2 - 0.05*x**2,
     "a": 3.0, "b": 6.0, "description": "Beam deflection equation"},
    
    # Problem 48 - Chemical equilibrium
    {"name": "f48", "func": lambda x: 0.05 - x**3/((1 - x)*(0.8 - 2*x)**2),
     "a": 0.01, "b": 0.3, "description": "Chemical equilibrium"},
]

# Expected iterations from paper (Opt.BFMS column from Algorithm_Iterations_Matrix.csv)
EXPECTED_ITERATIONS_BFMS = [
    3, 3, 3, 2, 2, 3, 2, 3, 3, 2,  # 1-10
    3, 4, 3, 3, 3, 2, 3, 2, 3, 4,  # 11-20
    1, 3, 2, 1, 4, 4, 4, 2, 3, 5,  # 21-30
    1, 3, 4, 2, 1, 6, 2, 1, 1, 5,  # 31-40
    5, 1, 3, 2, 2, 3, 3, 4         # 41-48
]


def run_single_benchmark(func: Callable, a: float, b: float, 
                         algorithm: Callable, tol: float = 1e-14) -> Dict:
    """Run a single benchmark and return results."""
    # Warmup
    try:
        algorithm(func, a, b, tol=tol)
    except Exception:
        pass
        
    runs = 100
    start_time = time.perf_counter()
    try:
        for _ in range(runs):
            root, info = algorithm(func, a, b, tol=tol)
        elapsed = (time.perf_counter() - start_time) * 1e6 / runs  # microseconds
        
        # Verify root
        f_root = func(root)
        
        return {
            "root": root,
            "f_root": f_root,
            "iterations": info["iterations"],
            "function_calls": info["function_calls"],
            "converged": info["converged"],
            "time_us": elapsed,
            "error": None
        }
    except Exception as e:
        elapsed = (time.perf_counter() - start_time) * 1e6
        return {
            "root": None,
            "f_root": None,
            "iterations": None,
            "function_calls": None,
            "converged": False,
            "time_us": elapsed,
            "error": str(e)
        }


def run_benchmarks(tol: float = 1e-14, verbose: bool = True) -> Dict:
    """
    Run all 48 benchmark functions with all four algorithms.
    
    Parameters
    ----------
    tol : float
        Tolerance for convergence.
    verbose : bool
        Print progress and summary.
    
    Returns
    -------
    results : dict
        Dictionary with algorithm names as keys, containing lists of results.
    """
    algorithms = {
        "mpbf": mpbf,
        "mpbfms": mpbfms,
        "mptf": mptf,
        "mptfms": mptfms,
    }
    
    results = {name: [] for name in algorithms}
    
    if verbose:
        print("=" * 70)
        print("HybridRoots Benchmark Suite - 48 Functions")
        print("=" * 70)
    
    for i, benchmark in enumerate(BENCHMARK_FUNCTIONS):
        if verbose:
            print(f"\n[{i+1:2d}/48] {benchmark['name']}: {benchmark['description']}")
        
        for alg_name, alg_func in algorithms.items():
            result = run_single_benchmark(
                benchmark["func"], benchmark["a"], benchmark["b"], 
                alg_func, tol
            )
            result["problem"] = benchmark["name"]
            results[alg_name].append(result)
            
            if verbose:
                if result["converged"]:
                    print(f"       {alg_name:8s}: iter={result['iterations']:2d}, "
                          f"nfe={result['function_calls']:3d}, "
                          f"|f(x)|={abs(result['f_root']):.2e}")
                else:
                    print(f"       {alg_name:8s}: FAILED - {result['error']}")
    
    if verbose:
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        
        for alg_name in algorithms:
            converged = sum(1 for r in results[alg_name] if r["converged"])
            avg_iter = sum(r["iterations"] for r in results[alg_name] if r["converged"]) / max(converged, 1)
            avg_nfe = sum(r["function_calls"] for r in results[alg_name] if r["converged"]) / max(converged, 1)
            avg_time = sum(r["time_us"] for r in results[alg_name] if r["converged"]) / max(converged, 1)
            
            print(f"{alg_name:8s}: {converged}/48 converged, "
                  f"avg_iter={avg_iter:.2f}, avg_nfe={avg_nfe:.1f}, "
                  f"avg_time={avg_time:.1f}μs")
    
    return results


def compare_with_scipy(tol: float = 1e-14, verbose: bool = True) -> Dict:
    """
    Compare hybridroots algorithms with scipy.optimize.brentq.
    
    Requires: pip install scipy
    """
    try:
        from scipy.optimize import brentq
    except ImportError:
        print("scipy not installed. Run: pip install scipy")
        return {}
    
    algorithms = {
        "mpbf": mpbf,
        "mpbfms": mpbfms,
        "mptf": mptf,
        "mptfms": mptfms,
    }
    
    results = {name: [] for name in algorithms}
    results["brentq"] = []
    
    if verbose:
        print("=" * 80)
        print("Comparison: HybridRoots vs SciPy brentq")
        print("=" * 80)
        print("Warming up to avoid CPU bias...")
    for _ in range(10):        
        for benchmark in BENCHMARK_FUNCTIONS:
            func = benchmark["func"]
            a, b = benchmark["a"], benchmark["b"]
            try:
                brentq(func, a, b, xtol=tol, full_output=False)
            except Exception:
                pass
            for alg_func in algorithms.values():
                try:
                    alg_func(func, a, b, tol=tol)
                except Exception:
                    pass
    
    for i, benchmark in enumerate(BENCHMARK_FUNCTIONS):
        if verbose:
            print(f"\n[{i+1:2d}/48] {benchmark['name']}: {benchmark['description']}")
        
        # Run brentq
        try:
            brentq(benchmark["func"], benchmark["a"], benchmark["b"], xtol=tol, full_output=False)
        except Exception:
            pass
            
        runs = 100
        start = time.perf_counter()
        try:
            for _ in range(runs):
                root_brent, r_brent = brentq(benchmark["func"], benchmark["a"], benchmark["b"], xtol=tol, full_output=True)
            elapsed = (time.perf_counter() - start) * 1e6 / runs
            
            nfe = r_brent.function_calls
            iters = max(0, nfe - 1)
            
            results["brentq"].append({
                "problem": benchmark["name"],
                "root": root_brent,
                "f_root": benchmark["func"](root_brent),
                "time_us": elapsed,
                "iterations": iters,
                "function_calls": nfe,
                "converged": r_brent.converged,
                "error": None
            })
            if verbose:
                print(f"       brentq  : root={root_brent:.10f}, "
                      f"iter={iters:2d}, nfe={nfe:3d}")
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1e6
            results["brentq"].append({
                "problem": benchmark["name"],
                "root": None,
                "iterations": 0,
                "function_calls": 0,
                "converged": False,
                "error": str(e),
                "time_us": elapsed
            })
            if verbose:
                print(f"       brentq   : FAILED - {e}")
        
        # Run hybridroots
        for alg_name, alg_func in algorithms.items():
            result = run_single_benchmark(
                benchmark["func"], benchmark["a"], benchmark["b"],
                alg_func, tol
            )
            result["problem"] = benchmark["name"]
            results[alg_name].append(result)
            
            if verbose and result["converged"]:
                print(f"       {alg_name:8s}: root={result['root']:.10f}, "
                      f"iter={result['iterations']:2d}, nfe={result['function_calls']:3d}")
    
    if verbose:
        print("\n" + "=" * 80)
        print("SUMMARY RESULTS (Over 48 Benchmark Problems)")
        print("=" * 80)
        print(f"{'Algorithm':<10s} | {'Converged':<10s} | {'Total Time (us)':<18s} | {'Avg NFE':<10s} | {'Avg Iterations':<15s}")
        print("-" * 80)
        
        all_algs = ["brentq"] + list(algorithms.keys())
        for alg_name in all_algs:
            alg_results = results[alg_name]
            converged_runs = [r for r in alg_results if r.get("converged", False)]
            converged = len(converged_runs)
            total_problems = len(alg_results)
            
            if converged > 0:
                avg_nfe = sum(r.get("function_calls", 0) for r in converged_runs) / converged
                avg_iter = sum(r.get("iterations", 0) for r in converged_runs) / converged
                total_time = sum(r.get("time_us", 0) for r in converged_runs)
                print(f"{alg_name:<10s} | {converged:>2d}/{total_problems:<7d} | {total_time:>18.2f} | {avg_nfe:>10.2f} | {avg_iter:>15.2f}")
            else:
                print(f"{alg_name:<10s} | {0:>2d}/{total_problems:<7d} | {'N/A':>18s} | {'N/A':>10s} | {'N/A':>15s}")
        print("=" * 80)
        
    return results


def validate_against_paper(verbose: bool = True) -> bool:
    """
    Validate that Opt.BFMS iteration counts match the paper.
    
    Returns True if all problems match within tolerance.
    """
    if verbose:
        print("=" * 60)
        print("Validating Opt.BFMS against paper results")
        print("=" * 60)
    
    all_match = True
    
    for i, benchmark in enumerate(BENCHMARK_FUNCTIONS):
        result = run_single_benchmark(
            benchmark["func"], benchmark["a"], benchmark["b"],
            mpbfms, tol=1e-14
        )
        
        expected = EXPECTED_ITERATIONS_BFMS[i]
        actual = result["iterations"]
        match = (actual == expected)
        
        if not match:
            all_match = False
        
        if verbose:
            status = "✓" if match else "✗"
            print(f"[{i+1:2d}] {benchmark['name']}: expected={expected}, "
                  f"actual={actual} {status}")
    
    if verbose:
        print("\n" + ("ALL TESTS PASSED" if all_match else "SOME TESTS FAILED"))
    
    return all_match


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        validate_against_paper()
    elif len(sys.argv) > 1 and sys.argv[1] == "--scipy":
        compare_with_scipy()
    else:
        run_benchmarks()
