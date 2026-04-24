package com.hybridroots;

/**
 * Result of a root finding algorithm.
 */
public class HybridRootsResult {
    /** The estimated root location. */
    public double root;
    /** The number of iterations performed. */
    public int iterations;
    /** The number of function evaluations performed. */
    public int functionCalls;
    /** True if the algorithm converged to the specified tolerance. */
    public boolean converged;

    /**
     * Constructs a HybridRootsResult.
     * @param root the estimated root
     * @param iterations the number of iterations
     * @param functionCalls the number of function evaluations
     * @param converged whether the algorithm converged
     */
    public HybridRootsResult(double root, int iterations, int functionCalls, boolean converged) {
        this.root = root;
        this.iterations = iterations;
        this.functionCalls = functionCalls;
        this.converged = converged;
    }
}
