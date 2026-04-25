/**
 * @file hybridroots.hpp
 * @brief Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding.
 *
 * This header-only C++ library implements the four novel hybrid root-finding
 * algorithms introduced in:
 *
 *   Ellithy, A. (2026). "Four New Multi-Phase Hybrid Bracketing Algorithms for
 *   Numerical Root Finding." Journal of the Egyptian Mathematical Society, 34.
 *   DOI: https://doi.org/10.21608/joems.2026.440115.1078
 *
 * All algorithms are deterministic and guarantee convergence for continuous
 * functions with a valid bracket [a, b] where f(a)*f(b) < 0.
 *
 * @author Abdelrahman Ellithy
 * @version 1.0.0
 * @license Apache-2.0
 */
#pragma once
#include <cmath>
#include <functional>
#include <algorithm>
#include <stdexcept>

namespace hybridroots {

/**
 * @brief Result returned by every HybridRoots algorithm.
 *
 * Mirrors the structure of scipy.optimize.RootResults for cross-language
 * consistency.
 */
struct HybridRootsResult {
    double root;          ///< Estimated root location.
    int    iterations;    ///< Number of iterations performed.
    int    function_calls;///< Number of function evaluations performed.
    bool   converged;     ///< True if |f(root)| <= tol.
};

/// @cond INTERNAL
constexpr double HR_EPS = 1e-15;
/// @endcond

/**
 * @brief Multi-Phase Bisection–False Position (Opt.BF).
 *
 * Combines classical Bisection with False Position to achieve faster
 * convergence while maintaining a guaranteed bracket. Described in Section 2
 * of the paper (DOI: 10.21608/joems.2026.440115.1078).
 *
 * @param f        The continuous function whose root is sought.
 * @param a        Left endpoint of the initial bracket (f(a)*f(b) < 0).
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance; convergence declared when |f(x)| <= tol.
 * @param max_iter Maximum number of iterations allowed.
 * @return         HybridRootsResult containing root, iterations, function_calls, and converged.
 */
inline HybridRootsResult mpbf(const std::function<double(double)>& f,
                               double a, double b,
                               double tol = 1e-14, int max_iter = 10000) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) return {a, 0, nfe, true};
    if (std::abs(fb) <= tol) return {b, 0, nfe, true};
    if (fa * fb >= 0) return {a, 0, nfe, false};

    for (int n = 1; n <= max_iter; n++) {
        double mid = 0.5 * (a + b);
        double fmid = f(mid);
        nfe++;
        if (std::abs(fmid) <= tol) return {mid, n, nfe, true};
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

        double denom = fb - fa;
        if (std::abs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (std::abs(ffp) <= tol) return {fp, n, nfe, true};
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }
    double final_x = 0.5 * (a + b);
    bool converged = std::abs(f(final_x)) <= tol;
    return {final_x, max_iter, nfe + 1, converged};
}

/**
 * @brief Multi-Phase Bisection–False Position–Modified Secant (Opt.BFMS).
 *
 * Extends Opt.BF with an adaptive Modified Secant acceleration step that
 * is accepted only when it reduces the residual and remains in-bracket.
 * Described in Section 3 of the paper (DOI: 10.21608/joems.2026.440115.1078).
 *
 * @param f        The continuous function whose root is sought.
 * @param a        Left endpoint of the initial bracket.
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance.
 * @param max_iter Maximum number of iterations.
 * @return         HybridRootsResult.
 */
inline HybridRootsResult mpbfms(const std::function<double(double)>& f,
                                 double a, double b,
                                 double tol = 1e-14, int max_iter = 10000) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) return {a, 0, nfe, true};
    if (std::abs(fb) <= tol) return {b, 0, nfe, true};
    if (fa * fb >= 0) return {a, 0, nfe, false};

    for (int n = 1; n <= max_iter; n++) {
        double mid = 0.5 * (a + b);
        double fmid = f(mid);
        nfe++;
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

        double denom = fb - fa;
        if (std::abs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (std::abs(ffp) <= tol) return {fp, n, nfe, true};

        double delta = 1e-8 * std::max(1.0, std::abs(fp)) + HR_EPS;
        double f_delta = f(fp + delta);
        nfe++;
        double denom_secant = f_delta - ffp;
        if (std::abs(denom_secant) < HR_EPS) denom_secant = denom_secant >= 0 ? denom_secant + HR_EPS : denom_secant - HR_EPS;
        double xS = fp - (delta * ffp) / denom_secant;

        if (xS > a && xS < b) {
            double fxS = f(xS);
            nfe++;
            if (std::abs(fxS) < std::abs(ffp)) {
                if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                if (std::abs(fxS) <= tol) return {xS, n, nfe, true};
            }
        }
    }
    double final_x = 0.5 * (a + b);
    bool converged = std::abs(f(final_x)) <= tol;
    return {final_x, max_iter, nfe + 1, converged};
}

/**
 * @brief Multi-Phase Trisection–False Position (Opt.TF).
 *
 * Divides the bracket into thirds at each phase for faster interval
 * reduction, then applies False Position refinement.
 * Described in Section 4 of the paper (DOI: 10.21608/joems.2026.440115.1078).
 *
 * @param f        The continuous function whose root is sought.
 * @param a        Left endpoint of the initial bracket.
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance.
 * @param max_iter Maximum number of iterations.
 * @return         HybridRootsResult.
 */
inline HybridRootsResult mptf(const std::function<double(double)>& f,
                               double a, double b,
                               double tol = 1e-14, int max_iter = 10000) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) return {a, 0, nfe, true};
    if (std::abs(fb) <= tol) return {b, 0, nfe, true};
    if (fa * fb >= 0) return {a, 0, nfe, false};

    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (std::abs(fx1) <= tol) return {x1, n, nfe, true};
        if (std::abs(fx2) <= tol) return {x2, n, nfe, true};

        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }

        double denom = fb - fa;
        if (std::abs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double x = (a * fb - b * fa) / denom;
        double fx = f(x);
        nfe++;
        if (std::abs(fx) <= tol) return {x, n, nfe, true};
        if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
    }
    double final_x = 0.5 * (a + b);
    bool converged = std::abs(f(final_x)) <= tol;
    return {final_x, max_iter, nfe + 1, converged};
}

/**
 * @brief Multi-Phase Trisection–False Position–Modified Secant (Opt.TFMS).
 *
 * Combines Trisection, False Position, and an adaptive Modified Secant step
 * for maximum efficiency. The fastest of the four algorithms for smooth functions.
 * Described in Section 5 of the paper (DOI: 10.21608/joems.2026.440115.1078).
 *
 * @param f        The continuous function whose root is sought.
 * @param a        Left endpoint of the initial bracket.
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance.
 * @param max_iter Maximum number of iterations.
 * @return         HybridRootsResult.
 */
inline HybridRootsResult mptfms(const std::function<double(double)>& f,
                                 double a, double b,
                                 double tol = 1e-14, int max_iter = 10000) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) return {a, 0, nfe, true};
    if (std::abs(fb) <= tol) return {b, 0, nfe, true};
    if (fa * fb >= 0) return {a, 0, nfe, false};

    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (std::abs(fx1) <= tol) return {x1, n, nfe, true};
        if (std::abs(fx2) <= tol) return {x2, n, nfe, true};

        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }

        double denom = fb - fa;
        if (std::abs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (std::abs(ffp) <= tol) return {fp, n, nfe, true};

        double delta = 1e-8 * std::max(1.0, std::abs(fp)) + HR_EPS;
        double f_delta = f(fp + delta);
        nfe++;
        double denom_secant = f_delta - ffp;
        if (std::abs(denom_secant) < HR_EPS) denom_secant = denom_secant >= 0 ? denom_secant + HR_EPS : denom_secant - HR_EPS;
        double xS = fp - (delta * ffp) / denom_secant;

        if (xS > a && xS < b) {
            double fxS = f(xS);
            nfe++;
            if (std::abs(fxS) < std::abs(ffp)) {
                if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                if (std::abs(fxS) <= tol) return {xS, n, nfe, true};
            }
        }
    }
    double final_x = 0.5 * (a + b);
    bool converged = std::abs(f(final_x)) <= tol;
    return {final_x, max_iter, nfe + 1, converged};
}

} // namespace hybridroots
