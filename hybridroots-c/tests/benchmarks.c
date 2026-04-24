#include "hybridroots.h"
#include <stdio.h>
#include <math.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
double get_time_us() {
    LARGE_INTEGER freq, val;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&val);
    return (double)val.QuadPart * 1000000.0 / (double)freq.QuadPart;
}
#else
#include <sys/time.h>
double get_time_us() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000000.0 + tv.tv_usec;
}
#endif

typedef double (*FuncPtr)(double);
typedef HybridRootsResult (*AlgorithmPtr)(FuncPtr, double, double, double, int);
typedef struct {
    char name[10];
    FuncPtr func;
    double a;
    double b;
    char desc[100];
} Benchmark;

double func_f1(double x) { return x * exp(x) - 7.0; }
double func_f2(double x) { return pow(x, 3.0) - x - 1.0; }
double func_f3(double x) { return pow(x, 2.0) - x - 2.0; }
double func_f4(double x) { return x - cos(x); }
double func_f5(double x) { return pow(x, 2.0) - 10.0; }
double func_f6(double x) { return sin(x) - pow(x, 2.0); }
double func_f7(double x) { return x + log(x); }
double func_f8(double x) { return exp(x) - 3.0*x - 2.0; }
double func_f9(double x) { return pow(x, 2.0) + exp(x/2.0) - 5.0; }
double func_f10(double x) { return x * sin(x) - 1.0; }
double func_f11(double x) { return x * cos(x) + 1.0; }
double func_f12(double x) { return pow(x, 10.0) - 1.0; }
double func_f13(double x) { return pow(x, 2.0) + 2.0*x - 7.0; }
double func_f14(double x) { return pow(x, 3.0) - 2.0*x - 5.0; }
double func_f15(double x) { return exp(x) - 3.0*pow(x, 2.0); }
double func_f16(double x) { return sin(10.0*x) - 0.5*x; }
double func_f17(double x) { return x - 0.8*sin(x) - 1.2; }
double func_f18(double x) { return pow(x, 2.0) - exp(x) - 3.0*x + 2.0; }
double func_f19(double x) { return pow(x - 1.0, 3.0) + 4.0*pow(x - 1.0, 2.0) - 10.0; }
double func_f20(double x) { return exp(pow(x, 2.0)) - exp(sqrt(2.0)*x); }
double func_f21(double x) { return (pow(x, 2.0) - 4.0)*(x + 1.5)*(x - 0.5); }
double func_f22(double x) { return pow(x, 3.0) - 3.0*pow(x, 2.0) - 4.0*x + 13.0; }
double func_f23(double x) { return -0.9*pow(x, 2.0) + 1.7*x + 2.5; }
double func_f24(double x) { return 1.0 - 0.61*x; }
double func_f25(double x) { return pow(x, 2.0) * fabs(sin(x)) - 4.1; }
double func_f26(double x) { return pow(x, 5.0) - 3.0*pow(x, 4.0) + 25.0; }
double func_f27(double x) { return pow(x, 4.0) - 2.0*pow(x, 2.0) - 4.0; }
double func_f28(double x) { return x - 0.5*sin(x) - 1.0; }
double func_f29(double x) { return exp(-x) - cos(3.0*x) - 0.5; }
double func_f30(double x) { return (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0); }
double func_f31(double x) { return (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0); }
double func_f32(double x) { return pow(x, 4.0) + 2.0*pow(x, 2.0) - x - 1.0; }
double func_f33(double x) { return pow(x, 4.0) - 10.0*pow(x, 3.0) + 35.0*pow(x, 2.0) - 50.0*x + 24.0; }
double func_f34(double x) { return 4.0*sin(x) - x + 1.0; }
double func_f35(double x) { return pow(x, 25.0) - 1.0; }
double func_f36(double x) { return pow(x - 1.8, 6.0) * (x - 1.81); }
double func_f37(double x) { return sin(20.0*x) - 0.3*x; }
double func_f38(double x) { return pow(x, 4.0) + 2.0*pow(x, 3.0) - 13.0*pow(x, 2.0) - 14.0*x + 24.0; }
double func_f39(double x) { return exp(pow(x, 2.0)) - exp(1.2*x); }
double func_f40(double x) { return pow(x, 5.0) - 3.0*pow(x, 4.0) + 2.0*pow(x, 3.0) - x + 0.1; }
double func_f41(double x) { return pow(x + 0.3, 7.0) - 0.01; }
double func_f42(double x) { return pow(x, 6.0) - 8.0*pow(x, 5.0) + 24.0*pow(x, 4.0) - 32.0*pow(x, 3.0) + 16.0*pow(x, 2.0); }
double func_f43(double x) { return -2.0*log10(0.000027027 + 2.51/(10000000.0*sqrt(x))) - 1.0/sqrt(x); }
double func_f44(double x) { return x - 0.99*sin(x) - 2.0; }
double func_f45(double x) { return (10.0 + 3.592/pow(x, 2.0))*(x - 0.04267) - 0.08206*300.0; }
double func_f46(double x) { return x*exp(x/2.0) - 1.5; }
double func_f47(double x) { return cos(x) + 1.0*pow(1.0 - cos(x), 2.0) - 0.05*pow(x, 2.0); }
double func_f48(double x) { return 0.05 - pow(x, 3.0)/((1.0 - x)*pow(0.8 - 2.0*x, 2.0)); }

Benchmark benchmarks[] = {
    {"f1", func_f1, 1.0, 2.0, "x*exp(x) - 7"},
    {"f2", func_f2, 1.0, 2.0, "x^3 - x - 1"},
    {"f3", func_f3, 1.0, 4.0, "x^2 - x - 2"},
    {"f4", func_f4, 0.0, 1.0, "x - cos(x)"},
    {"f5", func_f5, 3.0, 4.0, "x^2 - 10"},
    {"f6", func_f6, 0.5, 1.0, "sin(x) - x^2"},
    {"f7", func_f7, 0.1, 1.0, "x + ln(x)"},
    {"f8", func_f8, 2.0, 3.0, "exp(x) - 3x - 2"},
    {"f9", func_f9, 1.0, 2.0, "x^2 + exp(x/2) - 5"},
    {"f10", func_f10, 0.0, 2.0, "x*sin(x) - 1"},
    {"f11", func_f11, -2.0, 4.0, "x*cos(x) + 1"},
    {"f12", func_f12, 0.0, 1.3, "x^10 - 1"},
    {"f13", func_f13, 1.0, 3.0, "x^2 + 2x - 7"},
    {"f14", func_f14, 2.0, 3.0, "x^3 - 2x - 5"},
    {"f15", func_f15, 0.0, 1.0, "exp(x) - 3x^2"},
    {"f16", func_f16, 0.1, 0.4, "sin(10x) - 0.5x"},
    {"f17", func_f17, 1.0, 3.0, "x - 0.8*sin(x) - 1.2"},
    {"f18", func_f18, 0.0, 1.0, "x^2 - exp(x) - 3x + 2"},
    {"f19", func_f19, 0.0, 3.0, "(x-1)^3 + 4(x-1)^2 - 10"},
    {"f20", func_f20, 0.5, 1.5, "exp(x^2) - exp(sqrt(2)*x)"},
    {"f21", func_f21, 0.0, 2.0, "(x^2-4)(x+1.5)(x-0.5)"},
    {"f22", func_f22, -3.0, -2.0, "x^3 - 3x^2 - 4x + 13"},
    {"f23", func_f23, 2.8, 3.0, "-0.9x^2 + 1.7x + 2.5"},
    {"f24", func_f24, 1.5, 2.0, "1 - 0.61x (linear)"},
    {"f25", func_f25, 0.0, 4.0, "x^2*|sin(x)| - 4.1"},
    {"f26", func_f26, -3.0, -1.0, "x^5 - 3x^4 + 25"},
    {"f27", func_f27, 1.0, 3.0, "x^4 - 2x^2 - 4"},
    {"f28", func_f28, 0.0, 3.0, "x - 0.5*sin(x) - 1"},
    {"f29", func_f29, 0.0, 1.0, "exp(-x) - cos(3x) - 0.5"},
    {"f30", func_f30, 0.0, 1.5, "Wilkinson-like deg-20 polynomial"},
    {"f31", func_f31, 19.0, 21.0, "Wilkinson-like deg-20 at root 20"},
    {"f32", func_f32, -0.5, 0.0, "x^4 + 2x^2 - x - 1"},
    {"f33", func_f33, 0.0, 1.5, "x^4 - 10x^3 + 35x^2 - 50x + 24"},
    {"f34", func_f34, -1.0, 0.0, "4sin(x) - x + 1"},
    {"f35", func_f35, 0.0, 2.0, "x^25 - 1"},
    {"f36", func_f36, 0.0, 2.0, "(x-1.8)^6*(x-1.81) - near multiple root"},
    {"f37", func_f37, 0.05, 0.25, "sin(20x) - 0.3x"},
    {"f38", func_f38, -3.0, 1.0, "x^4 + 2x^3 - 13x^2 - 14x + 24"},
    {"f39", func_f39, 0.0, 2.0, "exp(x^2) - exp(1.2x)"},
    {"f40", func_f40, -1.0, 3.0, "x^5 - 3x^4 + 2x^3 - x + 0.1"},
    {"f41", func_f41, -2.0, 1.0, "(x+0.3)^7 - 0.01"},
    {"f42", func_f42, 0.0, 4.0, "x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2"},
    {"f43", func_f43, 0.008, 0.03, "Colebrook-White friction factor"},
    {"f44", func_f44, 2.0, 3.0, "Kepler equation (e=0.99)"},
    {"f45", func_f45, 2.0, 3.0, "Van der Waals (CO2)"},
    {"f46", func_f46, 0.0, 1.0, "x*exp(x/2) - 1.5"},
    {"f47", func_f47, 3.0, 6.0, "Beam deflection equation"},
    {"f48", func_f48, 0.01, 0.3, "Chemical equilibrium"},
};


int main() {
    int num_benchmarks = sizeof(benchmarks) / sizeof(benchmarks[0]);
    double tol = 1e-14;
    int max_iter = 10000;
    
    printf("HybridRoots Benchmark Suite - C Port\n");
    printf("======================================\n");
    
    // Arrays to store summary
    double time_mpbf = 0, time_mpbfms = 0, time_mptf = 0, time_mptfms = 0;
    int conv_mpbf = 0, conv_mpbfms = 0, conv_mptf = 0, conv_mptfms = 0;
    double iter_mpbf = 0, iter_mpbfms = 0, iter_mptf = 0, iter_mptfms = 0;
    double nfe_mpbf = 0, nfe_mpbfms = 0, nfe_mptf = 0, nfe_mptfms = 0;

    for (int i = 0; i < num_benchmarks; i++) {
        Benchmark b = benchmarks[i];
        printf("\n[%2d/48] %s: %s\n", i+1, b.name, b.desc);
        
        AlgorithmPtr funcs[] = {mpbf, mpbfms, mptf, mptfms};
        char* names[] = {"mpbf", "mpbfms", "mptf", "mptfms"};
        double* times[] = {&time_mpbf, &time_mpbfms, &time_mptf, &time_mptfms};
        int* convs[] = {&conv_mpbf, &conv_mpbfms, &conv_mptf, &conv_mptfms};
        double* iters[] = {&iter_mpbf, &iter_mpbfms, &iter_mptf, &iter_mptfms};
        double* nfes[] = {&nfe_mpbf, &nfe_mpbfms, &nfe_mptf, &nfe_mptfms};
        
        for (int a = 0; a < 4; a++) {
            // Warmup
            funcs[a](b.func, b.a, b.b, tol, max_iter);
            
            int runs = 100;
            HybridRootsResult result;
            double start = get_time_us();
            for (int r = 0; r < runs; r++) {
                result = funcs[a](b.func, b.a, b.b, tol, max_iter);
            }
            double elapsed = (get_time_us() - start) / runs;
            
            if (result.converged) {
                printf("       %-8s: root=%.10f, iter=%2d, nfe=%3d\n", names[a], result.root, result.iterations, result.function_calls);
                *(times[a]) += elapsed;
                *(convs[a]) += 1;
                *(iters[a]) += result.iterations;
                *(nfes[a]) += result.function_calls;
            } else {
                printf("       %-8s: FAILED\n", names[a]);
            }
        }
    }
    
    printf("\nSUMMARY\n");
    printf("======================================\n");
    printf("Algorithm  | Converged  | Total Time (us)    | Avg NFE    | Avg Iterations\n");
    printf("--------------------------------------------------------------------------------\n");
    printf("%-10s | %2d/%-7d | %18.2f | %10.2f | %15.2f\n", "mpbf", conv_mpbf, num_benchmarks, time_mpbf, nfe_mpbf/conv_mpbf, iter_mpbf/conv_mpbf);
    printf("%-10s | %2d/%-7d | %18.2f | %10.2f | %15.2f\n", "mpbfms", conv_mpbfms, num_benchmarks, time_mpbfms, nfe_mpbfms/conv_mpbfms, iter_mpbfms/conv_mpbfms);
    printf("%-10s | %2d/%-7d | %18.2f | %10.2f | %15.2f\n", "mptf", conv_mptf, num_benchmarks, time_mptf, nfe_mptf/conv_mptf, iter_mptf/conv_mptf);
    printf("%-10s | %2d/%-7d | %18.2f | %10.2f | %15.2f\n", "mptfms", conv_mptfms, num_benchmarks, time_mptfms, nfe_mptfms/conv_mptfms, iter_mptfms/conv_mptfms);
    
    return 0;
}
