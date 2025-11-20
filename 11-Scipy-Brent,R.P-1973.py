# -*- coding: utf-8 -*-
"""
Benchmarking SciPy's Brent Method using the shared Benchmarker class.
"""
from scipy import optimize
from benchmarker import ScientificBenchmark

# --- Adapter Function ---
# We need this wrapper to make SciPy's brentq look like the function signature 
# that ScientificBenchmark expects: func(f, a, b, tol, **kwargs)

def brentq_adapter(f, a, b, tol, max_iter=10000):
    """
    Wraps scipy.optimize.brentq to return the format:
    (iterations, root, fx, a, b)
    """
    try:
        # full_output=True makes it return (root, result_object)
        root, res = optimize.brentq(
            f, a, b, 
            xtol=tol, 
            rtol=tol, 
            maxiter=max_iter, 
            full_output=True, 
            disp=False # Prevent printing errors to console
        )
        
        if res.converged:
            # Success! Return the tuple benchmarker expects
            return res.iterations, root, f(root), a, b
        else:
            return None, None, None, None, None
            
    except Exception:
        # Catches "f(a) and f(b) must have different signs" errors
        return None, None, None, None, None

# --- Execution ---

if __name__ == "__main__":
    # 1. Setup Database (if needed)
    ScientificBenchmark.rest_data()

    # 2. Initialize Benchmark
    # Auto-loads config.json
    bench = ScientificBenchmark('config.json')
    
    # 3. Run Benchmark
    # We pass our adapter function instead of QIR
    results = bench.run(
        algorithm_func=brentq_adapter, 
        method_name='11-Scipy-Brent,R.P-1973',
        tol=1e-14
    )
    
    # 4. Save Results
    if results:
        ScientificBenchmark.record_speeds(results)
        print("\nResults saved to database successfully.")