package com.hybridroots;

import java.util.function.Function;

/**
 * Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding.
 *
 * <p>All algorithms are deterministic and guarantee convergence for any continuous
 * function {@code f} on a bracket {@code [a, b]} where {@code f(a)*f(b) < 0}.</p>
 *
 * <p>Reference: Ellithy, A. (2026). <em>Four New Multi-Phase Hybrid Bracketing
 * Algorithms for Numerical Root Finding.</em> Journal of the Egyptian Mathematical
 * Society, 34.<br>
 * DOI: <a href="https://doi.org/10.21608/joems.2026.440115.1078">
 * 10.21608/joems.2026.440115.1078</a></p>
 *
 * @author Abdelrahman Ellithy
 * @version 1.0.0
 */
public final class HybridRoots {

    /** Default absolute tolerance. */
    public static final double DEFAULT_TOL = 1e-14;
    /** Default maximum iterations. */
    public static final int DEFAULT_MAX_ITER = 10000;

    private HybridRoots() { /* utility class */ }

    private static final double EPS = 1e-15;

    /**
     * Multi-Phase Bisection-False Position (Opt.BF) Algorithm.
     *
     * <p>Combines Bisection with False Position for guaranteed convergence
     * with faster interval reduction. See Section 2 of the paper.</p>
     *
     * @param f the continuous function whose root is sought
     * @param a the left endpoint of the bracket ({@code f(a)*f(b) < 0})
     * @param b the right endpoint of the bracket
     * @param tol absolute tolerance; convergence when {@code |f(x)| <= tol}
     * @param maxIter maximum number of iterations
     * @return a {@link HybridRootsResult} with root, iterations, functionCalls, converged
     * @see <a href="https://doi.org/10.21608/joems.2026.440115.1078">Paper DOI</a>
     */
    public static HybridRootsResult mpbf(Function<Double, Double> f, double a, double b, double tol, int maxIter) {
        double fa = f.apply(a), fb = f.apply(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
        if (Math.abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
        if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

        for (int n = 1; n <= maxIter; n++) {
            double mid = 0.5 * (a + b);
            double fmid = f.apply(mid);
            nfe++;
            if (Math.abs(fmid) <= tol) return new HybridRootsResult(mid, n, nfe, true);
            if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double fp = (a * fb - b * fa) / denom;
            double ffp = f.apply(fp);
            nfe++;
            if (Math.abs(ffp) <= tol) return new HybridRootsResult(fp, n, nfe, true);
            if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        }
        double finalX = 0.5 * (a + b);
        boolean converged = Math.abs(f.apply(finalX)) <= tol;
        return new HybridRootsResult(finalX, maxIter, nfe + 1, converged);
    }

    /**
     * Multi-Phase Bisection-False Position-Modified Secant (Opt.BFMS) Algorithm.
     * @param f the function to find the root of
     * @param a the lower bound of the bracket
     * @param b the upper bound of the bracket
     * @param tol the tolerance for convergence
     * @param maxIter the maximum number of iterations
     * @return the result of the root finding algorithm
     */
    public static HybridRootsResult mpbfms(Function<Double, Double> f, double a, double b, double tol, int maxIter) {
        double fa = f.apply(a), fb = f.apply(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
        if (Math.abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
        if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

        for (int n = 1; n <= maxIter; n++) {
            double mid = 0.5 * (a + b);
            double fmid = f.apply(mid);
            nfe++;
            if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double fp = (a * fb - b * fa) / denom;
            double ffp = f.apply(fp);
            nfe++;
            if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
            if (Math.abs(ffp) <= tol) return new HybridRootsResult(fp, n, nfe, true);

            double delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + EPS;
            double fDelta = f.apply(fp + delta);
            nfe++;
            double denomSecant = fDelta - ffp;
            if (Math.abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
            double xS = fp - (delta * ffp) / denomSecant;

            if (xS > a && xS < b) {
                double fxS = f.apply(xS);
                nfe++;
                if (Math.abs(fxS) < Math.abs(ffp)) {
                    if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                    if (Math.abs(fxS) <= tol) return new HybridRootsResult(xS, n, nfe, true);
                }
            }
        }
        double finalX = 0.5 * (a + b);
        boolean converged = Math.abs(f.apply(finalX)) <= tol;
        return new HybridRootsResult(finalX, maxIter, nfe + 1, converged);
    }

    /**
     * Multi-Phase Trisection-False Position (Opt.TF) Algorithm.
     * @param f the function to find the root of
     * @param a the lower bound of the bracket
     * @param b the upper bound of the bracket
     * @param tol the tolerance for convergence
     * @param maxIter the maximum number of iterations
     * @return the result of the root finding algorithm
     */
    public static HybridRootsResult mptf(Function<Double, Double> f, double a, double b, double tol, int maxIter) {
        double fa = f.apply(a), fb = f.apply(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
        if (Math.abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
        if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

        for (int n = 1; n <= maxIter; n++) {
            double diff = b - a;
            double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
            double fx1 = f.apply(x1), fx2 = f.apply(x2);
            nfe += 2;
            if (Math.abs(fx1) <= tol) return new HybridRootsResult(x1, n, nfe, true);
            if (Math.abs(fx2) <= tol) return new HybridRootsResult(x2, n, nfe, true);

            if (fa * fx1 < 0) { b = x1; fb = fx1; }
            else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
            else { a = x2; fa = fx2; }

            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double x = (a * fb - b * fa) / denom;
            double fx = f.apply(x);
            nfe++;
            if (Math.abs(fx) <= tol) return new HybridRootsResult(x, n, nfe, true);
            if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
        }
        double finalX = 0.5 * (a + b);
        boolean converged = Math.abs(f.apply(finalX)) <= tol;
        return new HybridRootsResult(finalX, maxIter, nfe + 1, converged);
    }

    /**
     * Multi-Phase Trisection-False Position-Modified Secant (Opt.TFMS) Algorithm.
     * @param f the function to find the root of
     * @param a the lower bound of the bracket
     * @param b the upper bound of the bracket
     * @param tol the tolerance for convergence
     * @param maxIter the maximum number of iterations
     * @return the result of the root finding algorithm
     */
    public static HybridRootsResult mptfms(Function<Double, Double> f, double a, double b, double tol, int maxIter) {
        double fa = f.apply(a), fb = f.apply(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
        if (Math.abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
        if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

        for (int n = 1; n <= maxIter; n++) {
            double diff = b - a;
            double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
            double fx1 = f.apply(x1), fx2 = f.apply(x2);
            nfe += 2;
            if (Math.abs(fx1) <= tol) return new HybridRootsResult(x1, n, nfe, true);
            if (Math.abs(fx2) <= tol) return new HybridRootsResult(x2, n, nfe, true);

            if (fa * fx1 < 0) { b = x1; fb = fx1; }
            else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
            else { a = x2; fa = fx2; }

            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double fp = (a * fb - b * fa) / denom;
            double ffp = f.apply(fp);
            nfe++;
            if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
            if (Math.abs(ffp) <= tol) return new HybridRootsResult(fp, n, nfe, true);

            double delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + EPS;
            double fDelta = f.apply(fp + delta);
            nfe++;
            double denomSecant = fDelta - ffp;
            if (Math.abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
            double xS = fp - (delta * ffp) / denomSecant;

            if (xS > a && xS < b) {
                double fxS = f.apply(xS);
                nfe++;
                if (Math.abs(fxS) < Math.abs(ffp)) {
                    if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                    if (Math.abs(fxS) <= tol) return new HybridRootsResult(xS, n, nfe, true);
                }
            }
        }
        double finalX = 0.5 * (a + b);
        boolean converged = Math.abs(f.apply(finalX)) <= tol;
        return new HybridRootsResult(finalX, maxIter, nfe + 1, converged);
    }

    // ── Convenience overloads with default tol and maxIter ──────────────

    /** Calls {@link #mpbf(Function, double, double, double, int)} with default tolerance and max iterations. */
    public static HybridRootsResult mpbf(Function<Double, Double> f, double a, double b) {
        return mpbf(f, a, b, DEFAULT_TOL, DEFAULT_MAX_ITER);
    }

    /** Calls {@link #mpbfms(Function, double, double, double, int)} with default tolerance and max iterations. */
    public static HybridRootsResult mpbfms(Function<Double, Double> f, double a, double b) {
        return mpbfms(f, a, b, DEFAULT_TOL, DEFAULT_MAX_ITER);
    }

    /** Calls {@link #mptf(Function, double, double, double, int)} with default tolerance and max iterations. */
    public static HybridRootsResult mptf(Function<Double, Double> f, double a, double b) {
        return mptf(f, a, b, DEFAULT_TOL, DEFAULT_MAX_ITER);
    }

    /** Calls {@link #mptfms(Function, double, double, double, int)} with default tolerance and max iterations. */
    public static HybridRootsResult mptfms(Function<Double, Double> f, double a, double b) {
        return mptfms(f, a, b, DEFAULT_TOL, DEFAULT_MAX_ITER);
    }
}
