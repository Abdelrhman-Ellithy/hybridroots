"""
HybridRoots: Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding

Four novel root-finding algorithms combining bisection/trisection, false position,
and modified secant methods for efficient, reliable nonlinear equation solving.

Algorithms:
    mpbf    - Multi-Phase Bisection-False Position (Opt.BF)
    mpbfms  - Multi-Phase Bisection-False Position-Modified Secant (Opt.BFMS)
    mptf    - Multi-Phase Trisection-False Position (Opt.TF)
    mptfms  - Multi-Phase Trisection-False Position-Modified Secant (Opt.TFMS)

Reference:
    Ellithy, A. (2026). Four New Multi-Phase Hybrid Bracketing Algorithms
    for Numerical Root Finding. Journal of the Egyptian Mathematical Society, 34.

Example:
    >>> from hybridroots import mpbfms
    >>> def f(x): return x**3 - x - 2
    >>> root, info = mpbfms(f, 1, 2)
    >>> print(f"Root: {root:.10f}, Iterations: {info['iterations']}")
    Root: 1.5213797068, Iterations: 3
"""

__version__ = "1.0.0"
__author__ = "Abdelrahman Ellithy"

from .core import mpbf, mpbfms, mptf, mptfms

__all__ = ["mpbf", "mpbfms", "mptf", "mptfms", "__version__"]
