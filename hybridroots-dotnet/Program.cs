using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace HybridRoots
{
    class BenchmarkDef
    {
        public string Name { get; set; }
        public Func<double, double> Func { get; set; }
        public double A { get; set; }
        public double B { get; set; }
        public string Desc { get; set; }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var benchmarks = new List<BenchmarkDef>
            {
                new BenchmarkDef { Name = "f1", Func = x => x * Math.Exp(x) - 7.0, A = 1.0, B = 2.0, Desc = "x*exp(x) - 7" },
                new BenchmarkDef { Name = "f2", Func = x => Math.Pow(x, 3.0) - x - 1.0, A = 1.0, B = 2.0, Desc = "x^3 - x - 1" },
                new BenchmarkDef { Name = "f3", Func = x => Math.Pow(x, 2.0) - x - 2.0, A = 1.0, B = 4.0, Desc = "x^2 - x - 2" },
                new BenchmarkDef { Name = "f4", Func = x => x - Math.Cos(x), A = 0.0, B = 1.0, Desc = "x - cos(x)" },
                new BenchmarkDef { Name = "f5", Func = x => Math.Pow(x, 2.0) - 10.0, A = 3.0, B = 4.0, Desc = "x^2 - 10" },
                new BenchmarkDef { Name = "f6", Func = x => Math.Sin(x) - Math.Pow(x, 2.0), A = 0.5, B = 1.0, Desc = "sin(x) - x^2" },
                new BenchmarkDef { Name = "f7", Func = x => x + Math.Log(x), A = 0.1, B = 1.0, Desc = "x + ln(x)" },
                new BenchmarkDef { Name = "f8", Func = x => Math.Exp(x) - 3.0*x - 2.0, A = 2.0, B = 3.0, Desc = "exp(x) - 3x - 2" },
                new BenchmarkDef { Name = "f9", Func = x => Math.Pow(x, 2.0) + Math.Exp(x/2.0) - 5.0, A = 1.0, B = 2.0, Desc = "x^2 + exp(x/2) - 5" },
                new BenchmarkDef { Name = "f10", Func = x => x * Math.Sin(x) - 1.0, A = 0.0, B = 2.0, Desc = "x*sin(x) - 1" },
                new BenchmarkDef { Name = "f11", Func = x => x * Math.Cos(x) + 1.0, A = -2.0, B = 4.0, Desc = "x*cos(x) + 1" },
                new BenchmarkDef { Name = "f12", Func = x => Math.Pow(x, 10.0) - 1.0, A = 0.0, B = 1.3, Desc = "x^10 - 1" },
                new BenchmarkDef { Name = "f13", Func = x => Math.Pow(x, 2.0) + 2.0*x - 7.0, A = 1.0, B = 3.0, Desc = "x^2 + 2x - 7" },
                new BenchmarkDef { Name = "f14", Func = x => Math.Pow(x, 3.0) - 2.0*x - 5.0, A = 2.0, B = 3.0, Desc = "x^3 - 2x - 5" },
                new BenchmarkDef { Name = "f15", Func = x => Math.Exp(x) - 3.0*Math.Pow(x, 2.0), A = 0.0, B = 1.0, Desc = "exp(x) - 3x^2" },
                new BenchmarkDef { Name = "f16", Func = x => Math.Sin(10.0*x) - 0.5*x, A = 0.1, B = 0.4, Desc = "sin(10x) - 0.5x" },
                new BenchmarkDef { Name = "f17", Func = x => x - 0.8*Math.Sin(x) - 1.2, A = 1.0, B = 3.0, Desc = "x - 0.8*sin(x) - 1.2" },
                new BenchmarkDef { Name = "f18", Func = x => Math.Pow(x, 2.0) - Math.Exp(x) - 3.0*x + 2.0, A = 0.0, B = 1.0, Desc = "x^2 - exp(x) - 3x + 2" },
                new BenchmarkDef { Name = "f19", Func = x => Math.Pow(x - 1.0, 3.0) + 4.0*Math.Pow(x - 1.0, 2.0) - 10.0, A = 0.0, B = 3.0, Desc = "(x-1)^3 + 4(x-1)^2 - 10" },
                new BenchmarkDef { Name = "f20", Func = x => Math.Exp(Math.Pow(x, 2.0)) - Math.Exp(Math.Sqrt(2.0)*x), A = 0.5, B = 1.5, Desc = "exp(x^2) - exp(sqrt(2)*x)" },
                new BenchmarkDef { Name = "f21", Func = x => (Math.Pow(x, 2.0) - 4.0)*(x + 1.5)*(x - 0.5), A = 0.0, B = 2.0, Desc = "(x^2-4)(x+1.5)(x-0.5)" },
                new BenchmarkDef { Name = "f22", Func = x => Math.Pow(x, 3.0) - 3.0*Math.Pow(x, 2.0) - 4.0*x + 13.0, A = -3.0, B = -2.0, Desc = "x^3 - 3x^2 - 4x + 13" },
                new BenchmarkDef { Name = "f23", Func = x => -0.9*Math.Pow(x, 2.0) + 1.7*x + 2.5, A = 2.8, B = 3.0, Desc = "-0.9x^2 + 1.7x + 2.5" },
                new BenchmarkDef { Name = "f24", Func = x => 1.0 - 0.61*x, A = 1.5, B = 2.0, Desc = "1 - 0.61x (linear)" },
                new BenchmarkDef { Name = "f25", Func = x => Math.Pow(x, 2.0) * Math.Abs(Math.Sin(x)) - 4.1, A = 0.0, B = 4.0, Desc = "x^2*|sin(x)| - 4.1" },
                new BenchmarkDef { Name = "f26", Func = x => Math.Pow(x, 5.0) - 3.0*Math.Pow(x, 4.0) + 25.0, A = -3.0, B = -1.0, Desc = "x^5 - 3x^4 + 25" },
                new BenchmarkDef { Name = "f27", Func = x => Math.Pow(x, 4.0) - 2.0*Math.Pow(x, 2.0) - 4.0, A = 1.0, B = 3.0, Desc = "x^4 - 2x^2 - 4" },
                new BenchmarkDef { Name = "f28", Func = x => x - 0.5*Math.Sin(x) - 1.0, A = 0.0, B = 3.0, Desc = "x - 0.5*sin(x) - 1" },
                new BenchmarkDef { Name = "f29", Func = x => Math.Exp(-x) - Math.Cos(3.0*x) - 0.5, A = 0.0, B = 1.0, Desc = "exp(-x) - cos(3x) - 0.5" },
                new BenchmarkDef { Name = "f30", Func = x => (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), A = 0.0, B = 1.5, Desc = "Wilkinson-like deg-20 polynomial" },
                new BenchmarkDef { Name = "f31", Func = x => (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), A = 19.0, B = 21.0, Desc = "Wilkinson-like deg-20 at root 20" },
                new BenchmarkDef { Name = "f32", Func = x => Math.Pow(x, 4.0) + 2.0*Math.Pow(x, 2.0) - x - 1.0, A = -0.5, B = 0.0, Desc = "x^4 + 2x^2 - x - 1" },
                new BenchmarkDef { Name = "f33", Func = x => Math.Pow(x, 4.0) - 10.0*Math.Pow(x, 3.0) + 35.0*Math.Pow(x, 2.0) - 50.0*x + 24.0, A = 0.0, B = 1.5, Desc = "x^4 - 10x^3 + 35x^2 - 50x + 24" },
                new BenchmarkDef { Name = "f34", Func = x => 4.0*Math.Sin(x) - x + 1.0, A = -1.0, B = 0.0, Desc = "4sin(x) - x + 1" },
                new BenchmarkDef { Name = "f35", Func = x => Math.Pow(x, 25.0) - 1.0, A = 0.0, B = 2.0, Desc = "x^25 - 1" },
                new BenchmarkDef { Name = "f36", Func = x => Math.Pow(x - 1.8, 6.0) * (x - 1.81), A = 0.0, B = 2.0, Desc = "(x-1.8)^6*(x-1.81) - near multiple root" },
                new BenchmarkDef { Name = "f37", Func = x => Math.Sin(20.0*x) - 0.3*x, A = 0.05, B = 0.25, Desc = "sin(20x) - 0.3x" },
                new BenchmarkDef { Name = "f38", Func = x => Math.Pow(x, 4.0) + 2.0*Math.Pow(x, 3.0) - 13.0*Math.Pow(x, 2.0) - 14.0*x + 24.0, A = -3.0, B = 1.0, Desc = "x^4 + 2x^3 - 13x^2 - 14x + 24" },
                new BenchmarkDef { Name = "f39", Func = x => Math.Exp(Math.Pow(x, 2.0)) - Math.Exp(1.2*x), A = 0.0, B = 2.0, Desc = "exp(x^2) - exp(1.2x)" },
                new BenchmarkDef { Name = "f40", Func = x => Math.Pow(x, 5.0) - 3.0*Math.Pow(x, 4.0) + 2.0*Math.Pow(x, 3.0) - x + 0.1, A = -1.0, B = 3.0, Desc = "x^5 - 3x^4 + 2x^3 - x + 0.1" },
                new BenchmarkDef { Name = "f41", Func = x => Math.Pow(x + 0.3, 7.0) - 0.01, A = -2.0, B = 1.0, Desc = "(x+0.3)^7 - 0.01" },
                new BenchmarkDef { Name = "f42", Func = x => Math.Pow(x, 6.0) - 8.0*Math.Pow(x, 5.0) + 24.0*Math.Pow(x, 4.0) - 32.0*Math.Pow(x, 3.0) + 16.0*Math.Pow(x, 2.0), A = 0.0, B = 4.0, Desc = "x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2" },
                new BenchmarkDef { Name = "f43", Func = x => -2.0*Math.Log10(0.000027027 + 2.51/(10000000.0*Math.Sqrt(x))) - 1.0/Math.Sqrt(x), A = 0.008, B = 0.03, Desc = "Colebrook-White friction factor" },
                new BenchmarkDef { Name = "f44", Func = x => x - 0.99*Math.Sin(x) - 2.0, A = 2.0, B = 3.0, Desc = "Kepler equation (e=0.99)" },
                new BenchmarkDef { Name = "f45", Func = x => (10.0 + 3.592/Math.Pow(x, 2.0))*(x - 0.04267) - 0.08206*300.0, A = 2.0, B = 3.0, Desc = "Van der Waals (CO2)" },
                new BenchmarkDef { Name = "f46", Func = x => x*Math.Exp(x/2.0) - 1.5, A = 0.0, B = 1.0, Desc = "x*exp(x/2) - 1.5" },
                new BenchmarkDef { Name = "f47", Func = x => Math.Cos(x) + 1.0*Math.Pow(1.0 - Math.Cos(x), 2.0) - 0.05*Math.Pow(x, 2.0), A = 3.0, B = 6.0, Desc = "Beam deflection equation" },
                new BenchmarkDef { Name = "f48", Func = x => 0.05 - Math.Pow(x, 3.0)/((1.0 - x)*Math.Pow(0.8 - 2.0*x, 2.0)), A = 0.01, B = 0.3, Desc = "Chemical equilibrium" },
            };

            double tol = 1e-14;
            int maxIter = 10000;

            Console.WriteLine("HybridRoots Benchmark Suite - C# Port");
            Console.WriteLine("======================================");

            double[] times = new double[4];
            int[] convs = new int[4];
            double[] iters = new double[4];
            double[] nfes = new double[4];

            Func<Func<double, double>, double, double, double, int, HybridRootsInfo, double>[] funcs = {
                Core.Mpbf, Core.Mpbfms, Core.Mptf, Core.Mptfms
            };
            string[] names = { "mpbf", "mpbfms", "mptf", "mptfms" };

            for (int i = 0; i < benchmarks.Count; i++)
            {
                var b = benchmarks[i];
                Console.WriteLine($"\n[{i + 1,2}/48] {b.Name}: {b.Desc}");

                for (int a = 0; a < 4; a++)
                {
                    HybridRootsInfo info = new HybridRootsInfo();
                    funcs[a](b.Func, b.A, b.B, tol, maxIter, info); // Warmup

                    int runs = 100;
                    double root = 0;
                    Stopwatch sw = Stopwatch.StartNew();
                    for (int r = 0; r < runs; r++)
                    {
                        root = funcs[a](b.Func, b.A, b.B, tol, maxIter, info);
                    }
                    sw.Stop();
                    double elapsedUs = sw.Elapsed.TotalMilliseconds * 1000.0 / runs;

                    if (info.Converged)
                    {
                        Console.WriteLine($"       {names[a],-8}: root={root:F10}, iter={info.Iterations,2}, nfe={info.FunctionCalls,3}");
                        times[a] += elapsedUs;
                        convs[a]++;
                        iters[a] += info.Iterations;
                        nfes[a] += info.FunctionCalls;
                    }
                    else
                    {
                        Console.WriteLine($"       {names[a],-8}: FAILED");
                    }
                }
            }

            Console.WriteLine("\nSUMMARY");
            Console.WriteLine("======================================");
            Console.WriteLine("Algorithm  | Converged  | Total Time (us)    | Avg NFE    | Avg Iterations");
            Console.WriteLine("--------------------------------------------------------------------------------");
            for (int a = 0; a < 4; a++)
            {
                Console.WriteLine($"{names[a],-10} | {convs[a],2}/{benchmarks.Count,-7} | {times[a],18:F2} | {nfes[a] / convs[a],10:F2} | {iters[a] / convs[a],15:F2}");
            }
        }
    }
}
