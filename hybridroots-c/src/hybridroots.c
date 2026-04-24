#include "hybridroots.h"
#include <math.h>

#define HR_EPS 1e-15

HybridRootsResult mpbf(double (*f)(double), double a, double b, double tol, int max_iter) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) return (HybridRootsResult){a, 0, nfe, 1};
    if (fabs(fb) <= tol) return (HybridRootsResult){b, 0, nfe, 1};
    if (fa * fb >= 0) return (HybridRootsResult){a, 0, nfe, 0};
    
    for (int n = 1; n <= max_iter; n++) {
        double mid = 0.5 * (a + b);
        double fmid = f(mid);
        nfe++;
        if (fabs(fmid) <= tol) return (HybridRootsResult){mid, n, nfe, 1};
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }
        
        double denom = fb - fa;
        if (fabs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fabs(ffp) <= tol) return (HybridRootsResult){fp, n, nfe, 1};
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }
    double final_x = 0.5 * (a + b);
    return (HybridRootsResult){final_x, max_iter, nfe + 1, fabs(f(final_x)) <= tol};
}

HybridRootsResult mpbfms(double (*f)(double), double a, double b, double tol, int max_iter) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) return (HybridRootsResult){a, 0, nfe, 1};
    if (fabs(fb) <= tol) return (HybridRootsResult){b, 0, nfe, 1};
    if (fa * fb >= 0) return (HybridRootsResult){a, 0, nfe, 0};
    
    for (int n = 1; n <= max_iter; n++) {
        double mid = 0.5 * (a + b);
        double fmid = f(mid);
        nfe++;
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }
        
        double denom = fb - fa;
        if (fabs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (fabs(ffp) <= tol) return (HybridRootsResult){fp, n, nfe, 1};
        
        double delta = 1e-8 * fmax(1.0, fabs(fp)) + HR_EPS;
        double f_delta = f(fp + delta);
        nfe++;
        double denom_secant = f_delta - ffp;
        if (fabs(denom_secant) < HR_EPS) denom_secant = denom_secant >= 0 ? denom_secant + HR_EPS : denom_secant - HR_EPS;
        double xS = fp - (delta * ffp) / denom_secant;
        
        if (xS > a && xS < b) {
            double fxS = f(xS);
            nfe++;
            if (fabs(fxS) < fabs(ffp)) {
                if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                if (fabs(fxS) <= tol) return (HybridRootsResult){xS, n, nfe, 1};
            }
        }
    }
    double final_x = 0.5 * (a + b);
    return (HybridRootsResult){final_x, max_iter, nfe + 1, fabs(f(final_x)) <= tol};
}

HybridRootsResult mptf(double (*f)(double), double a, double b, double tol, int max_iter) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) return (HybridRootsResult){a, 0, nfe, 1};
    if (fabs(fb) <= tol) return (HybridRootsResult){b, 0, nfe, 1};
    if (fa * fb >= 0) return (HybridRootsResult){a, 0, nfe, 0};
    
    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (fabs(fx1) <= tol) return (HybridRootsResult){x1, n, nfe, 1};
        if (fabs(fx2) <= tol) return (HybridRootsResult){x2, n, nfe, 1};
        
        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }
        
        double denom = fb - fa;
        if (fabs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double x = (a * fb - b * fa) / denom;
        double fx = f(x);
        nfe++;
        if (fabs(fx) <= tol) return (HybridRootsResult){x, n, nfe, 1};
        if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
    }
    double final_x = 0.5 * (a + b);
    return (HybridRootsResult){final_x, max_iter, nfe + 1, fabs(f(final_x)) <= tol};
}

HybridRootsResult mptfms(double (*f)(double), double a, double b, double tol, int max_iter) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) return (HybridRootsResult){a, 0, nfe, 1};
    if (fabs(fb) <= tol) return (HybridRootsResult){b, 0, nfe, 1};
    if (fa * fb >= 0) return (HybridRootsResult){a, 0, nfe, 0};
    
    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (fabs(fx1) <= tol) return (HybridRootsResult){x1, n, nfe, 1};
        if (fabs(fx2) <= tol) return (HybridRootsResult){x2, n, nfe, 1};
        
        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }
        
        double denom = fb - fa;
        if (fabs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (fabs(ffp) <= tol) return (HybridRootsResult){fp, n, nfe, 1};
        
        double delta = 1e-8 * fmax(1.0, fabs(fp)) + HR_EPS;
        double f_delta = f(fp + delta);
        nfe++;
        double denom_secant = f_delta - ffp;
        if (fabs(denom_secant) < HR_EPS) denom_secant = denom_secant >= 0 ? denom_secant + HR_EPS : denom_secant - HR_EPS;
        double xS = fp - (delta * ffp) / denom_secant;
        
        if (xS > a && xS < b) {
            double fxS = f(xS);
            nfe++;
            if (fabs(fxS) < fabs(ffp)) {
                if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                if (fabs(fxS) <= tol) return (HybridRootsResult){xS, n, nfe, 1};
            }
        }
    }
    double final_x = 0.5 * (a + b);
    return (HybridRootsResult){final_x, max_iter, nfe + 1, fabs(f(final_x)) <= tol};
}
