#include "hybridroots.h"
#include <math.h>

#define HR_EPS 1e-15

double mpbf(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return a; }
    if (fabs(fb) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return b; }
    if (fa * fb >= 0) { info->iterations = 0; info->function_calls = nfe; info->converged = 0; return a; }
    
    for (int n = 1; n <= max_iter; n++) {
        double mid = 0.5 * (a + b);
        double fmid = f(mid);
        nfe++;
        if (fabs(fmid) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return mid; }
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }
        
        double denom = fb - fa;
        if (fabs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fabs(ffp) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return fp; }
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }
    info->iterations = max_iter; info->function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info->converged = fabs(f(final_x)) <= tol;
    info->function_calls++;
    return final_x;
}

double mpbfms(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return a; }
    if (fabs(fb) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return b; }
    if (fa * fb >= 0) { info->iterations = 0; info->function_calls = nfe; info->converged = 0; return a; }
    
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
        if (fabs(ffp) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return fp; }
        
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
                if (fabs(fxS) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return xS; }
            }
        }
    }
    info->iterations = max_iter; info->function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info->converged = fabs(f(final_x)) <= tol;
    info->function_calls++;
    return final_x;
}

double mptf(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return a; }
    if (fabs(fb) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return b; }
    if (fa * fb >= 0) { info->iterations = 0; info->function_calls = nfe; info->converged = 0; return a; }
    
    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (fabs(fx1) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return x1; }
        if (fabs(fx2) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return x2; }
        
        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }
        
        double denom = fb - fa;
        if (fabs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double x = (a * fb - b * fa) / denom;
        double fx = f(x);
        nfe++;
        if (fabs(fx) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return x; }
        if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
    }
    info->iterations = max_iter; info->function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info->converged = fabs(f(final_x)) <= tol;
    info->function_calls++;
    return final_x;
}

double mptfms(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (fabs(fa) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return a; }
    if (fabs(fb) <= tol) { info->iterations = 0; info->function_calls = nfe; info->converged = 1; return b; }
    if (fa * fb >= 0) { info->iterations = 0; info->function_calls = nfe; info->converged = 0; return a; }
    
    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (fabs(fx1) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return x1; }
        if (fabs(fx2) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return x2; }
        
        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }
        
        double denom = fb - fa;
        if (fabs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (fabs(ffp) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return fp; }
        
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
                if (fabs(fxS) <= tol) { info->iterations = n; info->function_calls = nfe; info->converged = 1; return xS; }
            }
        }
    }
    info->iterations = max_iter; info->function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info->converged = fabs(f(final_x)) <= tol;
    info->function_calls++;
    return final_x;
}
