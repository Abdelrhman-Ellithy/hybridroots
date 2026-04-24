pub struct HybridRootsInfo {
    pub iterations: usize,
    pub function_calls: usize,
    pub converged: bool,
}

const EPS: f64 = 1e-15;

pub fn mpbf<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> (f64, HybridRootsInfo) {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fb.abs() <= tol { return (b, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fa * fb >= 0.0 { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: false }); }

    for n in 1..=max_iter {
        let mid = 0.5 * (a + b);
        let fmid = f(mid);
        nfe += 1;
        if fmid.abs() <= tol { return (mid, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }
        if fa * fmid < 0.0 { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

        let mut denom = fb - fa;
        if denom.abs() < EPS { denom = if denom >= 0.0 { denom + EPS } else { denom - EPS }; }
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe += 1;
        if ffp.abs() <= tol { return (fp, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }
        if fa * ffp < 0.0 { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }

    let final_x = 0.5 * (a + b);
    let converged = f(final_x).abs() <= tol;
    nfe += 1;
    (final_x, HybridRootsInfo { iterations: max_iter, function_calls: nfe, converged })
}

pub fn mpbfms<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> (f64, HybridRootsInfo) {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fb.abs() <= tol { return (b, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fa * fb >= 0.0 { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: false }); }

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
        if ffp.abs() <= tol { return (fp, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }

        let delta = 1e-8 * 1.0f64.max(fp.abs()) + EPS;
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
                if fxs.abs() <= tol { return (xs, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }
            }
        }
    }

    let final_x = 0.5 * (a + b);
    let converged = f(final_x).abs() <= tol;
    nfe += 1;
    (final_x, HybridRootsInfo { iterations: max_iter, function_calls: nfe, converged })
}

pub fn mptf<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> (f64, HybridRootsInfo) {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fb.abs() <= tol { return (b, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fa * fb >= 0.0 { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: false }); }

    for n in 1..=max_iter {
        let diff = b - a;
        let x1 = a + diff / 3.0;
        let x2 = b - diff / 3.0;
        let fx1 = f(x1);
        let fx2 = f(x2);
        nfe += 2;

        if fx1.abs() <= tol { return (x1, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }
        if fx2.abs() <= tol { return (x2, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }

        if fa * fx1 < 0.0 { b = x1; fb = fx1; }
        else if fx1 * fx2 < 0.0 { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }

        let mut denom = fb - fa;
        if denom.abs() < EPS { denom = if denom >= 0.0 { denom + EPS } else { denom - EPS }; }
        let x = (a * fb - b * fa) / denom;
        let fx = f(x);
        nfe += 1;
        if fx.abs() <= tol { return (x, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }
        if fa * fx < 0.0 { b = x; fb = fx; } else { a = x; fa = fx; }
    }

    let final_x = 0.5 * (a + b);
    let converged = f(final_x).abs() <= tol;
    nfe += 1;
    (final_x, HybridRootsInfo { iterations: max_iter, function_calls: nfe, converged })
}

pub fn mptfms<F: Fn(f64) -> f64>(f: &F, mut a: f64, mut b: f64, tol: f64, max_iter: usize) -> (f64, HybridRootsInfo) {
    let mut fa = f(a);
    let mut fb = f(b);
    let mut nfe = 2;

    if fa.abs() <= tol { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fb.abs() <= tol { return (b, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: true }); }
    if fa * fb >= 0.0 { return (a, HybridRootsInfo { iterations: 0, function_calls: nfe, converged: false }); }

    for n in 1..=max_iter {
        let diff = b - a;
        let x1 = a + diff / 3.0;
        let x2 = b - diff / 3.0;
        let fx1 = f(x1);
        let fx2 = f(x2);
        nfe += 2;

        if fx1.abs() <= tol { return (x1, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }
        if fx2.abs() <= tol { return (x2, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }

        if fa * fx1 < 0.0 { b = x1; fb = fx1; }
        else if fx1 * fx2 < 0.0 { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }

        let mut denom = fb - fa;
        if denom.abs() < EPS { denom = if denom >= 0.0 { denom + EPS } else { denom - EPS }; }
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe += 1;
        if fa * ffp < 0.0 { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if ffp.abs() <= tol { return (fp, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }

        let delta = 1e-8 * 1.0f64.max(fp.abs()) + EPS;
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
                if fxs.abs() <= tol { return (xs, HybridRootsInfo { iterations: n, function_calls: nfe, converged: true }); }
            }
        }
    }

    let final_x = 0.5 * (a + b);
    let converged = f(final_x).abs() <= tol;
    nfe += 1;
    (final_x, HybridRootsInfo { iterations: max_iter, function_calls: nfe, converged })
}
