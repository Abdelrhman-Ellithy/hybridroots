# Four New Hybrid Root Bracketing Algorithms: Optimization-Based Approaches for Numerical Root Finding

## Project Overview
This project presents four novel hybrid root bracketing algorithms that combine the reliability of traditional bracketing methods with the speed of optimization-based techniques. The algorithms are implemented in Python, evaluated on a diverse set of 48 test functions, and analyzed for convergence and computational efficiency. The results are compiled and discussed in an academic LaTeX paper.

Authors: Abdelrahman Ellithy

---

## Repository Structure
- **Python Scripts**: Each algorithm is implemented in its own script (e.g., `06-Optimized-Bisection-FalsePosition.py`, `07-Optimized_Bisection-FalsePosition-Modified-Secant.py`, etc.).
- **Results Files**:
  - CSV files containing raw results and summary tables (e.g., `Algorithm_CPU_Time_us_Matrix.csv`, `Iterations_Per_Algorithm.csv`, `Complexity_Per_Algorithm.csv`).
  - `Results.db`: SQLite database with raw results.
- **Plots**: PNG files visualizing CPU time and performance (e.g., `avg_cpu_time_per_algorithm.png`, `cpu_time_lineplot_per_problem.png`).
- **Analysis and Benchmarking**:
  - `benchmarker.py`: Script for running algorithms on the benchmark suite.
- **Configuration**: `config.json`, `dataset.json` for test functions and settings.

---

## About the Algorithms
This project introduces and compares four new hybrid root bracketing algorithms:

- **Optimized Bisection-False Position (Opt.BF)**:
  - Combines the reliability of bisection with the speed of the false position method.
  - Alternates between bisection and false position steps to quickly reduce the interval containing the root.

- **Optimized Bisection-False Position with Modified Secant (Opt.BFMS)**:
  - Extends Opt.BF by adding a modified secant step for even faster convergence.
  - Uses a small perturbation to approximate the derivative and refine the root estimate.
  - Leading performer with average 2.79 iterations, 10.48 microseconds CPU time, winning 45.83% of problems by execution time.

- **Optimized Trisection-False Position (Opt.TF)**:
  - Uses trisection (splitting the interval into three) instead of bisection for potentially faster convergence.
  - Integrates the false position method for acceleration.

- **Optimized Trisection-False Position with Modified Secant (Opt.TFMS)**:
  - Combines trisection, false position, and modified secant steps for maximum efficiency.
  - Offers high convergence speed across various function types.

All algorithms are designed to guarantee convergence (if the initial interval brackets a root) and are implemented using the SymPy library for high-precision computation. They outperform traditional methods like Bisection (3.5x speedup) and modern methods like Brent and QIR.

---

## How to Run the Algorithms
1. Ensure you have Python 3.11+ and the required packages:
   ```bash
   pip install sympy numpy pandas matplotlib scipy
   ```
2. Run each algorithm script individually (e.g., `python 06-Optimized-Bisection-FalsePosition.py`). Results will be stored in `Results.db`.
3. To run all algorithms and regenerate results, use `python benchmarker.py`.

---

## License
- See `LICENSE` for details.
