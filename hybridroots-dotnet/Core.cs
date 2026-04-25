// <copyright file="Core.cs" company="HybridRoots">
// Licensed under the Apache License, Version 2.0.
// </copyright>
//
// This library implements the four novel hybrid root-finding algorithms introduced in:
//
//   Ellithy, A. (2026). "Four New Multi-Phase Hybrid Bracketing Algorithms for
//   Numerical Root Finding." Journal of the Egyptian Mathematical Society, 34.
//   DOI: https://doi.org/10.21608/joems.2026.440115.1078
//
// Author: Abdelrahman Ellithy

using System;

namespace HybridRoots
{
    /// <summary>
    /// Holds the result of a HybridRoots algorithm call.
    /// Mirrors scipy.optimize.RootResults for cross-language consistency.
    /// </summary>
    public sealed class HybridRootsResult
    {
        /// <summary>Gets the estimated root location.</summary>
        public double Root { get; }
        /// <summary>Gets the number of iterations performed.</summary>
        public int Iterations { get; }
        /// <summary>Gets the number of function evaluations performed.</summary>
        public int FunctionCalls { get; }
        /// <summary>Gets a value indicating whether |f(root)| &lt;= tol.</summary>
        public bool Converged { get; }

        /// <summary>Initializes a new instance of <see cref="HybridRootsResult"/>.</summary>
        public HybridRootsResult(double root, int iterations, int functionCalls, bool converged)
        {
            Root = root;
            Iterations = iterations;
            FunctionCalls = functionCalls;
            Converged = converged;
        }

        /// <inheritdoc/>
        public override string ToString() =>
            $"HybridRootsResult(root={Root:G17}, iterations={Iterations}, " +
            $"functionCalls={FunctionCalls}, converged={Converged})";
    }

    /// <summary>
    /// Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding.
    /// <para>
    /// All algorithms are deterministic and guarantee convergence for any continuous
    /// function f on a bracket [a, b] where f(a)*f(b) &lt; 0.
    /// </para>
    /// <para>
    /// Reference: Ellithy, A. (2026). Journal of the Egyptian Mathematical Society, 34.
    /// DOI: <see href="https://doi.org/10.21608/joems.2026.440115.1078"/>
    /// </para>
    /// </summary>
    public static class Core
    {
        private const double EPS = 1e-15;

        /// <summary>
        /// Multi-Phase Bisection–False Position (Opt.BF).
        /// <para>
        /// Combines classical Bisection with False Position for guaranteed convergence
        /// with faster interval reduction. See Section 2 of the paper.
        /// </para>
        /// </summary>
        /// <param name="f">The continuous function whose root is sought.</param>
        /// <param name="a">Left endpoint of the initial bracket (f(a)*f(b) &lt; 0).</param>
        /// <param name="b">Right endpoint of the initial bracket.</param>
        /// <param name="tol">Absolute tolerance; convergence declared when |f(x)| &lt;= tol.</param>
        /// <param name="maxIter">Maximum number of iterations allowed.</param>
        /// <returns>A <see cref="HybridRootsResult"/> with root, iterations, functionCalls, and converged.</returns>
        /// <exception cref="ArgumentNullException">Thrown when f is null.</exception>
        public static HybridRootsResult Mpbf(Func<double, double> f, double a, double b,
                                              double tol = 1e-14, int maxIter = 10000)
        {
            if (f == null) throw new ArgumentNullException(nameof(f));
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
            if (Math.Abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
            if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

            for (int n = 1; n <= maxIter; n++)
            {
                double mid = 0.5 * (a + b);
                double fmid = f(mid);
                nfe++;
                if (Math.Abs(fmid) <= tol) return new HybridRootsResult(mid, n, nfe, true);
                if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

                double denom = fb - fa;
                if (Math.Abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
                double fp = (a * fb - b * fa) / denom;
                double ffp = f(fp);
                nfe++;
                if (Math.Abs(ffp) <= tol) return new HybridRootsResult(fp, n, nfe, true);
                if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
            }
            double finalX = 0.5 * (a + b);
            bool converged = Math.Abs(f(finalX)) <= tol;
            return new HybridRootsResult(finalX, maxIter, nfe + 1, converged);
        }

        /// <summary>
        /// Multi-Phase Bisection–False Position–Modified Secant (Opt.BFMS).
        /// <para>
        /// Extends Opt.BF with an adaptive Modified Secant acceleration step that
        /// is accepted only when it reduces the residual and remains in-bracket.
        /// See Section 3 of the paper.
        /// </para>
        /// </summary>
        /// <param name="f">The continuous function whose root is sought.</param>
        /// <param name="a">Left endpoint of the initial bracket.</param>
        /// <param name="b">Right endpoint of the initial bracket.</param>
        /// <param name="tol">Absolute tolerance.</param>
        /// <param name="maxIter">Maximum number of iterations.</param>
        /// <returns>A <see cref="HybridRootsResult"/>.</returns>
        /// <exception cref="ArgumentNullException">Thrown when f is null.</exception>
        public static HybridRootsResult Mpbfms(Func<double, double> f, double a, double b,
                                                double tol = 1e-14, int maxIter = 10000)
        {
            if (f == null) throw new ArgumentNullException(nameof(f));
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
            if (Math.Abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
            if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

            for (int n = 1; n <= maxIter; n++)
            {
                double mid = 0.5 * (a + b);
                double fmid = f(mid);
                nfe++;
                if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

                double denom = fb - fa;
                if (Math.Abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
                double fp = (a * fb - b * fa) / denom;
                double ffp = f(fp);
                nfe++;
                if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
                if (Math.Abs(ffp) <= tol) return new HybridRootsResult(fp, n, nfe, true);

                double delta = 1e-8 * Math.Max(1.0, Math.Abs(fp)) + EPS;
                double fDelta = f(fp + delta);
                nfe++;
                double denomSecant = fDelta - ffp;
                if (Math.Abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
                double xS = fp - (delta * ffp) / denomSecant;

                if (xS > a && xS < b)
                {
                    double fxS = f(xS);
                    nfe++;
                    if (Math.Abs(fxS) < Math.Abs(ffp))
                    {
                        if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                        if (Math.Abs(fxS) <= tol) return new HybridRootsResult(xS, n, nfe, true);
                    }
                }
            }
            double finalX2 = 0.5 * (a + b);
            bool converged2 = Math.Abs(f(finalX2)) <= tol;
            return new HybridRootsResult(finalX2, maxIter, nfe + 1, converged2);
        }

        /// <summary>
        /// Multi-Phase Trisection–False Position (Opt.TF).
        /// <para>
        /// Divides the bracket into thirds for faster interval reduction, then applies
        /// False Position refinement. See Section 4 of the paper.
        /// </para>
        /// </summary>
        /// <param name="f">The continuous function whose root is sought.</param>
        /// <param name="a">Left endpoint of the initial bracket.</param>
        /// <param name="b">Right endpoint of the initial bracket.</param>
        /// <param name="tol">Absolute tolerance.</param>
        /// <param name="maxIter">Maximum number of iterations.</param>
        /// <returns>A <see cref="HybridRootsResult"/>.</returns>
        /// <exception cref="ArgumentNullException">Thrown when f is null.</exception>
        public static HybridRootsResult Mptf(Func<double, double> f, double a, double b,
                                              double tol = 1e-14, int maxIter = 10000)
        {
            if (f == null) throw new ArgumentNullException(nameof(f));
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
            if (Math.Abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
            if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

            for (int n = 1; n <= maxIter; n++)
            {
                double diff = b - a;
                double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
                double fx1 = f(x1), fx2 = f(x2);
                nfe += 2;
                if (Math.Abs(fx1) <= tol) return new HybridRootsResult(x1, n, nfe, true);
                if (Math.Abs(fx2) <= tol) return new HybridRootsResult(x2, n, nfe, true);

                if (fa * fx1 < 0) { b = x1; fb = fx1; }
                else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
                else { a = x2; fa = fx2; }

                double denom = fb - fa;
                if (Math.Abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
                double x = (a * fb - b * fa) / denom;
                double fx = f(x);
                nfe++;
                if (Math.Abs(fx) <= tol) return new HybridRootsResult(x, n, nfe, true);
                if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
            }
            double finalX3 = 0.5 * (a + b);
            bool converged3 = Math.Abs(f(finalX3)) <= tol;
            return new HybridRootsResult(finalX3, maxIter, nfe + 1, converged3);
        }

        /// <summary>
        /// Multi-Phase Trisection–False Position–Modified Secant (Opt.TFMS).
        /// <para>
        /// Combines Trisection, False Position, and an adaptive Modified Secant step
        /// for maximum efficiency. The fastest of the four algorithms for smooth functions.
        /// See Section 5 of the paper.
        /// </para>
        /// </summary>
        /// <param name="f">The continuous function whose root is sought.</param>
        /// <param name="a">Left endpoint of the initial bracket.</param>
        /// <param name="b">Right endpoint of the initial bracket.</param>
        /// <param name="tol">Absolute tolerance.</param>
        /// <param name="maxIter">Maximum number of iterations.</param>
        /// <returns>A <see cref="HybridRootsResult"/>.</returns>
        /// <exception cref="ArgumentNullException">Thrown when f is null.</exception>
        public static HybridRootsResult Mptfms(Func<double, double> f, double a, double b,
                                                double tol = 1e-14, int maxIter = 10000)
        {
            if (f == null) throw new ArgumentNullException(nameof(f));
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) return new HybridRootsResult(a, 0, nfe, true);
            if (Math.Abs(fb) <= tol) return new HybridRootsResult(b, 0, nfe, true);
            if (fa * fb >= 0) return new HybridRootsResult(a, 0, nfe, false);

            for (int n = 1; n <= maxIter; n++)
            {
                double diff = b - a;
                double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
                double fx1 = f(x1), fx2 = f(x2);
                nfe += 2;
                if (Math.Abs(fx1) <= tol) return new HybridRootsResult(x1, n, nfe, true);
                if (Math.Abs(fx2) <= tol) return new HybridRootsResult(x2, n, nfe, true);

                if (fa * fx1 < 0) { b = x1; fb = fx1; }
                else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
                else { a = x2; fa = fx2; }

                double denom = fb - fa;
                if (Math.Abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
                double fp = (a * fb - b * fa) / denom;
                double ffp = f(fp);
                nfe++;
                if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
                if (Math.Abs(ffp) <= tol) return new HybridRootsResult(fp, n, nfe, true);

                double delta = 1e-8 * Math.Max(1.0, Math.Abs(fp)) + EPS;
                double fDelta = f(fp + delta);
                nfe++;
                double denomSecant = fDelta - ffp;
                if (Math.Abs(denomSecant) < EPS) denomSecant = denomSecant >= 0 ? denomSecant + EPS : denomSecant - EPS;
                double xS = fp - (delta * ffp) / denomSecant;

                if (xS > a && xS < b)
                {
                    double fxS = f(xS);
                    nfe++;
                    if (Math.Abs(fxS) < Math.Abs(ffp))
                    {
                        if (fa * fxS < 0) { b = xS; fb = fxS; } else { a = xS; fa = fxS; }
                        if (Math.Abs(fxS) <= tol) return new HybridRootsResult(xS, n, nfe, true);
                    }
                }
            }
            double finalX4 = 0.5 * (a + b);
            bool converged4 = Math.Abs(f(finalX4)) <= tol;
            return new HybridRootsResult(finalX4, maxIter, nfe + 1, converged4);
        }
    }
}
