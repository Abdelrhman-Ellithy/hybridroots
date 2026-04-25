/**
 * @fileoverview HybridRoots – Four Multi-Phase Hybrid Bracketing Algorithms.
 *
 * Implements the algorithms introduced in:
 *   Ellithy, A. (2026). "Four New Multi-Phase Hybrid Bracketing Algorithms for
 *   Numerical Root Finding." Journal of the Egyptian Mathematical Society, 34.
 *   DOI: https://doi.org/10.21608/joems.2026.440115.1078
 *
 * All algorithms are deterministic and guarantee convergence for any continuous
 * function f on a bracket [a, b] where f(a)*f(b) < 0.
 *
 * @author Abdelrahman Ellithy
 * @license Apache-2.0
 * @version 1.0.0
 */

'use strict';

const _EPS = 1e-15;

/**
 * @typedef {Object} HybridRootsResult
 * @property {number}  root          - Estimated root location.
 * @property {number}  iterations    - Number of iterations performed.
 * @property {number}  functionCalls - Number of function evaluations performed.
 * @property {boolean} converged     - True if |f(root)| <= tol.
 */

/**
 * Multi-Phase Bisection–False Position (Opt.BF).
 *
 * Combines classical Bisection with False Position for guaranteed convergence
 * with faster interval reduction.
 * See Section 2 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param {function(number): number} f        - Continuous function f(x).
 * @param {number}                   a        - Left endpoint of the initial bracket.
 * @param {number}                   b        - Right endpoint of the initial bracket.
 * @param {number}                  [tol=1e-14] - Absolute convergence tolerance.
 * @param {number}                  [maxIter=10000] - Maximum iterations.
 * @returns {HybridRootsResult}
 */
export function mpbf(f, a, b, tol = 1e-14, maxIter = 10000) {
    let fa = f(a), fb = f(b);
    let nfe = 2;
    if (Math.abs(fa) <= tol) return { root: a, iterations: 0, functionCalls: nfe, converged: true };
    if (Math.abs(fb) <= tol) return { root: b, iterations: 0, functionCalls: nfe, converged: true };
    if (fa * fb >= 0) return { root: a, iterations: 0, functionCalls: nfe, converged: false };

    for (let n = 1; n <= maxIter; n++) {
        let mid = 0.5 * (a + b);
        let fmid = f(mid);
        nfe++;
        if (Math.abs(fmid) <= tol) return { root: mid, iterations: n, functionCalls: nfe, converged: true };
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

        let denom = fb - fa;
        if (Math.abs(denom) < _EPS) denom = denom >= 0 ? denom + _EPS : denom - _EPS;
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe++;
        if (Math.abs(ffp) <= tol) return { root: fp, iterations: n, functionCalls: nfe, converged: true };
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }

    const finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}

/**
 * Multi-Phase Bisection–False Position–Modified Secant (Opt.BFMS).
 *
 * Extends Opt.BF with an adaptive Modified Secant acceleration step that
 * is accepted only when it reduces the residual and stays in-bracket.
 * See Section 3 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param {function(number): number} f        - Continuous function f(x).
 * @param {number}                   a        - Left endpoint of the initial bracket.
 * @param {number}                   b        - Right endpoint of the initial bracket.
 * @param {number}                  [tol=1e-14] - Absolute convergence tolerance.
 * @param {number}                  [maxIter=10000] - Maximum iterations.
 * @returns {HybridRootsResult}
 */
export function mpbfms(f, a, b, tol = 1e-14, maxIter = 10000) {
    let fa = f(a), fb = f(b);
    let nfe = 2;
    if (Math.abs(fa) <= tol) return { root: a, iterations: 0, functionCalls: nfe, converged: true };
    if (Math.abs(fb) <= tol) return { root: b, iterations: 0, functionCalls: nfe, converged: true };
    if (fa * fb >= 0) return { root: a, iterations: 0, functionCalls: nfe, converged: false };

    for (let n = 1; n <= maxIter; n++) {
        let mid = 0.5 * (a + b);
        let fmid = f(mid);
        nfe++;
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

        let denom = fb - fa;
        if (Math.abs(denom) < _EPS) denom = denom >= 0 ? denom + _EPS : denom - _EPS;
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (Math.abs(ffp) <= tol) return { root: fp, iterations: n, functionCalls: nfe, converged: true };

        let delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + _EPS;
        let fDelta = f(fp + delta);
        nfe++;
        let denomSecant = fDelta - ffp;
        if (Math.abs(denomSecant) < _EPS) denomSecant = denomSecant >= 0 ? denomSecant + _EPS : denomSecant - _EPS;
        let xS = fp - (delta * ffp) / denomSecant;

        if (xS > a && xS < b) {
            let fxS = f(xS);
            nfe++;
            if (Math.abs(fxS) < Math.abs(ffp)) {
                if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                if (Math.abs(fxS) <= tol) return { root: xS, iterations: n, functionCalls: nfe, converged: true };
            }
        }
    }

    const finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}

/**
 * Multi-Phase Trisection–False Position (Opt.TF).
 *
 * Divides the bracket into thirds for faster interval reduction, then applies
 * False Position refinement.
 * See Section 4 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param {function(number): number} f        - Continuous function f(x).
 * @param {number}                   a        - Left endpoint of the initial bracket.
 * @param {number}                   b        - Right endpoint of the initial bracket.
 * @param {number}                  [tol=1e-14] - Absolute convergence tolerance.
 * @param {number}                  [maxIter=10000] - Maximum iterations.
 * @returns {HybridRootsResult}
 */
export function mptf(f, a, b, tol = 1e-14, maxIter = 10000) {
    let fa = f(a), fb = f(b);
    let nfe = 2;
    if (Math.abs(fa) <= tol) return { root: a, iterations: 0, functionCalls: nfe, converged: true };
    if (Math.abs(fb) <= tol) return { root: b, iterations: 0, functionCalls: nfe, converged: true };
    if (fa * fb >= 0) return { root: a, iterations: 0, functionCalls: nfe, converged: false };

    for (let n = 1; n <= maxIter; n++) {
        let diff = b - a;
        let x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        let fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (Math.abs(fx1) <= tol) return { root: x1, iterations: n, functionCalls: nfe, converged: true };
        if (Math.abs(fx2) <= tol) return { root: x2, iterations: n, functionCalls: nfe, converged: true };

        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }

        let denom = fb - fa;
        if (Math.abs(denom) < _EPS) denom = denom >= 0 ? denom + _EPS : denom - _EPS;
        let x = (a * fb - b * fa) / denom;
        let fx = f(x);
        nfe++;
        if (Math.abs(fx) <= tol) return { root: x, iterations: n, functionCalls: nfe, converged: true };
        if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
    }

    const finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}

/**
 * Multi-Phase Trisection–False Position–Modified Secant (Opt.TFMS).
 *
 * Combines Trisection, False Position, and an adaptive Modified Secant step
 * for maximum efficiency. The fastest of the four algorithms for smooth functions.
 * See Section 5 of DOI: 10.21608/joems.2026.440115.1078
 *
 * @param {function(number): number} f        - Continuous function f(x).
 * @param {number}                   a        - Left endpoint of the initial bracket.
 * @param {number}                   b        - Right endpoint of the initial bracket.
 * @param {number}                  [tol=1e-14] - Absolute convergence tolerance.
 * @param {number}                  [maxIter=10000] - Maximum iterations.
 * @returns {HybridRootsResult}
 */
export function mptfms(f, a, b, tol = 1e-14, maxIter = 10000) {
    let fa = f(a), fb = f(b);
    let nfe = 2;
    if (Math.abs(fa) <= tol) return { root: a, iterations: 0, functionCalls: nfe, converged: true };
    if (Math.abs(fb) <= tol) return { root: b, iterations: 0, functionCalls: nfe, converged: true };
    if (fa * fb >= 0) return { root: a, iterations: 0, functionCalls: nfe, converged: false };

    for (let n = 1; n <= maxIter; n++) {
        let diff = b - a;
        let x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        let fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (Math.abs(fx1) <= tol) return { root: x1, iterations: n, functionCalls: nfe, converged: true };
        if (Math.abs(fx2) <= tol) return { root: x2, iterations: n, functionCalls: nfe, converged: true };

        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }

        let denom = fb - fa;
        if (Math.abs(denom) < _EPS) denom = denom >= 0 ? denom + _EPS : denom - _EPS;
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (Math.abs(ffp) <= tol) return { root: fp, iterations: n, functionCalls: nfe, converged: true };

        let delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + _EPS;
        let fDelta = f(fp + delta);
        nfe++;
        let denomSecant = fDelta - ffp;
        if (Math.abs(denomSecant) < _EPS) denomSecant = denomSecant >= 0 ? denomSecant + _EPS : denomSecant - _EPS;
        let xS = fp - (delta * ffp) / denomSecant;

        if (xS > a && xS < b) {
            let fxS = f(xS);
            nfe++;
            if (Math.abs(fxS) < Math.abs(ffp)) {
                if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                if (Math.abs(fxS) <= tol) return { root: xS, iterations: n, functionCalls: nfe, converged: true };
            }
        }
    }

    const finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}
