# HybridRoots

[![PyPI version](https://badge.fury.io/py/hybridroots.svg)](https://badge.fury.io/py/hybridroots)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding**

A Python package implementing four novel root-finding algorithms that combine bisection/trisection, false position, and modified secant methods for efficient, reliable nonlinear equation solving.

## Features

- **Four Algorithms**: Opt.BF, Opt.BFMS, Opt.TF, Opt.TFMS
- **Pure Python**: No external dependencies required
- **SciPy Compatible**: Same interface as `scipy.optimize.brentq`
- **Deterministic**: Guaranteed convergence for bracketed roots

## Algorithm Summary

| Algorithm | Method | Avg Iterations | NFE/iter |
|-----------|--------|---------------|----------|
| `mpbfms` | Bisection + False Position + Modified Secant | ~2.8 | 3-4 |
| `mptfms` | Trisection + False Position + Modified Secant | ~2.4 | 4-5 |
| `mpbf` | Bisection + False Position | ~6.7 | 2 |
| `mptf` | Trisection + False Position | ~5.3 | 3 |

##  Installation

```bash
pip install hybridroots
```

For development with testing:
```bash
pip install hybridroots[test]
```

## 🔧 Usage

```python
from hybridroots import mpbf, mpbfms, mptf, mptfms

# Define your function
def f(x):
    return x**3 - x - 2

# Find root in interval [1, 2]
root, info = mpbfms(f, 1, 2)
print(f"Root: {root}")  # Root: 1.5213797068045676
print(f"Iterations: {info['iterations']}")
print(f"Function calls: {info['function_calls']}")

# All algorithms have the same interface
root1, _ = mpbf(f, 1, 2)    # Opt.BF
root2, _ = mpbfms(f, 1, 2)  # Opt.BFMS
root3, _ = mptf(f, 1, 2)    # Opt.TF
root4, _ = mptfms(f, 1, 2)  # Opt.TFMS
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `f` | callable | required | Function to find root of |
| `a` | float | required | Left endpoint of bracket |
| `b` | float | required | Right endpoint of bracket |
| `tol` | float | 1e-14 | Absolute tolerance |
| `max_iter` | int | 10000 | Maximum iterations |

### Returns

| Value | Type | Description |
|-------|------|-------------|
| `root` | float | Approximate root |
| `info` | dict | `{'iterations', 'function_calls', 'converged'}` |

## 📖 Algorithm Overview

### Opt.BFMS (`mpbfms`)
Multi-phase **Bisection-False Position-Modified Secant** method:
1. Bisection step to reduce interval
2. False position step for refinement
3. Modified secant with adaptive δ

### Opt.TFMS (`mptfms`)
Multi-phase **Trisection-False Position-Modified Secant** method:
1. Trisection for interval reduction
2. False position refinement
3. Modified secant with adaptive δ

### Opt.BF (`mpbf`)
Multi-phase **Bisection-False Position** method. Each iteration:
1. Bisection step to reduce interval
2. False position step for refinement

### Opt.TF (`mptf`)
Multi-phase **Trisection-False Position** method:
1. Trisection (divides interval into thirds)
2. False position refinement

## 📚 Citation

If you use this package in your research, please cite:

```bibtex
@article{ellithy2026hybrid,
  title={Four New Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding},
  author={Ellithy, Abdelrahman},
  journal={Journal of the Egyptian Mathematical Society},
  volume={34},
  year={2026},
  publisher={National Information and Documentation Centre (NIDOC), Academy of Scientific Research and Technology, ASRT}
}
```

## Running Benchmarks

```bash
pip install hybridroots[benchmark]
python -m hybridroots.benchmarks
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Paper (DOI)](https://doi.org/10.21608/joems.2026.440115.1078)
- [Issue Tracker](https://github.com/Abdelrhman-Ellithy/NM-Algorithms/issues)
