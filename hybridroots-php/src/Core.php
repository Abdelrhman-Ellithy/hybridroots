<?php

namespace HybridRoots;

class HybridRootsInfo {
    public int $iterations = 0;
    public int $functionCalls = 0;
    public bool $converged = false;
}

class Core {
    private const EPS = 1e-15;

    public static function mpbf(callable $f, float $a, float $b, float $tol = 1e-15, int $maxIter = 10000, HybridRootsInfo $info): float {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $a; }
        if (abs($fb) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $b; }
        if ($fa * $fb >= 0) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = false; return $a; }

        for ($n = 1; $n <= $maxIter; $n++) {
            $mid = 0.5 * ($a + $b);
            $fmid = $f($mid);
            $nfe++;
            if (abs($fmid) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $mid; }
            if ($fa * $fmid < 0) { $b = $mid; $fb = $fmid; } else { $a = $mid; $fa = $fmid; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $fp = ($a * $fb - $b * $fa) / $denom;
            $ffp = $f($fp);
            $nfe++;
            if (abs($ffp) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $fp; }
            if ($fa * $ffp < 0) { $b = $fp; $fb = $ffp; } else { $a = $fp; $fa = $ffp; }
        }
        $info->iterations = $maxIter; $info->functionCalls = $nfe;
        $finalX = 0.5 * ($a + $b);
        $info->converged = abs($f($finalX)) <= $tol;
        $info->functionCalls++;
        return $finalX;
    }

    public static function mpbfms(callable $f, float $a, float $b, float $tol = 1e-15, int $maxIter = 10000, HybridRootsInfo $info): float {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $a; }
        if (abs($fb) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $b; }
        if ($fa * $fb >= 0) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = false; return $a; }

        for ($n = 1; $n <= $maxIter; $n++) {
            $mid = 0.5 * ($a + $b);
            $fmid = $f($mid);
            $nfe++;
            if ($fa * $fmid < 0) { $b = $mid; $fb = $fmid; } else { $a = $mid; $fa = $fmid; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $fp = ($a * $fb - $b * $fa) / $denom;
            $ffp = $f($fp);
            $nfe++;
            if ($fa * $ffp < 0) { $b = $fp; $fb = $ffp; } else { $a = $fp; $fa = $ffp; }
            if (abs($ffp) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $fp; }

            $delta = 1e-8 * max(1.0, abs($fp)) + self::EPS;
            $fDelta = $f($fp + $delta);
            $nfe++;
            $denomSecant = $fDelta - $ffp;
            if (abs($denomSecant) < self::EPS) $denomSecant = $denomSecant >= 0 ? $denomSecant + self::EPS : $denomSecant - self::EPS;
            $xS = $fp - ($delta * $ffp) / $denomSecant;

            if ($xS > $a && $xS < $b) {
                $fxS = $f($xS);
                $nfe++;
                if (abs($fxS) < abs($ffp)) {
                    if ($fa * $fxS < 0) { $b = $xS; $fb = $fxS; } else { $a = $xS; $fa = $fxS; }
                    if (abs($fxS) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $xS; }
                }
            }
        }
        $info->iterations = $maxIter; $info->functionCalls = $nfe;
        $finalX = 0.5 * ($a + $b);
        $info->converged = abs($f($finalX)) <= $tol;
        $info->functionCalls++;
        return $finalX;
    }

    public static function mptf(callable $f, float $a, float $b, float $tol = 1e-15, int $maxIter = 10000, HybridRootsInfo $info): float {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $a; }
        if (abs($fb) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $b; }
        if ($fa * $fb >= 0) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = false; return $a; }

        for ($n = 1; $n <= $maxIter; $n++) {
            $diff = $b - $a;
            $x1 = $a + $diff / 3.0; $x2 = $b - $diff / 3.0;
            $fx1 = $f($x1); $fx2 = $f($x2);
            $nfe += 2;
            if (abs($fx1) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $x1; }
            if (abs($fx2) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $x2; }

            if ($fa * $fx1 < 0) { $b = $x1; $fb = $fx1; }
            else if ($fx1 * $fx2 < 0) { $a = $x1; $b = $x2; $fa = $fx1; $fb = $fx2; }
            else { $a = $x2; $fa = $fx2; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $x = ($a * $fb - $b * $fa) / $denom;
            $fx = $f($x);
            $nfe++;
            if (abs($fx) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $x; }
            if ($fa * $fx < 0) { $b = $x; $fb = $fx; } else { $a = $x; $fa = $fx; }
        }
        $info->iterations = $maxIter; $info->functionCalls = $nfe;
        $finalX = 0.5 * ($a + $b);
        $info->converged = abs($f($finalX)) <= $tol;
        $info->functionCalls++;
        return $finalX;
    }

    public static function mptfms(callable $f, float $a, float $b, float $tol = 1e-15, int $maxIter = 10000, HybridRootsInfo $info): float {
        $fa = $f($a); $fb = $f($b);
        $nfe = 2;
        if (abs($fa) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $a; }
        if (abs($fb) <= $tol) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = true; return $b; }
        if ($fa * $fb >= 0) { $info->iterations = 0; $info->functionCalls = $nfe; $info->converged = false; return $a; }

        for ($n = 1; $n <= $maxIter; $n++) {
            $diff = $b - $a;
            $x1 = $a + $diff / 3.0; $x2 = $b - $diff / 3.0;
            $fx1 = $f($x1); $fx2 = $f($x2);
            $nfe += 2;
            if (abs($fx1) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $x1; }
            if (abs($fx2) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $x2; }

            if ($fa * $fx1 < 0) { $b = $x1; $fb = $fx1; }
            else if ($fx1 * $fx2 < 0) { $a = $x1; $b = $x2; $fa = $fx1; $fb = $fx2; }
            else { $a = $x2; $fa = $fx2; }

            $denom = $fb - $fa;
            if (abs($denom) < self::EPS) $denom = $denom >= 0 ? $denom + self::EPS : $denom - self::EPS;
            $fp = ($a * $fb - $b * $fa) / $denom;
            $ffp = $f($fp);
            $nfe++;
            if ($fa * $ffp < 0) { $b = $fp; $fb = $ffp; } else { $a = $fp; $fa = $ffp; }
            if (abs($ffp) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $fp; }

            $delta = 1e-8 * max(1.0, abs($fp)) + self::EPS;
            $fDelta = $f($fp + $delta);
            $nfe++;
            $denomSecant = $fDelta - $ffp;
            if (abs($denomSecant) < self::EPS) $denomSecant = $denomSecant >= 0 ? $denomSecant + self::EPS : $denomSecant - self::EPS;
            $xS = $fp - ($delta * $ffp) / $denomSecant;

            if ($xS > $a && $xS < $b) {
                $fxS = $f($xS);
                $nfe++;
                if (abs($fxS) < abs($ffp)) {
                    if ($fa * $fxS < 0) { $b = $xS; $fb = $fxS; } else { $a = $xS; $fa = $fxS; }
                    if (abs($fxS) <= $tol) { $info->iterations = $n; $info->functionCalls = $nfe; $info->converged = true; return $xS; }
                }
            }
        }
        $info->iterations = $maxIter; $info->functionCalls = $nfe;
        $finalX = 0.5 * ($a + $b);
        $info->converged = abs($f($finalX)) <= $tol;
        $info->functionCalls++;
        return $finalX;
    }
}
