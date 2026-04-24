package com.hybridroots;

public class HybridRoots {
    private static final double EPS = 1e-15;

    public static double mpbf(Function f, double a, double b, double tol, int maxIter, HybridRootsInfo info) {
        double fa = f.evaluate(a), fb = f.evaluate(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return a; }
        if (Math.abs(fb) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return b; }
        if (fa * fb >= 0) { info.iterations = 0; info.functionCalls = nfe; info.converged = false; return a; }
        
        for (int n = 1; n <= maxIter; n++) {
            double mid = 0.5 * (a + b);
            double fmid = f.evaluate(mid);
            nfe++;
            if (Math.abs(fmid) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return mid; }
            if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }
            
            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double fp = (a * fb - b * fa) / denom;
            double ffp = f.evaluate(fp);
            nfe++;
            if (Math.abs(ffp) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return fp; }
            if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        }
        info.iterations = maxIter; info.functionCalls = nfe;
        double finalX = 0.5 * (a + b);
        info.converged = Math.abs(f.evaluate(finalX)) <= tol;
        info.functionCalls++;
        return finalX;
    }

    public static double mpbfms(Function f, double a, double b, double tol, int maxIter, HybridRootsInfo info) {
        double fa = f.evaluate(a), fb = f.evaluate(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return a; }
        if (Math.abs(fb) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return b; }
        if (fa * fb >= 0) { info.iterations = 0; info.functionCalls = nfe; info.converged = false; return a; }
        
        for (int n = 1; n <= maxIter; n++) {
            double mid = 0.5 * (a + b);
            double fmid = f.evaluate(mid);
            nfe++;
            if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }
            
            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double fp = (a * fb - b * fa) / denom;
            double ffp = f.evaluate(fp);
            nfe++;
            if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
            if (Math.abs(ffp) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return fp; }
            
            double delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + EPS;
            double fDelta = f.evaluate(fp + delta);
            nfe++;
            double denomSecant = fDelta - ffp;
            if (Math.abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
            double xS = fp - (delta * ffp) / denomSecant;
            
            if (xS > a && xS < b) {
                double fxS = f.evaluate(xS);
                nfe++;
                if (Math.abs(fxS) < Math.abs(ffp)) {
                    if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                    if (Math.abs(fxS) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return xS; }
                }
            }
        }
        info.iterations = maxIter; info.functionCalls = nfe;
        double finalX = 0.5 * (a + b);
        info.converged = Math.abs(f.evaluate(finalX)) <= tol;
        info.functionCalls++;
        return finalX;
    }

    public static double mptf(Function f, double a, double b, double tol, int maxIter, HybridRootsInfo info) {
        double fa = f.evaluate(a), fb = f.evaluate(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return a; }
        if (Math.abs(fb) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return b; }
        if (fa * fb >= 0) { info.iterations = 0; info.functionCalls = nfe; info.converged = false; return a; }
        
        for (int n = 1; n <= maxIter; n++) {
            double diff = b - a;
            double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
            double fx1 = f.evaluate(x1), fx2 = f.evaluate(x2);
            nfe += 2;
            if (Math.abs(fx1) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return x1; }
            if (Math.abs(fx2) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return x2; }
            
            if (fa * fx1 < 0) { b = x1; fb = fx1; }
            else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
            else { a = x2; fa = fx2; }
            
            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double x = (a * fb - b * fa) / denom;
            double fx = f.evaluate(x);
            nfe++;
            if (Math.abs(fx) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return x; }
            if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
        }
        info.iterations = maxIter; info.functionCalls = nfe;
        double finalX = 0.5 * (a + b);
        info.converged = Math.abs(f.evaluate(finalX)) <= tol;
        info.functionCalls++;
        return finalX;
    }

    public static double mptfms(Function f, double a, double b, double tol, int maxIter, HybridRootsInfo info) {
        double fa = f.evaluate(a), fb = f.evaluate(b);
        int nfe = 2;
        if (Math.abs(fa) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return a; }
        if (Math.abs(fb) <= tol) { info.iterations = 0; info.functionCalls = nfe; info.converged = true; return b; }
        if (fa * fb >= 0) { info.iterations = 0; info.functionCalls = nfe; info.converged = false; return a; }
        
        for (int n = 1; n <= maxIter; n++) {
            double diff = b - a;
            double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
            double fx1 = f.evaluate(x1), fx2 = f.evaluate(x2);
            nfe += 2;
            if (Math.abs(fx1) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return x1; }
            if (Math.abs(fx2) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return x2; }
            
            if (fa * fx1 < 0) { b = x1; fb = fx1; }
            else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
            else { a = x2; fa = fx2; }
            
            double denom = fb - fa;
            if (Math.abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
            double fp = (a * fb - b * fa) / denom;
            double ffp = f.evaluate(fp);
            nfe++;
            if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
            if (Math.abs(ffp) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return fp; }
            
            double delta = 1e-8 * Math.max(1.0, Math.abs(fp)) + EPS;
            double fDelta = f.evaluate(fp + delta);
            nfe++;
            double denomSecant = fDelta - ffp;
            if (Math.abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
            double xS = fp - (delta * ffp) / denomSecant;
            
            if (xS > a && xS < b) {
                double fxS = f.evaluate(xS);
                nfe++;
                if (Math.abs(fxS) < Math.abs(ffp)) {
                    if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                    if (Math.abs(fxS) <= tol) { info.iterations = n; info.functionCalls = nfe; info.converged = true; return xS; }
                }
            }
        }
        info.iterations = maxIter; info.functionCalls = nfe;
        double finalX = 0.5 * (a + b);
        info.converged = Math.abs(f.evaluate(finalX)) <= tol;
        info.functionCalls++;
        return finalX;
    }
}
