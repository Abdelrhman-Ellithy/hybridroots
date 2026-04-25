<?php

declare(strict_types=1);

/**
 * HybridRoots – Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding.
 *
 * Implements the algorithms introduced in:
 *   Ellithy, A. (2026). "Four New Multi-Phase Hybrid Bracketing Algorithms for
 *   Numerical Root Finding." Journal of the Egyptian Mathematical Society, 34.
 *   DOI: https://doi.org/10.21608/joems.2026.440115.1078
 *
 * All algorithms are deterministic and guarantee convergence for any continuous
 * function f on a bracket [a, b] where f(a)*f(b) < 0.
 *
 * @author  Abdelrahman Ellithy
 * @license Apache-2.0
 * @version 1.0.0
 */

namespace HybridRoots;

/**
 * Holds the result of a HybridRoots algorithm call.
 * Mirrors scipy.optimize.RootResults for cross-language consistency.
 */
final class HybridRootsResult
{
    /**
     * @param float $root          Estimated root location.
     * @param int   $iterations    Number of iterations performed.
     * @param int   $functionCalls Number of function evaluations performed.
     * @param bool  $converged     True if |f(root)| <= tol.
     */
    public function __construct(
        public readonly float $root,
        public readonly int   $iterations,
        public readonly int   $functionCalls,
        public readonly bool  $converged,
    ) {}

    public function __toString(): string
    {
        $conv = $this->converged ? 'true' : 'false';
        return "HybridRootsResult(root={$this->root}, iterations={$this->iterations}, " .
               "functionCalls={$this->functionCalls}, converged={$conv})";
    }
}

/**
 * Four Multi-Phase Hybrid Bracketing root-finding algorithms.
 *
 * @see https://doi.org/10.21608/joems.2026.440115.1078
 */
final class Core
{
    private const EPS = 1e-15;

    /** Prevent instantiation – all methods are static. */
    private function __construct() {}

    /**
     * Multi-Phase Bisection–False Position (Opt.BF).
     *
     * Combines classical Bisection with False Position for guaranteed convergence
     * with faster interval reduction.
     * See Section 2 of DOI: 10.21608/joems.2026.440115.1078
     *
     * @param callable $f       Continuous function f(x): float.
     * @param float    $a       Left endpoint of the initial bracket (f(a)*f(b) < 0).
     * @param float    $b       Right endpoint of the initial bracket.
     * @param float    $tol     Absolute tolerance (default 1e-14).
     * @param int      $maxIter Maximum iterations (default 10000).
     * @return HybridRootsResult
     */
    public static function mpbf(
        callable $f, float $a, float $b,
        float $tol = 1e-14, int $maxIter = 10000
    ): HybridRootsResult {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) return new HybridRootsResult($a, 0, $nfe, true);
        if (abs($fb) <= $tol) return new HybridRootsResult($b, 0, $nfe, true);
        if ($fa * $fb >= 0) return new HybridRootsResult($a, 0, $nfe, false);

        for ($n = 1; $n <= $maxIter; $n++) {
            $mid = 0.5 * ($a + $b);
            $fmid = $f($mid);
            $nfe++;
            if (abs($fmid) <= $tol) return new HybridRootsResult($mid, $n, $nfe, true);
            if ($fa * $fmid < 0) { $b = $mid; $fb = $fmid; } else { $a = $mid; $fa = $fmid; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $fp  = ($a * $fb - $b * $fa) / $denom;
            $ffp = $f($fp);
            $nfe++;
            if (abs($ffp) <= $tol) return new HybridRootsResult($fp, $n, $nfe, true);
            if ($fa * $ffp < 0) { $b = $fp; $fb = $ffp; } else { $a = $fp; $fa = $ffp; }
        }
        $finalX = 0.5 * ($a + $b);
        return new HybridRootsResult($finalX, $maxIter, $nfe + 1, abs($f($finalX)) <= $tol);
    }

    /**
     * Multi-Phase Bisection–False Position–Modified Secant (Opt.BFMS).
     *
     * Extends Opt.BF with an adaptive Modified Secant acceleration step that
     * is accepted only when it reduces the residual and stays in-bracket.
     * See Section 3 of DOI: 10.21608/joems.2026.440115.1078
     *
     * @param callable $f       Continuous function f(x): float.
     * @param float    $a       Left endpoint of the initial bracket.
     * @param float    $b       Right endpoint of the initial bracket.
     * @param float    $tol     Absolute tolerance (default 1e-14).
     * @param int      $maxIter Maximum iterations (default 10000).
     * @return HybridRootsResult
     */
    public static function mpbfms(
        callable $f, float $a, float $b,
        float $tol = 1e-14, int $maxIter = 10000
    ): HybridRootsResult {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) return new HybridRootsResult($a, 0, $nfe, true);
        if (abs($fb) <= $tol) return new HybridRootsResult($b, 0, $nfe, true);
        if ($fa * $fb >= 0) return new HybridRootsResult($a, 0, $nfe, false);

        for ($n = 1; $n <= $maxIter; $n++) {
            $mid = 0.5 * ($a + $b);
            $fmid = $f($mid);
            $nfe++;
            if ($fa * $fmid < 0) { $b = $mid; $fb = $fmid; } else { $a = $mid; $fa = $fmid; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $fp  = ($a * $fb - $b * $fa) / $denom;
            $ffp = $f($fp);
            $nfe++;
            if ($fa * $ffp < 0) { $b = $fp; $fb = $ffp; } else { $a = $fp; $fa = $ffp; }
            if (abs($ffp) <= $tol) return new HybridRootsResult($fp, $n, $nfe, true);

            $delta      = 1e-8 * max(1.0, abs($fp)) + self::EPS;
            $fDelta     = $f($fp + $delta);
            $nfe++;
            $denomSecant = $fDelta - $ffp;
            if (abs($denomSecant) < self::EPS) $denomSecant = $denomSecant >= 0 ? $denomSecant + self::EPS : $denomSecant - self::EPS;
            $xS = $fp - ($delta * $ffp) / $denomSecant;

            if ($xS > $a && $xS < $b) {
                $fxS = $f($xS);
                $nfe++;
                if (abs($fxS) < abs($ffp)) {
                    if ($fa * $fxS < 0) { $b = $xS; $fb = $fxS; } else { $a = $xS; $fa = $fxS; }
                    if (abs($fxS) <= $tol) return new HybridRootsResult($xS, $n, $nfe, true);
                }
            }
        }
        $finalX = 0.5 * ($a + $b);
        return new HybridRootsResult($finalX, $maxIter, $nfe + 1, abs($f($finalX)) <= $tol);
    }

    /**
     * Multi-Phase Trisection–False Position (Opt.TF).
     *
     * Divides the bracket into thirds for faster interval reduction, then applies
     * False Position refinement.
     * See Section 4 of DOI: 10.21608/joems.2026.440115.1078
     *
     * @param callable $f       Continuous function f(x): float.
     * @param float    $a       Left endpoint of the initial bracket.
     * @param float    $b       Right endpoint of the initial bracket.
     * @param float    $tol     Absolute tolerance (default 1e-14).
     * @param int      $maxIter Maximum iterations (default 10000).
     * @return HybridRootsResult
     */
    public static function mptf(
        callable $f, float $a, float $b,
        float $tol = 1e-14, int $maxIter = 10000
    ): HybridRootsResult {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) return new HybridRootsResult($a, 0, $nfe, true);
        if (abs($fb) <= $tol) return new HybridRootsResult($b, 0, $nfe, true);
        if ($fa * $fb >= 0) return new HybridRootsResult($a, 0, $nfe, false);

        for ($n = 1; $n <= $maxIter; $n++) {
            $diff = $b - $a;
            $x1 = $a + $diff / 3.0; $x2 = $b - $diff / 3.0;
            $fx1 = $f($x1); $fx2 = $f($x2);
            $nfe += 2;
            if (abs($fx1) <= $tol) return new HybridRootsResult($x1, $n, $nfe, true);
            if (abs($fx2) <= $tol) return new HybridRootsResult($x2, $n, $nfe, true);

            if ($fa * $fx1 < 0)      { $b = $x1; $fb = $fx1; }
            elseif ($fx1 * $fx2 < 0) { $a = $x1; $b = $x2; $fa = $fx1; $fb = $fx2; }
            else                      { $a = $x2; $fa = $fx2; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $x  = ($a * $fb - $b * $fa) / $denom;
            $fx = $f($x);
            $nfe++;
            if (abs($fx) <= $tol) return new HybridRootsResult($x, $n, $nfe, true);
            if ($fa * $fx < 0) { $b = $x; $fb = $fx; } else { $a = $x; $fa = $fx; }
        }
        $finalX = 0.5 * ($a + $b);
        return new HybridRootsResult($finalX, $maxIter, $nfe + 1, abs($f($finalX)) <= $tol);
    }

    /**
     * Multi-Phase Trisection–False Position–Modified Secant (Opt.TFMS).
     *
     * Combines Trisection, False Position, and an adaptive Modified Secant step
     * for maximum efficiency. The fastest of the four algorithms for smooth functions.
     * See Section 5 of DOI: 10.21608/joems.2026.440115.1078
     *
     * @param callable $f       Continuous function f(x): float.
     * @param float    $a       Left endpoint of the initial bracket.
     * @param float    $b       Right endpoint of the initial bracket.
     * @param float    $tol     Absolute tolerance (default 1e-14).
     * @param int      $maxIter Maximum iterations (default 10000).
     * @return HybridRootsResult
     */
    public static function mptfms(
        callable $f, float $a, float $b,
        float $tol = 1e-14, int $maxIter = 10000
    ): HybridRootsResult {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) return new HybridRootsResult($a, 0, $nfe, true);
        if (abs($fb) <= $tol) return new HybridRootsResult($b, 0, $nfe, true);
        if ($fa * $fb >= 0) return new HybridRootsResult($a, 0, $nfe, false);

        for ($n = 1; $n <= $maxIter; $n++) {
            $diff = $b - $a;
            $x1 = $a + $diff / 3.0; $x2 = $b - $diff / 3.0;
            $fx1 = $f($x1); $fx2 = $f($x2);
            $nfe += 2;
            if (abs($fx1) <= $tol) return new HybridRootsResult($x1, $n, $nfe, true);
            if (abs($fx2) <= $tol) return new HybridRootsResult($x2, $n, $nfe, true);

            if ($fa * $fx1 < 0)      { $b = $x1; $fb = $fx1; }
            elseif ($fx1 * $fx2 < 0) { $a = $x1; $b = $x2; $fa = $fx1; $fb = $fx2; }
            else                      { $a = $x2; $fa = $fx2; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $fp  = ($a * $fb - $b * $fa) / $denom;
            $ffp = $f($fp);
            $nfe++;
            if ($fa * $ffp < 0) { $b = $fp; $fb = $ffp; } else { $a = $fp; $fa = $ffp; }
            if (abs($ffp) <= $tol) return new HybridRootsResult($fp, $n, $nfe, true);

            $delta      = 1e-8 * max(1.0, abs($fp)) + self::EPS;
            $fDelta     = $f($fp + $delta);
            $nfe++;
            $denomSecant = $fDelta - $ffp;
            if (abs($denomSecant) < self::EPS) $denomSecant = $denomSecant >= 0 ? $denomSecant + self::EPS : $denomSecant - self::EPS;
            $xS = $fp - ($delta * $ffp) / $denomSecant;

            if ($xS > $a && $xS < $b) {
                $fxS = $f($xS);
                $nfe++;
                if (abs($fxS) < abs($ffp)) {
                    if ($fa * $fxS < 0) { $b = $xS; $fb = $fxS; } else { $a = $xS; $fa = $fxS; }
                    if (abs($fxS) <= $tol) return new HybridRootsResult($xS, $n, $nfe, true);
                }
            }
        }
        $finalX = 0.5 * ($a + $b);
        return new HybridRootsResult($finalX, $maxIter, $nfe + 1, abs($f($finalX)) <= $tol);
    }
}
