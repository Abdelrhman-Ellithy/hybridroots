#pragma once
#include <cmath>
#include <functional>
#include <algorithm>

namespace hybridroots {

struct HybridRootsInfo {
    int iterations;
    int function_calls;
    bool converged;
};

constexpr double HR_EPS = 1e-15;

inline double mpbf(const std::function<double(double)>& f, double a, double b, double tol, int max_iter, HybridRootsInfo& info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return a; }
    if (std::abs(fb) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return b; }
    if (fa * fb >= 0) { info.iterations = 0; info.function_calls = nfe; info.converged = false; return a; }
    
    for (int n = 1; n <= max_iter; n++) {
        double mid = 0.5 * (a + b);
        double fmid = f(mid);
        nfe++;
        if (std::abs(fmid) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return mid; }
        if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }
        
        double denom = fb - fa;
        if (std::abs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (std::abs(ffp) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return fp; }
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
    }
    info.iterations = max_iter; info.function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info.converged = std::abs(f(final_x)) <= tol;
    info.function_calls++;
    return final_x;
}

inline double mpbfms(const std::function<double(double)>& f, double a, double b, double tol, int max_iter, HybridRootsInfo& info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return a; }
    if (std::abs(fb) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return b; }
    if (fa * fb >= 0) { info.iterations = 0; info.function_calls = nfe; info.converged = false; return a; }
    
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
        if (std::abs(ffp) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return fp; }
        
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
                if (std::abs(fxS) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return xS; }
            }
        }
    }
    info.iterations = max_iter; info.function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info.converged = std::abs(f(final_x)) <= tol;
    info.function_calls++;
    return final_x;
}

inline double mptf(const std::function<double(double)>& f, double a, double b, double tol, int max_iter, HybridRootsInfo& info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return a; }
    if (std::abs(fb) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return b; }
    if (fa * fb >= 0) { info.iterations = 0; info.function_calls = nfe; info.converged = false; return a; }
    
    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (std::abs(fx1) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return x1; }
        if (std::abs(fx2) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return x2; }
        
        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }
        
        double denom = fb - fa;
        if (std::abs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double x = (a * fb - b * fa) / denom;
        double fx = f(x);
        nfe++;
        if (std::abs(fx) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return x; }
        if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
    }
    info.iterations = max_iter; info.function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info.converged = std::abs(f(final_x)) <= tol;
    info.function_calls++;
    return final_x;
}

inline double mptfms(const std::function<double(double)>& f, double a, double b, double tol, int max_iter, HybridRootsInfo& info) {
    double fa = f(a), fb = f(b);
    int nfe = 2;
    if (std::abs(fa) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return a; }
    if (std::abs(fb) <= tol) { info.iterations = 0; info.function_calls = nfe; info.converged = true; return b; }
    if (fa * fb >= 0) { info.iterations = 0; info.function_calls = nfe; info.converged = false; return a; }
    
    for (int n = 1; n <= max_iter; n++) {
        double diff = b - a;
        double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
        double fx1 = f(x1), fx2 = f(x2);
        nfe += 2;
        if (std::abs(fx1) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return x1; }
        if (std::abs(fx2) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return x2; }
        
        if (fa * fx1 < 0) { b = x1; fb = fx1; }
        else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
        else { a = x2; fa = fx2; }
        
        double denom = fb - fa;
        if (std::abs(denom) < HR_EPS) denom = denom >= 0 ? denom + HR_EPS : denom - HR_EPS;
        double fp = (a * fb - b * fa) / denom;
        double ffp = f(fp);
        nfe++;
        if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
        if (std::abs(ffp) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return fp; }
        
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
                if (std::abs(fxS) <= tol) { info.iterations = n; info.function_calls = nfe; info.converged = true; return xS; }
            }
        }
    }
    info.iterations = max_iter; info.function_calls = nfe;
    double final_x = 0.5 * (a + b);
    info.converged = std::abs(f(final_x)) <= tol;
    info.function_calls++;
    return final_x;
}

} // namespace hybridroots
