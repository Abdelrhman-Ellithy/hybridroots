#include "hybridroots.hpp"
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <chrono>

using namespace hybridroots;
using namespace std;

struct Benchmark {
    string name;
    std::function<double(double)> func;
    double a;
    double b;
    string desc;
};

int main() {
    vector<Benchmark> benchmarks = {
        {"f1", [](double x) { return x * std::exp(x) - 7.0; }, 1.0, 2.0, "x*exp(x) - 7"},
        {"f2", [](double x) { return std::pow(x, 3.0) - x - 1.0; }, 1.0, 2.0, "x^3 - x - 1"},
        {"f3", [](double x) { return std::pow(x, 2.0) - x - 2.0; }, 1.0, 4.0, "x^2 - x - 2"},
        {"f4", [](double x) { return x - std::cos(x); }, 0.0, 1.0, "x - cos(x)"},
        {"f5", [](double x) { return std::pow(x, 2.0) - 10.0; }, 3.0, 4.0, "x^2 - 10"},
        {"f6", [](double x) { return std::sin(x) - std::pow(x, 2.0); }, 0.5, 1.0, "sin(x) - x^2"},
        {"f7", [](double x) { return x + std::log(x); }, 0.1, 1.0, "x + ln(x)"},
        {"f8", [](double x) { return std::exp(x) - 3.0*x - 2.0; }, 2.0, 3.0, "exp(x) - 3x - 2"},
        {"f9", [](double x) { return std::pow(x, 2.0) + std::exp(x/2.0) - 5.0; }, 1.0, 2.0, "x^2 + exp(x/2) - 5"},
        {"f10", [](double x) { return x * std::sin(x) - 1.0; }, 0.0, 2.0, "x*sin(x) - 1"},
        {"f11", [](double x) { return x * std::cos(x) + 1.0; }, -2.0, 4.0, "x*cos(x) + 1"},
        {"f12", [](double x) { return std::pow(x, 10.0) - 1.0; }, 0.0, 1.3, "x^10 - 1"},
        {"f13", [](double x) { return std::pow(x, 2.0) + 2.0*x - 7.0; }, 1.0, 3.0, "x^2 + 2x - 7"},
        {"f14", [](double x) { return std::pow(x, 3.0) - 2.0*x - 5.0; }, 2.0, 3.0, "x^3 - 2x - 5"},
        {"f15", [](double x) { return std::exp(x) - 3.0*std::pow(x, 2.0); }, 0.0, 1.0, "exp(x) - 3x^2"},
        {"f16", [](double x) { return std::sin(10.0*x) - 0.5*x; }, 0.1, 0.4, "sin(10x) - 0.5x"},
        {"f17", [](double x) { return x - 0.8*std::sin(x) - 1.2; }, 1.0, 3.0, "x - 0.8*sin(x) - 1.2"},
        {"f18", [](double x) { return std::pow(x, 2.0) - std::exp(x) - 3.0*x + 2.0; }, 0.0, 1.0, "x^2 - exp(x) - 3x + 2"},
        {"f19", [](double x) { return std::pow(x - 1.0, 3.0) + 4.0*std::pow(x - 1.0, 2.0) - 10.0; }, 0.0, 3.0, "(x-1)^3 + 4(x-1)^2 - 10"},
        {"f20", [](double x) { return std::exp(std::pow(x, 2.0)) - std::exp(std::sqrt(2.0)*x); }, 0.5, 1.5, "exp(x^2) - exp(sqrt(2)*x)"},
        {"f21", [](double x) { return (std::pow(x, 2.0) - 4.0)*(x + 1.5)*(x - 0.5); }, 0.0, 2.0, "(x^2-4)(x+1.5)(x-0.5)"},
        {"f22", [](double x) { return std::pow(x, 3.0) - 3.0*std::pow(x, 2.0) - 4.0*x + 13.0; }, -3.0, -2.0, "x^3 - 3x^2 - 4x + 13"},
        {"f23", [](double x) { return -0.9*std::pow(x, 2.0) + 1.7*x + 2.5; }, 2.8, 3.0, "-0.9x^2 + 1.7x + 2.5"},
        {"f24", [](double x) { return 1.0 - 0.61*x; }, 1.5, 2.0, "1 - 0.61x (linear)"},
        {"f25", [](double x) { return std::pow(x, 2.0) * std::abs(std::sin(x)) - 4.1; }, 0.0, 4.0, "x^2*|sin(x)| - 4.1"},
        {"f26", [](double x) { return std::pow(x, 5.0) - 3.0*std::pow(x, 4.0) + 25.0; }, -3.0, -1.0, "x^5 - 3x^4 + 25"},
        {"f27", [](double x) { return std::pow(x, 4.0) - 2.0*std::pow(x, 2.0) - 4.0; }, 1.0, 3.0, "x^4 - 2x^2 - 4"},
        {"f28", [](double x) { return x - 0.5*std::sin(x) - 1.0; }, 0.0, 3.0, "x - 0.5*sin(x) - 1"},
        {"f29", [](double x) { return std::exp(-x) - std::cos(3.0*x) - 0.5; }, 0.0, 1.0, "exp(-x) - cos(3x) - 0.5"},
        {"f30", [](double x) { return (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0); }, 0.0, 1.5, "Wilkinson-like deg-20 polynomial"},
        {"f31", [](double x) { return (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0); }, 19.0, 21.0, "Wilkinson-like deg-20 at root 20"},
        {"f32", [](double x) { return std::pow(x, 4.0) + 2.0*std::pow(x, 2.0) - x - 1.0; }, -0.5, 0.0, "x^4 + 2x^2 - x - 1"},
        {"f33", [](double x) { return std::pow(x, 4.0) - 10.0*std::pow(x, 3.0) + 35.0*std::pow(x, 2.0) - 50.0*x + 24.0; }, 0.0, 1.5, "x^4 - 10x^3 + 35x^2 - 50x + 24"},
        {"f34", [](double x) { return 4.0*std::sin(x) - x + 1.0; }, -1.0, 0.0, "4sin(x) - x + 1"},
        {"f35", [](double x) { return std::pow(x, 25.0) - 1.0; }, 0.0, 2.0, "x^25 - 1"},
        {"f36", [](double x) { return std::pow(x - 1.8, 6.0) * (x - 1.81); }, 0.0, 2.0, "(x-1.8)^6*(x-1.81) - near multiple root"},
        {"f37", [](double x) { return std::sin(20.0*x) - 0.3*x; }, 0.05, 0.25, "sin(20x) - 0.3x"},
        {"f38", [](double x) { return std::pow(x, 4.0) + 2.0*std::pow(x, 3.0) - 13.0*std::pow(x, 2.0) - 14.0*x + 24.0; }, -3.0, 1.0, "x^4 + 2x^3 - 13x^2 - 14x + 24"},
        {"f39", [](double x) { return std::exp(std::pow(x, 2.0)) - std::exp(1.2*x); }, 0.0, 2.0, "exp(x^2) - exp(1.2x)"},
        {"f40", [](double x) { return std::pow(x, 5.0) - 3.0*std::pow(x, 4.0) + 2.0*std::pow(x, 3.0) - x + 0.1; }, -1.0, 3.0, "x^5 - 3x^4 + 2x^3 - x + 0.1"},
        {"f41", [](double x) { return std::pow(x + 0.3, 7.0) - 0.01; }, -2.0, 1.0, "(x+0.3)^7 - 0.01"},
        {"f42", [](double x) { return std::pow(x, 6.0) - 8.0*std::pow(x, 5.0) + 24.0*std::pow(x, 4.0) - 32.0*std::pow(x, 3.0) + 16.0*std::pow(x, 2.0); }, 0.0, 4.0, "x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2"},
        {"f43", [](double x) { return -2.0*std::log10(0.000027027 + 2.51/(10000000.0*std::sqrt(x))) - 1.0/std::sqrt(x); }, 0.008, 0.03, "Colebrook-White friction factor"},
        {"f44", [](double x) { return x - 0.99*std::sin(x) - 2.0; }, 2.0, 3.0, "Kepler equation (e=0.99)"},
        {"f45", [](double x) { return (10.0 + 3.592/std::pow(x, 2.0))*(x - 0.04267) - 0.08206*300.0; }, 2.0, 3.0, "Van der Waals (CO2)"},
        {"f46", [](double x) { return x*std::exp(x/2.0) - 1.5; }, 0.0, 1.0, "x*exp(x/2) - 1.5"},
        {"f47", [](double x) { return std::cos(x) + 1.0*std::pow(1.0 - std::cos(x), 2.0) - 0.05*std::pow(x, 2.0); }, 3.0, 6.0, "Beam deflection equation"},
        {"f48", [](double x) { return 0.05 - std::pow(x, 3.0)/((1.0 - x)*std::pow(0.8 - 2.0*x, 2.0)); }, 0.01, 0.3, "Chemical equilibrium"},
    };

    double tol = 1e-14;
    int max_iter = 10000;
    
    cout << "HybridRoots Benchmark Suite - C++ Port\n";
    cout << "======================================\n";
    
    double time_mpbf = 0, time_mpbfms = 0, time_mptf = 0, time_mptfms = 0;
    int conv_mpbf = 0, conv_mpbfms = 0, conv_mptf = 0, conv_mptfms = 0;
    double iter_mpbf = 0, iter_mpbfms = 0, iter_mptf = 0, iter_mptfms = 0;
    double nfe_mpbf = 0, nfe_mpbfms = 0, nfe_mptf = 0, nfe_mptfms = 0;

    vector<std::function<double(const std::function<double(double)>&, double, double, double, int, HybridRootsInfo&)>> funcs = {
        mpbf, mpbfms, mptf, mptfms
    };
    vector<string> names = {"mpbf", "mpbfms", "mptf", "mptfms"};
    vector<double*> times = {&time_mpbf, &time_mpbfms, &time_mptf, &time_mptfms};
    vector<int*> convs = {&conv_mpbf, &conv_mpbfms, &conv_mptf, &conv_mptfms};
    vector<double*> iters = {&iter_mpbf, &iter_mpbfms, &iter_mptf, &iter_mptfms};
    vector<double*> nfes = {&nfe_mpbf, &nfe_mpbfms, &nfe_mptf, &nfe_mptfms};

    for (size_t i = 0; i < benchmarks.size(); i++) {
        auto& b = benchmarks[i];
        printf("\n[%2zu/48] %s: %s\n", i+1, b.name.c_str(), b.desc.c_str());
        
        for (int a = 0; a < 4; a++) {
            HybridRootsInfo info;
            funcs[a](b.func, b.a, b.b, tol, max_iter, info); // Warmup
            
            int runs = 100;
            double root;
            auto start = chrono::high_resolution_clock::now();
            for (int r = 0; r < runs; r++) {
                root = funcs[a](b.func, b.a, b.b, tol, max_iter, info);
            }
            auto end = chrono::high_resolution_clock::now();
            double elapsed = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0 / runs;
            
            if (info.converged) {
                printf("       %-8s: root=%.10f, iter=%2d, nfe=%3d\n", names[a].c_str(), root, info.iterations, info.function_calls);
                *(times[a]) += elapsed;
                *(convs[a]) += 1;
                *(iters[a]) += info.iterations;
                *(nfes[a]) += info.function_calls;
            } else {
                printf("       %-8s: FAILED\n", names[a].c_str());
            }
        }
    }
    
    printf("\nSUMMARY\n");
    printf("======================================\n");
    printf("Algorithm  | Converged  | Total Time (us)    | Avg NFE    | Avg Iterations\n");
    printf("--------------------------------------------------------------------------------\n");
    printf("%-10s | %2d/%-7zu | %18.2f | %10.2f | %15.2f\n", "mpbf", conv_mpbf, benchmarks.size(), time_mpbf, nfe_mpbf/conv_mpbf, iter_mpbf/conv_mpbf);
    printf("%-10s | %2d/%-7zu | %18.2f | %10.2f | %15.2f\n", "mpbfms", conv_mpbfms, benchmarks.size(), time_mpbfms, nfe_mpbfms/conv_mpbfms, iter_mpbfms/conv_mpbfms);
    printf("%-10s | %2d/%-7zu | %18.2f | %10.2f | %15.2f\n", "mptf", conv_mptf, benchmarks.size(), time_mptf, nfe_mptf/conv_mptf, iter_mptf/conv_mptf);
    printf("%-10s | %2d/%-7zu | %18.2f | %10.2f | %15.2f\n", "mptfms", conv_mptfms, benchmarks.size(), time_mptfms, nfe_mptfms/conv_mptfms, iter_mptfms/conv_mptfms);
    
    return 0;
}
