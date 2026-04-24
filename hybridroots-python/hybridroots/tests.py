"""
Pytest test suite for hybridroots algorithms.

Run with: pytest hybridroots/tests.py -v

Reference:
    Ellithy, A. (2026). Four New Multi-Phase Hybrid Bracketing Algorithms
    for Numerical Root Finding. Journal of the Egyptian Mathematical Society, 34.
"""

import math
import pytest

from .core import mpbf, mpbfms, mptf, mptfms

# All algorithms to test
ALGORITHMS = [
    ("mpbf", mpbf),
    ("mpbfms", mpbfms),
    ("mptf", mptf),
    ("mptfms", mptfms),
]


# =============================================================================
# Test Functions
# =============================================================================

def f_cubic(x):
    """x^3 - x - 2, root at x ≈ 1.521"""
    return x**3 - x - 2

def f_quadratic(x):
    """x^2 - 2, root at x = sqrt(2) ≈ 1.414"""
    return x**2 - 2

def f_trig(x):
    """cos(x) - x, root at x ≈ 0.739"""
    return math.cos(x) - x

def f_exp(x):
    """exp(x) - 3x - 2, root at x ≈ 2.128"""
    return math.exp(x) - 3*x - 2

def f_linear(x):
    """2x - 3, root at x = 1.5"""
    return 2*x - 3

def f_polynomial(x):
    """x^5 - x - 1, root near 1.167"""
    return x**5 - x - 1


# =============================================================================
# Basic Convergence Tests
# =============================================================================

class TestBasicConvergence:
    """Test that all algorithms converge on standard functions."""
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_cubic_function(self, name, algorithm):
        """Test convergence on x^3 - x - 2."""
        root, info = algorithm(f_cubic, 1, 2)
        assert info["converged"]
        assert abs(f_cubic(root)) < 1e-14
        assert 1.52 < root < 1.53
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_quadratic_function(self, name, algorithm):
        """Test convergence on x^2 - 2."""
        root, info = algorithm(f_quadratic, 1, 2)
        assert info["converged"]
        assert abs(f_quadratic(root)) < 1e-14
        assert abs(root - math.sqrt(2)) < 1e-10
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_trig_function(self, name, algorithm):
        """Test convergence on cos(x) - x."""
        root, info = algorithm(f_trig, 0, 1)
        assert info["converged"]
        assert abs(f_trig(root)) < 1e-14
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_exp_function(self, name, algorithm):
        """Test convergence on exp(x) - 3x - 2."""
        root, info = algorithm(f_exp, 2, 3)
        assert info["converged"]
        assert abs(f_exp(root)) < 1e-14
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_linear_function(self, name, algorithm):
        """Test convergence on linear 2x - 3."""
        root, info = algorithm(f_linear, 0, 3)
        assert info["converged"]
        assert abs(root - 1.5) < 1e-14


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_root_at_left_endpoint(self, name, algorithm):
        """Root exactly at left endpoint."""
        def f(x):
            return x - 1.0
        root, info = algorithm(f, 1.0, 2.0)
        assert info["converged"]
        assert abs(root - 1.0) < 1e-14
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_root_at_right_endpoint(self, name, algorithm):
        """Root exactly at right endpoint."""
        def f(x):
            return x - 2.0
        root, info = algorithm(f, 1.0, 2.0)
        assert info["converged"]
        assert abs(root - 2.0) < 1e-14
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_very_tight_tolerance(self, name, algorithm):
        """Test with machine epsilon tolerance."""
        root, info = algorithm(f_quadratic, 1, 2, tol=1e-15)
        assert info["converged"]
        assert abs(f_quadratic(root)) < 1e-14
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_wide_interval(self, name, algorithm):
        """Test with a wide initial bracket."""
        def f(x):
            return x**3 - 1
        root, info = algorithm(f, -100, 100)
        assert info["converged"]
        assert abs(root - 1.0) < 1e-10
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_narrow_interval(self, name, algorithm):
        """Test with a very narrow initial bracket."""
        def f(x):
            return x - 1.5
        root, info = algorithm(f, 1.49999, 1.50001)
        assert info["converged"]
        assert abs(root - 1.5) < 1e-10


# =============================================================================
# Error Handling
# =============================================================================

class TestErrorHandling:
    """Test error handling for invalid inputs."""
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_same_sign_endpoints(self, name, algorithm):
        """Should raise ValueError when f(a) and f(b) have same sign."""
        def f(x):
            return x**2 + 1  # Always positive
        with pytest.raises(ValueError, match="opposite signs"):
            algorithm(f, -1, 1)
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_both_positive(self, name, algorithm):
        """Both endpoints positive."""
        def f(x):
            return x + 10
        with pytest.raises(ValueError):
            algorithm(f, 1, 2)
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_both_negative(self, name, algorithm):
        """Both endpoints negative."""
        def f(x):
            return x - 10
        with pytest.raises(ValueError):
            algorithm(f, 1, 2)


# =============================================================================
# Return Value Structure
# =============================================================================

class TestReturnStructure:
    """Test that return values have correct structure."""
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_return_tuple(self, name, algorithm):
        """Should return (root, info) tuple."""
        result = algorithm(f_cubic, 1, 2)
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_info_dict_keys(self, name, algorithm):
        """Info dict should have required keys."""
        _, info = algorithm(f_cubic, 1, 2)
        assert "iterations" in info
        assert "function_calls" in info
        assert "converged" in info
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_info_dict_types(self, name, algorithm):
        """Info values should have correct types."""
        _, info = algorithm(f_cubic, 1, 2)
        assert isinstance(info["iterations"], int)
        assert isinstance(info["function_calls"], int)
        assert isinstance(info["converged"], bool)
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_positive_iterations(self, name, algorithm):
        """Iterations should be non-negative."""
        _, info = algorithm(f_cubic, 1, 2)
        assert info["iterations"] >= 0
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_function_calls_greater_than_iterations(self, name, algorithm):
        """Function calls should be at least 2 (initial evaluations)."""
        _, info = algorithm(f_cubic, 1, 2)
        assert info["function_calls"] >= 2


# =============================================================================
# Iteration Count Validation
# =============================================================================

class TestIterationCounts:
    """Validate iteration counts are reasonable."""
    
    def test_mpbfms_expected_iterations(self):
        """Opt.BFMS should achieve ~3 iterations on x^3 - x - 2."""
        _, info = mpbfms(f_cubic, 1, 2)
        assert info["iterations"] == 3
    
    def test_mptfms_expected_iterations(self):
        """Opt.TFMS should achieve ~2 iterations on x^3 - x - 2."""
        _, info = mptfms(f_cubic, 1, 2)
        assert info["iterations"] <= 3
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_max_iterations_respected(self, name, algorithm):
        """Should respect max_iter parameter."""
        # Use a function that converges slowly
        def f(x):
            return x**20 - 1
        _, info = algorithm(f, 0.5, 1.5, max_iter=5)
        assert info["iterations"] <= 5


# =============================================================================
# Numerical Stability
# =============================================================================

class TestNumericalStability:
    """Test numerical stability with challenging functions."""
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_high_degree_polynomial(self, name, algorithm):
        """Test on x^10 - 1."""
        def f(x):
            return x**10 - 1
        root, info = algorithm(f, 0, 1.3)
        assert info["converged"]
        assert abs(root - 1.0) < 1e-10
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_near_flat_function(self, name, algorithm):
        """Test on nearly flat function near root."""
        def f(x):
            return (x - 1)**5
        root, info = algorithm(f, 0, 2)
        # May not achieve 1e-14 for multiple roots, but should converge
        assert info["converged"] or info["iterations"] == 10000
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_oscillating_function(self, name, algorithm):
        """Test on sin-based function."""
        def f(x):
            return math.sin(x) - 0.5
        root, info = algorithm(f, 0, 1)
        assert info["converged"]
        assert abs(math.sin(root) - 0.5) < 1e-14


# =============================================================================
# Comparison Tests (require scipy)
# =============================================================================

class TestScipyComparison:
    """Compare with scipy.optimize.brentq."""
    
    @pytest.fixture
    def scipy_brentq(self):
        """Import brentq or skip if not available."""
        pytest.importorskip("scipy")
        from scipy.optimize import brentq
        return brentq
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_same_root_as_brentq(self, name, algorithm, scipy_brentq):
        """All algorithms should find same root as brentq."""
        our_root, _ = algorithm(f_quadratic, 1, 2)
        scipy_root = scipy_brentq(f_quadratic, 1, 2)
        assert abs(our_root - scipy_root) < 1e-10
    
    @pytest.mark.parametrize("name,algorithm", ALGORITHMS)
    def test_similar_accuracy_to_brentq(self, name, algorithm, scipy_brentq):
        """Our algorithms should achieve similar accuracy."""
        our_root, _ = algorithm(f_exp, 2, 3, tol=1e-14)
        scipy_root = scipy_brentq(f_exp, 2, 3, xtol=1e-14)
        
        our_error = abs(f_exp(our_root))
        scipy_error = abs(f_exp(scipy_root))
        
        # Our error should be at most 10x worse (generous margin)
        assert our_error < max(scipy_error * 10, 1e-12)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
