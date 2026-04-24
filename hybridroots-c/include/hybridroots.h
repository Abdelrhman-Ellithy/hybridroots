#ifndef HYBRIDROOTS_H
#define HYBRIDROOTS_H

typedef struct {
    int iterations;
    int function_calls;
    int converged;
} HybridRootsInfo;

double mpbf(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info);
double mpbfms(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info);
double mptf(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info);
double mptfms(double (*f)(double), double a, double b, double tol, int max_iter, HybridRootsInfo* info);

#endif // HYBRIDROOTS_H
