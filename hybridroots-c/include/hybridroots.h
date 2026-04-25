/**
 * @file hybridroots.h
 * @brief Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding.
 *
 * This C library implements the four novel hybrid root-finding algorithms
 * introduced in:
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
#ifndef HYBRIDROOTS_H
#define HYBRIDROOTS_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Result returned by every HybridRoots algorithm.
 *
 * Mirrors the structure of scipy.optimize.RootResults for cross-language
 * consistency.
 */
typedef struct {
    double root;          /**< Estimated root location.                        */
    int    iterations;    /**< Number of iterations performed.                 */
    int    function_calls;/**< Number of function evaluations performed.       */
    int    converged;     /**< 1 if |f(root)| <= tol, 0 otherwise.            */
} HybridRootsResult;

/**
 * @brief Multi-Phase Bisection–False Position (Opt.BF).
 *
 * Combines classical Bisection with False Position for guaranteed convergence
 * with faster interval reduction.
 * See Section 2 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param f        Pointer to the function f(x).
 * @param a        Left endpoint of the initial bracket (f(a)*f(b) < 0).
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance for convergence.
 * @param max_iter Maximum number of iterations.
 * @return         HybridRootsResult with root, iterations, function_calls, converged.
 */
HybridRootsResult mpbf(double (*f)(double), double a, double b, double tol, int max_iter);

/**
 * @brief Multi-Phase Bisection–False Position–Modified Secant (Opt.BFMS).
 *
 * Extends Opt.BF with an adaptive Modified Secant acceleration step.
 * See Section 3 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param f        Pointer to the function f(x).
 * @param a        Left endpoint of the initial bracket.
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance for convergence.
 * @param max_iter Maximum number of iterations.
 * @return         HybridRootsResult.
 */
HybridRootsResult mpbfms(double (*f)(double), double a, double b, double tol, int max_iter);

/**
 * @brief Multi-Phase Trisection–False Position (Opt.TF).
 *
 * Divides the bracket into thirds for faster interval reduction, then applies
 * False Position refinement.
 * See Section 4 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param f        Pointer to the function f(x).
 * @param a        Left endpoint of the initial bracket.
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance for convergence.
 * @param max_iter Maximum number of iterations.
 * @return         HybridRootsResult.
 */
HybridRootsResult mptf(double (*f)(double), double a, double b, double tol, int max_iter);

/**
 * @brief Multi-Phase Trisection–False Position–Modified Secant (Opt.TFMS).
 *
 * Combines Trisection, False Position, and an adaptive Modified Secant step
 * for maximum efficiency.
 * See Section 5 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param f        Pointer to the function f(x).
 * @param a        Left endpoint of the initial bracket.
 * @param b        Right endpoint of the initial bracket.
 * @param tol      Absolute tolerance for convergence.
 * @param max_iter Maximum number of iterations.
 * @return         HybridRootsResult.
 */
HybridRootsResult mptfms(double (*f)(double), double a, double b, double tol, int max_iter);

#ifdef __cplusplus
}
#endif

#endif /* HYBRIDROOTS_H */
