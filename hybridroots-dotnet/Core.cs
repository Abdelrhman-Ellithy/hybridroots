using System;

namespace HybridRoots
{
    public class HybridRootsInfo
    {
        public int Iterations { get; set; }
        public int FunctionCalls { get; set; }
        public bool Converged { get; set; }
    }

    public static class Core
    {
        private const double EPS = 1e-15;

        public static double Mpbf(Func<double, double> f, double a, double b, double tol, int maxIter, HybridRootsInfo info)
        {
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return a; }
            if (Math.Abs(fb) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return b; }
            if (fa * fb >= 0) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = false; return a; }

            for (int n = 1; n <= maxIter; n++)
            {
                double mid = 0.5 * (a + b);
                double fmid = f(mid);
                nfe++;
                if (Math.Abs(fmid) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return mid; }
                if (fa * fmid < 0) { b = mid; fb = fmid; } else { a = mid; fa = fmid; }

                double denom = fb - fa;
                if (Math.Abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
                double fp = (a * fb - b * fa) / denom;
                double ffp = f(fp);
                nfe++;
                if (Math.Abs(ffp) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return fp; }
                if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
            }
            info.Iterations = maxIter; info.FunctionCalls = nfe;
            double finalX = 0.5 * (a + b);
            info.Converged = Math.Abs(f(finalX)) <= tol;
            info.FunctionCalls++;
            return finalX;
        }

        public static double Mpbfms(Func<double, double> f, double a, double b, double tol, int maxIter, HybridRootsInfo info)
        {
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return a; }
            if (Math.Abs(fb) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return b; }
            if (fa * fb >= 0) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = false; return a; }

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
                if (Math.Abs(ffp) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return fp; }

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
                        if (Math.Abs(fxS) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return xS; }
                    }
                }
            }
            info.Iterations = maxIter; info.FunctionCalls = nfe;
            double finalX = 0.5 * (a + b);
            info.Converged = Math.Abs(f(finalX)) <= tol;
            info.FunctionCalls++;
            return finalX;
        }

        public static double Mptf(Func<double, double> f, double a, double b, double tol, int maxIter, HybridRootsInfo info)
        {
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return a; }
            if (Math.Abs(fb) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return b; }
            if (fa * fb >= 0) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = false; return a; }

            for (int n = 1; n <= maxIter; n++)
            {
                double diff = b - a;
                double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
                double fx1 = f(x1), fx2 = f(x2);
                nfe += 2;
                if (Math.Abs(fx1) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return x1; }
                if (Math.Abs(fx2) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return x2; }

                if (fa * fx1 < 0) { b = x1; fb = fx1; }
                else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
                else { a = x2; fa = fx2; }

                double denom = fb - fa;
                if (Math.Abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
                double x = (a * fb - b * fa) / denom;
                double fx = f(x);
                nfe++;
                if (Math.Abs(fx) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return x; }
                if (fa * fx < 0) { b = x; fb = fx; } else { a = x; fa = fx; }
            }
            info.Iterations = maxIter; info.FunctionCalls = nfe;
            double finalX = 0.5 * (a + b);
            info.Converged = Math.Abs(f(finalX)) <= tol;
            info.FunctionCalls++;
            return finalX;
        }

        public static double Mptfms(Func<double, double> f, double a, double b, double tol, int maxIter, HybridRootsInfo info)
        {
            double fa = f(a), fb = f(b);
            int nfe = 2;
            if (Math.Abs(fa) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return a; }
            if (Math.Abs(fb) <= tol) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = true; return b; }
            if (fa * fb >= 0) { info.Iterations = 0; info.FunctionCalls = nfe; info.Converged = false; return a; }

            for (int n = 1; n <= maxIter; n++)
            {
                double diff = b - a;
                double x1 = a + diff / 3.0, x2 = b - diff / 3.0;
                double fx1 = f(x1), fx2 = f(x2);
                nfe += 2;
                if (Math.Abs(fx1) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return x1; }
                if (Math.Abs(fx2) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return x2; }

                if (fa * fx1 < 0) { b = x1; fb = fx1; }
                else if (fx1 * fx2 < 0) { a = x1; b = x2; fa = fx1; fb = fx2; }
                else { a = x2; fa = fx2; }

                double denom = fb - fa;
                if (Math.Abs(denom) < EPS) denom = denom >= 0 ? denom + EPS : denom - EPS;
                double fp = (a * fb - b * fa) / denom;
                double ffp = f(fp);
                nfe++;
                if (fa * ffp < 0) { b = fp; fb = ffp; } else { a = fp; fa = ffp; }
                if (Math.Abs(ffp) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return fp; }

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
                        if (Math.Abs(fxS) <= tol) { info.Iterations = n; info.FunctionCalls = nfe; info.Converged = true; return xS; }
                    }
                }
            }
            info.Iterations = maxIter; info.FunctionCalls = nfe;
            double finalX = 0.5 * (a + b);
            info.Converged = Math.Abs(f(finalX)) <= tol;
            info.FunctionCalls++;
            return finalX;
        }
    }
}
