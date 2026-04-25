package com.hybridroots;

/**
 * Holds the result of a HybridRoots algorithm call.
 *
 * <p>Mirrors {@code scipy.optimize.RootResults} for cross-language consistency.</p>
 *
 * <p>Reference: Ellithy, A. (2026). <em>Four New Multi-Phase Hybrid Bracketing Algorithms
 * for Numerical Root Finding.</em> Journal of the Egyptian Mathematical Society, 34.<br>
 * DOI: <a href="https://doi.org/10.21608/joems.2026.440115.1078">
 * 10.21608/joems.2026.440115.1078</a></p>
 */
public final class HybridRootsResult {
    /** Estimated root location. */
    public final double root;
    /** Number of iterations performed. */
    public final int iterations;
    /** Number of function evaluations performed. */
    public final int functionCalls;
    /** {@code true} if {@code |f(root)| <= tol}. */
    public final boolean converged;

    /**
     * Constructs a {@code HybridRootsResult}.
     *
     * @param root          the estimated root
     * @param iterations    the number of iterations performed
     * @param functionCalls the number of function evaluations performed
     * @param converged     {@code true} if the algorithm converged
     */
    public HybridRootsResult(double root, int iterations, int functionCalls, boolean converged) {
        this.root = root;
        this.iterations = iterations;
        this.functionCalls = functionCalls;
        this.converged = converged;
    }

    @Override
    public String toString() {
        return String.format(
            "HybridRootsResult(root=%.17g, iterations=%d, functionCalls=%d, converged=%b)",
            root, iterations, functionCalls, converged);
    }
}
