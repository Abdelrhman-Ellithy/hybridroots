//! # hybridroots
//!
//! Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding.
//!
//! Implements the algorithms introduced in:
//!
//! > Ellithy, A. (2026). *Four New Multi-Phase Hybrid Bracketing Algorithms for
//! > Numerical Root Finding.* Journal of the Egyptian Mathematical Society, 34.
//! > DOI: <https://doi.org/10.21608/joems.2026.440115.1078>
//!
//! All algorithms are deterministic and guarantee convergence for any continuous
//! function `f` on a bracket `[a, b]` where `f(a) * f(b) < 0`.
//!
//! ## Quick Start
//! ```rust
//! use hybridroots::mptfms;
//!
//! let result = mptfms(&|x: f64| x * x - 2.0, 1.0, 2.0, 1e-14, 10000);
//! assert!(result.converged);
//! println!("sqrt(2) ≈ {}", result.root);
//! ```

const EPS: f64 = 1e-15;

/// Result returned by every HybridRoots algorithm.
///
/// Mirrors `scipy.optimize.RootResults` for cross-language consistency.
#[derive(Debug, Clone, PartialEq)]
pub struct HybridRootsResult {
    /// Estimated root location.
    pub root: f64,
    /// Number of iterations performed.
    pub iterations: usize,
    /// Number of function evaluations performed.
    pub function_calls: usize,
    /// `true` if `|f(root)| <= tol`.
    pub converged: bool,
}

/// Multi-Phase Bisection–False Position (Opt.BF).
///
/// Combines classical Bisection with False Position for guaranteed convergence
/// with faster interval reduction.
/// See Section 2 of DOI: 10.21608/joems.2026.440115.1078
///
/// # Arguments
/// * `f`        – Continuous function whose root is sought.
/// * `a`        – Left endpoint of the initial bracket (`f(a) * f(b) < 0`).
/// * `b`        – Right endpoint of the initial bracket.
/// * `tol`      – Absolute tolerance; convergence declared when `|f(x)| <= tol`.
/// * `max_iter` – Maximum number of iterations allowed.
///
/// # Returns
/// [`HybridRootsResult`] with `root`, `iterations`, `function_calls`, and `converged`.
pub fn mpbf<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> HybridRootsResult {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: true }; }
    if fb.abs() <= tol { return HybridRootsResult { root: b, iterations: 0, function_calls: nfe, converged: true }; }
    if fa * fb >= 0.0  { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: false }; }

    for n in 1..=max_iter {
        let mid = 0.5 * (a + b);
        let fmid = f(mid);
        nfe += 1;
        if fmid.abs() <= tol { return HybridRootsResult { root: mid, iterations: n, function_calls: nfe, converged: true }; }
        if fa * fmid < 0.0 { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

        let mut denom = fb - fa;
        if denom.abs() < EPS { denom = if denom >= 0.0 { denom + EPS } else { denom - EPS }; }
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe += 1;
        if ffp.abs() <= tol { return HybridRootsResult { root: fp, iterations: n, function_calls: nfe, converged: true }; }
        if fa * ffp < 0.0 { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }

    let final_x = 0.5 * (a + b);
    let fv = f(final_x);
    HybridRootsResult { root: final_x, iterations: max_iter, function_calls: nfe + 1, converged: fv.abs() <= tol }
}

/// Multi-Phase Bisection–False Position–Modified Secant (Opt.BFMS).
///
/// Extends Opt.BF with an adaptive Modified Secant acceleration step that
/// is accepted only when it reduces the residual and stays in-bracket.
/// See Section 3 of DOI: 10.21608/joems.2026.440115.1078
///
/// # Arguments
/// * `f`        – Continuous function whose root is sought.
/// * `a`        – Left endpoint of the initial bracket.
/// * `b`        – Right endpoint of the initial bracket.
/// * `tol`      – Absolute tolerance.
/// * `max_iter` – Maximum number of iterations.
///
/// # Returns
/// [`HybridRootsResult`].
pub fn mpbfms<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> HybridRootsResult {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: true }; }
    if fb.abs() <= tol { return HybridRootsResult { root: b, iterations: 0, function_calls: nfe, converged: true }; }
    if fa * fb >= 0.0  { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: false }; }

    for n in 1..=max_iter {
        let mid = 0.5 * (a + b);
        let fmid = f(mid);
        nfe += 1;
        if fa * fmid < 0.0 { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

        let mut denom = fb - fa;
        if denom.abs() < EPS { denom = if denom >= 0.0 { denom + EPS } else { denom - EPS }; }
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe += 1;
        if fa * ffp < 0.0 { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if ffp.abs() <= tol { return HybridRootsResult { root: fp, iterations: n, function_calls: nfe, converged: true }; }

        let delta = 1e-8 * 1.0_f64.max(fp.abs()) + EPS;
        let f_delta = f(fp + delta);
        nfe += 1;
        let mut denom_secant = f_delta - ffp;
        if denom_secant.abs() < EPS { denom_secant = if denom_secant >= 0.0 { denom_secant + EPS } else { denom_secant - EPS }; }
        let xs = fp - (delta * ffp) / denom_secant;

        if xs > a && xs < b {
            let fxs = f(xs);
            nfe += 1;
            if fxs.abs() < ffp.abs() {
                if fa * fxs < 0.0 { b = xs; fb = fxs; } else { a = xs; fa = fxs; }
                if fxs.abs() <= tol { return HybridRootsResult { root: xs, iterations: n, function_calls: nfe, converged: true }; }
            }
        }
    }

    let final_x = 0.5 * (a + b);
    let fv = f(final_x);
    HybridRootsResult { root: final_x, iterations: max_iter, function_calls: nfe + 1, converged: fv.abs() <= tol }
}

/// Multi-Phase Trisection–False Position (Opt.TF).
///
/// Divides the bracket into thirds for faster interval reduction, then applies
/// False Position refinement.
/// See Section 4 of DOI: 10.21608/joems.2026.440115.1078
///
/// # Arguments
/// * `f`        – Continuous function whose root is sought.
/// * `a`        – Left endpoint of the initial bracket.
/// * `b`        – Right endpoint of the initial bracket.
/// * `tol`      – Absolute tolerance.
/// * `max_iter` – Maximum number of iterations.
///
/// # Returns
/// [`HybridRootsResult`].
pub fn mptf<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> HybridRootsResult {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: true }; }
    if fb.abs() <= tol { return HybridRootsResult { root: b, iterations: 0, function_calls: nfe, converged: true }; }
    if fa * fb >= 0.0  { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: false }; }

    for n in 1..=max_iter {
        let diff = b - a;
        let x1 = a + diff / 3.0;
        let x2 = b - diff / 3.0;
        let fx1 = f(x1);
        let fx2 = f(x2);
        nfe += 2;

        if fx1.abs() <= tol { return HybridRootsResult { root: x1, iterations: n, function_calls: nfe, converged: true }; }
        if fx2.abs() <= tol { return HybridRootsResult { root: x2, iterations: n, function_calls: nfe, converged: true }; }

        if fa * fx1 < 0.0       { b = x1; fb = fx1; }
        else if fx1 * fx2 < 0.0 { a = x1; b = x2; fa = fx1; fb = fx2; }
        else                     { a = x2; fa = fx2; }

        let mut denom = fb - fa;
        if denom.abs() < EPS { denom = if denom >= 0.0 { denom + EPS } else { denom - EPS }; }
        let x = (a * fb - b * fa) / denom;
        let fx = f(x);
        nfe += 1;
        if fx.abs() <= tol { return HybridRootsResult { root: x, iterations: n, function_calls: nfe, converged: true }; }
        if fa * fx < 0.0 { b = x; fb = fx; } else { a = x; fa = fx; }
    }

    let final_x = 0.5 * (a + b);
    let fv = f(final_x);
    HybridRootsResult { root: final_x, iterations: max_iter, function_calls: nfe + 1, converged: fv.abs() <= tol }
}

/// Multi-Phase Trisection–False Position–Modified Secant (Opt.TFMS).
///
/// Combines Trisection, False Position, and an adaptive Modified Secant step
/// for maximum efficiency. The fastest of the four algorithms for smooth functions.
/// See Section 5 of DOI: 10.21608/joems.2026.440115.1078
///
/// # Arguments
/// * `f`        – Continuous function whose root is sought.
/// * `a`        – Left endpoint of the initial bracket.
/// * `b`        – Right endpoint of the initial bracket.
/// * `tol`      – Absolute tolerance.
/// * `max_iter` – Maximum number of iterations.
///
/// # Returns
/// [`HybridRootsResult`].
pub fn mptfms<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> HybridRootsResult {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: true }; }
    if fb.abs() <= tol { return HybridRootsResult { root: b, iterations: 0, function_calls: nfe, converged: true }; }
    if fa * fb >= 0.0  { return HybridRootsResult { root: a, iterations: 0, function_calls: nfe, converged: false }; }

    for n in 1..=max_iter {
        let diff = b - a;
        let x1 = a + diff / 3.0;
        let x2 = b - diff / 3.0;
        let fx1 = f(x1);
        let fx2 = f(x2);
        nfe += 2;

        if fx1.abs() <= tol { return HybridRootsResult { root: x1, iterations: n, function_calls: nfe, converged: true }; }
        if fx2.abs() <= tol { return HybridRootsResult { root: x2, iterations: n, function_calls: nfe, converged: true }; }

        if fa * fx1 < 0.0       { b = x1; fb = fx1; }
        else if fx1 * fx2 < 0.0 { a = x1; b = x2; fa = fx1; fb = fx2; }
        else                     { a = x2; fa = fx2; }

        let mut denom = fb - fa;
        if denom.abs() < EPS { denom = if denom >= 0.0 { denom + EPS } else { denom - EPS }; }
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe += 1;
        if fa * ffp < 0.0 { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if ffp.abs() <= tol { return HybridRootsResult { root: fp, iterations: n, function_calls: nfe, converged: true }; }

        let delta = 1e-8 * 1.0_f64.max(fp.abs()) + EPS;
        let f_delta = f(fp + delta);
        nfe += 1;
        let mut denom_secant = f_delta - ffp;
        if denom_secant.abs() < EPS { denom_secant = if denom_secant >= 0.0 { denom_secant + EPS } else { denom_secant - EPS }; }
        let xs = fp - (delta * ffp) / denom_secant;

        if xs > a && xs < b {
            let fxs = f(xs);
            nfe += 1;
            if fxs.abs() < ffp.abs() {
                if fa * fxs < 0.0 { b = xs; fb = fxs; } else { a = xs; fa = fxs; }
                if fxs.abs() <= tol { return HybridRootsResult { root: xs, iterations: n, function_calls: nfe, converged: true }; }
            }
        }
    }

    let final_x = 0.5 * (a + b);
    let fv = f(final_x);
    HybridRootsResult { root: final_x, iterations: max_iter, function_calls: nfe + 1, converged: fv.abs() <= tol }
}
