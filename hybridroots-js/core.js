const EPS = 1e-15;

export function mpbf(f, a, b, tol = 1e-15, maxIter = 10000) {
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
        if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe++;
        if (Math.abs(ffp) <= tol) return { root: fp, iterations: n, functionCalls: nfe, converged: true };
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }

    let finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}

export function mpbfms(f, a, b, tol = 1e-15, maxIter = 10000) {
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
        if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (Math.abs(ffp) <= tol) return { root: fp, iterations: n, functionCalls: nfe, converged: true };

        let delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + EPS;
        let fDelta = f(fp + delta);
        nfe++;
        let denomSecant = fDelta - ffp;
        if (Math.abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
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

    let finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}

export function mptf(f, a, b, tol = 1e-15, maxIter = 10000) {
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
        if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
        let x = (a * fb - b * fa) / denom;
        let fx = f(x);
        nfe++;
        if (Math.abs(fx) <= tol) return { root: x, iterations: n, functionCalls: nfe, converged: true };
        if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
    }

    let finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}

export function mptfms(f, a, b, tol = 1e-15, maxIter = 10000) {
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
        if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
        let fp = (a * fb - b * fa) / denom;
        let ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (Math.abs(ffp) <= tol) return { root: fp, iterations: n, functionCalls: nfe, converged: true };

        let delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + EPS;
        let fDelta = f(fp + delta);
        nfe++;
        let denomSecant = fDelta - ffp;
        if (Math.abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
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

    let finalX = 0.5 * (a + b);
    return { root: finalX, iterations: maxIter, functionCalls: nfe + 1, converged: Math.abs(f(finalX)) <= tol };
}
