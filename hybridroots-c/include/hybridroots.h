#ifndef HYBRIDROOTS_H
#define HYBRIDROOTS_H

typedef struct {
    double root;
    int iterations;
    int function_calls;
    int converged;
} HybridRootsResult;

HybridRootsResult mpbf(double (*f)(double), double a, double b, double tol, int max_iter);
HybridRootsResult mpbfms(double (*f)(double), double a, double b, double tol, int max_iter);
HybridRootsResult mptf(double (*f)(double), double a, double b, double tol, int max_iter);
HybridRootsResult mptfms(double (*f)(double), double a, double b, double tol, int max_iter);

#endif // HYBRIDROOTS_H
