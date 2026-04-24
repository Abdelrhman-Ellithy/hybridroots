package com.hybridroots;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

class BenchmarkDef {
    String name;
    Function<Double, Double> func;
    double a, b;
    String desc;

    public BenchmarkDef(String name, Function<Double, Double> func, double a, double b, String desc) {
        this.name = name;
        this.func = func;
        this.a = a;
        this.b = b;
        this.desc = desc;
    }
}

interface AlgType {
    HybridRootsResult run(Function<Double, Double> f, double a, double b, double tol, int maxIter);
}

public class Benchmarks {
    public static void main(String[] args) {
        List<BenchmarkDef> benchmarks = new ArrayList<>();
        benchmarks.add(new BenchmarkDef("f1", x -> x * Math.exp(x) - 7.0, 1.0, 2.0, "x*exp(x) - 7"));
        benchmarks.add(new BenchmarkDef("f2", x -> Math.pow(x, 3.0) - x - 1.0, 1.0, 2.0, "x^3 - x - 1"));
        benchmarks.add(new BenchmarkDef("f3", x -> Math.pow(x, 2.0) - x - 2.0, 1.0, 4.0, "x^2 - x - 2"));
        benchmarks.add(new BenchmarkDef("f4", x -> x - Math.cos(x), 0.0, 1.0, "x - cos(x)"));
        benchmarks.add(new BenchmarkDef("f5", x -> Math.pow(x, 2.0) - 10.0, 3.0, 4.0, "x^2 - 10"));
        benchmarks.add(new BenchmarkDef("f6", x -> Math.sin(x) - Math.pow(x, 2.0), 0.5, 1.0, "sin(x) - x^2"));
        benchmarks.add(new BenchmarkDef("f7", x -> x + Math.log(x), 0.1, 1.0, "x + ln(x)"));
        benchmarks.add(new BenchmarkDef("f8", x -> Math.exp(x) - 3.0*x - 2.0, 2.0, 3.0, "exp(x) - 3x - 2"));
        benchmarks.add(new BenchmarkDef("f9", x -> Math.pow(x, 2.0) + Math.exp(x/2.0) - 5.0, 1.0, 2.0, "x^2 + exp(x/2) - 5"));
        benchmarks.add(new BenchmarkDef("f10", x -> x * Math.sin(x) - 1.0, 0.0, 2.0, "x*sin(x) - 1"));
        benchmarks.add(new BenchmarkDef("f11", x -> x * Math.cos(x) + 1.0, -2.0, 4.0, "x*cos(x) + 1"));
        benchmarks.add(new BenchmarkDef("f12", x -> Math.pow(x, 10.0) - 1.0, 0.0, 1.3, "x^10 - 1"));
        benchmarks.add(new BenchmarkDef("f13", x -> Math.pow(x, 2.0) + 2.0*x - 7.0, 1.0, 3.0, "x^2 + 2x - 7"));
        benchmarks.add(new BenchmarkDef("f14", x -> Math.pow(x, 3.0) - 2.0*x - 5.0, 2.0, 3.0, "x^3 - 2x - 5"));
        benchmarks.add(new BenchmarkDef("f15", x -> Math.exp(x) - 3.0*Math.pow(x, 2.0), 0.0, 1.0, "exp(x) - 3x^2"));
        benchmarks.add(new BenchmarkDef("f16", x -> Math.sin(10.0*x) - 0.5*x, 0.1, 0.4, "sin(10x) - 0.5x"));
        benchmarks.add(new BenchmarkDef("f17", x -> x - 0.8*Math.sin(x) - 1.2, 1.0, 3.0, "x - 0.8*sin(x) - 1.2"));
        benchmarks.add(new BenchmarkDef("f18", x -> Math.pow(x, 2.0) - Math.exp(x) - 3.0*x + 2.0, 0.0, 1.0, "x^2 - exp(x) - 3x + 2"));
        benchmarks.add(new BenchmarkDef("f19", x -> Math.pow(x - 1.0, 3.0) + 4.0*Math.pow(x - 1.0, 2.0) - 10.0, 0.0, 3.0, "(x-1)^3 + 4(x-1)^2 - 10"));
        benchmarks.add(new BenchmarkDef("f20", x -> Math.exp(Math.pow(x, 2.0)) - Math.exp(Math.sqrt(2.0)*x), 0.5, 1.5, "exp(x^2) - exp(sqrt(2)*x)"));
        benchmarks.add(new BenchmarkDef("f21", x -> (Math.pow(x, 2.0) - 4.0)*(x + 1.5)*(x - 0.5), 0.0, 2.0, "(x^2-4)(x+1.5)(x-0.5)"));
        benchmarks.add(new BenchmarkDef("f22", x -> Math.pow(x, 3.0) - 3.0*Math.pow(x, 2.0) - 4.0*x + 13.0, -3.0, -2.0, "x^3 - 3x^2 - 4x + 13"));
        benchmarks.add(new BenchmarkDef("f23", x -> -0.9*Math.pow(x, 2.0) + 1.7*x + 2.5, 2.8, 3.0, "-0.9x^2 + 1.7x + 2.5"));
        benchmarks.add(new BenchmarkDef("f24", x -> 1.0 - 0.61*x, 1.5, 2.0, "1 - 0.61x (linear)"));
        benchmarks.add(new BenchmarkDef("f25", x -> Math.pow(x, 2.0) * Math.abs(Math.sin(x)) - 4.1, 0.0, 4.0, "x^2*|sin(x)| - 4.1"));
        benchmarks.add(new BenchmarkDef("f26", x -> Math.pow(x, 5.0) - 3.0*Math.pow(x, 4.0) + 25.0, -3.0, -1.0, "x^5 - 3x^4 + 25"));
        benchmarks.add(new BenchmarkDef("f27", x -> Math.pow(x, 4.0) - 2.0*Math.pow(x, 2.0) - 4.0, 1.0, 3.0, "x^4 - 2x^2 - 4"));
        benchmarks.add(new BenchmarkDef("f28", x -> x - 0.5*Math.sin(x) - 1.0, 0.0, 3.0, "x - 0.5*sin(x) - 1"));
        benchmarks.add(new BenchmarkDef("f29", x -> Math.exp(-x) - Math.cos(3.0*x) - 0.5, 0.0, 1.0, "exp(-x) - cos(3x) - 0.5"));
        benchmarks.add(new BenchmarkDef("f30", x -> (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), 0.0, 1.5, "Wilkinson-like deg-20 polynomial"));
        benchmarks.add(new BenchmarkDef("f31", x -> (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), 19.0, 21.0, "Wilkinson-like deg-20 at root 20"));
        benchmarks.add(new BenchmarkDef("f32", x -> Math.pow(x, 4.0) + 2.0*Math.pow(x, 2.0) - x - 1.0, -0.5, 0.0, "x^4 + 2x^2 - x - 1"));
        benchmarks.add(new BenchmarkDef("f33", x -> Math.pow(x, 4.0) - 10.0*Math.pow(x, 3.0) + 35.0*Math.pow(x, 2.0) - 50.0*x + 24.0, 0.0, 1.5, "x^4 - 10x^3 + 35x^2 - 50x + 24"));
        benchmarks.add(new BenchmarkDef("f34", x -> 4.0*Math.sin(x) - x + 1.0, -1.0, 0.0, "4sin(x) - x + 1"));
        benchmarks.add(new BenchmarkDef("f35", x -> Math.pow(x, 25.0) - 1.0, 0.0, 2.0, "x^25 - 1"));
        benchmarks.add(new BenchmarkDef("f36", x -> Math.pow(x - 1.8, 6.0) * (x - 1.81), 0.0, 2.0, "(x-1.8)^6*(x-1.81) - near multiple root"));
        benchmarks.add(new BenchmarkDef("f37", x -> Math.sin(20.0*x) - 0.3*x, 0.05, 0.25, "sin(20x) - 0.3x"));
        benchmarks.add(new BenchmarkDef("f38", x -> Math.pow(x, 4.0) + 2.0*Math.pow(x, 3.0) - 13.0*Math.pow(x, 2.0) - 14.0*x + 24.0, -3.0, 1.0, "x^4 + 2x^3 - 13x^2 - 14x + 24"));
        benchmarks.add(new BenchmarkDef("f39", x -> Math.exp(Math.pow(x, 2.0)) - Math.exp(1.2*x), 0.0, 2.0, "exp(x^2) - exp(1.2x)"));
        benchmarks.add(new BenchmarkDef("f40", x -> Math.pow(x, 5.0) - 3.0*Math.pow(x, 4.0) + 2.0*Math.pow(x, 3.0) - x + 0.1, -1.0, 3.0, "x^5 - 3x^4 + 2x^3 - x + 0.1"));
        benchmarks.add(new BenchmarkDef("f41", x -> Math.pow(x + 0.3, 7.0) - 0.01, -2.0, 1.0, "(x+0.3)^7 - 0.01"));
        benchmarks.add(new BenchmarkDef("f42", x -> Math.pow(x, 6.0) - 8.0*Math.pow(x, 5.0) + 24.0*Math.pow(x, 4.0) - 32.0*Math.pow(x, 3.0) + 16.0*Math.pow(x, 2.0), 0.0, 4.0, "x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2"));
        benchmarks.add(new BenchmarkDef("f43", x -> -2.0*Math.log10(0.000027027 + 2.51/(10000000.0*Math.sqrt(x))) - 1.0/Math.sqrt(x), 0.008, 0.03, "Colebrook-White friction factor"));
        benchmarks.add(new BenchmarkDef("f44", x -> x - 0.99*Math.sin(x) - 2.0, 2.0, 3.0, "Kepler equation (e=0.99)"));
        benchmarks.add(new BenchmarkDef("f45", x -> (10.0 + 3.592/Math.pow(x, 2.0))*(x - 0.04267) - 0.08206*300.0, 2.0, 3.0, "Van der Waals (CO2)"));
        benchmarks.add(new BenchmarkDef("f46", x -> x*Math.exp(x/2.0) - 1.5, 0.0, 1.0, "x*exp(x/2) - 1.5"));
        benchmarks.add(new BenchmarkDef("f47", x -> Math.cos(x) + 1.0*Math.pow(1.0 - Math.cos(x), 2.0) - 0.05*Math.pow(x, 2.0), 3.0, 6.0, "Beam deflection equation"));
        benchmarks.add(new BenchmarkDef("f48", x -> 0.05 - Math.pow(x, 3.0)/((1.0 - x)*Math.pow(0.8 - 2.0*x, 2.0)), 0.01, 0.3, "Chemical equilibrium"));

        double tol = 1e-14;
        int maxIter = 10000;

        System.out.println("HybridRoots Benchmark Suite - Java Port");
        System.out.println("======================================");

        double[] times = new double[4];
        int[] convs = new int[4];
        double[] iters = new double[4];
        double[] nfes = new double[4];

        AlgType[] funcs = {
            HybridRoots::mpbf, HybridRoots::mpbfms, HybridRoots::mptf, HybridRoots::mptfms
        };
        String[] names = { "mpbf", "mpbfms", "mptf", "mptfms" };

        for (int i = 0; i < benchmarks.size(); i++) {
            BenchmarkDef b = benchmarks.get(i);
            System.out.printf("\n[%2d/48] %s: %s\n", i + 1, b.name, b.desc);

            for (int a = 0; a < 4; a++) {
                funcs[a].run(b.func, b.a, b.b, tol, maxIter); // Warmup

                int runs = 100;
                HybridRootsResult result = null;
                long start = System.nanoTime();
                for (int r = 0; r < runs; r++) {
                    result = funcs[a].run(b.func, b.a, b.b, tol, maxIter);
                }
                long end = System.nanoTime();
                double elapsedUs = (end - start) / 1000.0 / runs;

                if (result.converged) {
                    System.out.printf("       %-8s: root=%.10f, iter=%2d, nfe=%3d\n", names[a], result.root, result.iterations, result.functionCalls);
                    times[a] += elapsedUs;
                    convs[a]++;
                    iters[a] += result.iterations;
                    nfes[a] += result.functionCalls;
                } else {
                    System.out.printf("       %-8s: FAILED\n", names[a]);
                }
            }
        }

        System.out.println("\nSUMMARY");
        System.out.println("======================================");
        System.out.println("Algorithm  | Converged  | Total Time (us)    | Avg NFE    | Avg Iterations");
        System.out.println("--------------------------------------------------------------------------------");
        for (int a = 0; a < 4; a++) {
            System.out.printf("%-10s | %2d/%-7d | %18.2f | %10.2f | %15.2f\n", names[a], convs[a], benchmarks.size(), times[a], nfes[a] / convs[a], iters[a] / convs[a]);
        }
    }
}
