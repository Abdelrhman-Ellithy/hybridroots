<?php

require_once __DIR__ . '/src/Core.php';

use HybridRoots\Core;

$benchmarks = [
    ['name' => 'f1', 'func' => function($x) { return $x * exp($x) - 7.0; }, 'a' => 1.0, 'b' => 2.0, 'desc' => 'x*exp(x) - 7'],
    ['name' => 'f2', 'func' => function($x) { return pow($x, 3.0) - $x - 1.0; }, 'a' => 1.0, 'b' => 2.0, 'desc' => 'x^3 - x - 1'],
    ['name' => 'f3', 'func' => function($x) { return pow($x, 2.0) - $x - 2.0; }, 'a' => 1.0, 'b' => 4.0, 'desc' => 'x^2 - x - 2'],
    ['name' => 'f4', 'func' => function($x) { return $x - cos($x); }, 'a' => 0.0, 'b' => 1.0, 'desc' => 'x - cos(x)'],
    ['name' => 'f5', 'func' => function($x) { return pow($x, 2.0) - 10.0; }, 'a' => 3.0, 'b' => 4.0, 'desc' => 'x^2 - 10'],
    ['name' => 'f6', 'func' => function($x) { return sin($x) - pow($x, 2.0); }, 'a' => 0.5, 'b' => 1.0, 'desc' => 'sin(x) - x^2'],
    ['name' => 'f7', 'func' => function($x) { return $x + log($x); }, 'a' => 0.1, 'b' => 1.0, 'desc' => 'x + ln(x)'],
    ['name' => 'f8', 'func' => function($x) { return exp($x) - 3.0*$x - 2.0; }, 'a' => 2.0, 'b' => 3.0, 'desc' => 'exp(x) - 3x - 2'],
    ['name' => 'f9', 'func' => function($x) { return pow($x, 2.0) + exp($x/2.0) - 5.0; }, 'a' => 1.0, 'b' => 2.0, 'desc' => 'x^2 + exp(x/2) - 5'],
    ['name' => 'f10', 'func' => function($x) { return $x * sin($x) - 1.0; }, 'a' => 0.0, 'b' => 2.0, 'desc' => 'x*sin(x) - 1'],
    ['name' => 'f11', 'func' => function($x) { return $x * cos($x) + 1.0; }, 'a' => -2.0, 'b' => 4.0, 'desc' => 'x*cos(x) + 1'],
    ['name' => 'f12', 'func' => function($x) { return pow($x, 10.0) - 1.0; }, 'a' => 0.0, 'b' => 1.3, 'desc' => 'x^10 - 1'],
    ['name' => 'f13', 'func' => function($x) { return pow($x, 2.0) + 2.0*$x - 7.0; }, 'a' => 1.0, 'b' => 3.0, 'desc' => 'x^2 + 2x - 7'],
    ['name' => 'f14', 'func' => function($x) { return pow($x, 3.0) - 2.0*$x - 5.0; }, 'a' => 2.0, 'b' => 3.0, 'desc' => 'x^3 - 2x - 5'],
    ['name' => 'f15', 'func' => function($x) { return exp($x) - 3.0*pow($x, 2.0); }, 'a' => 0.0, 'b' => 1.0, 'desc' => 'exp(x) - 3x^2'],
    ['name' => 'f16', 'func' => function($x) { return sin(10.0*$x) - 0.5*$x; }, 'a' => 0.1, 'b' => 0.4, 'desc' => 'sin(10x) - 0.5x'],
    ['name' => 'f17', 'func' => function($x) { return $x - 0.8*sin($x) - 1.2; }, 'a' => 1.0, 'b' => 3.0, 'desc' => 'x - 0.8*sin(x) - 1.2'],
    ['name' => 'f18', 'func' => function($x) { return pow($x, 2.0) - exp($x) - 3.0*$x + 2.0; }, 'a' => 0.0, 'b' => 1.0, 'desc' => 'x^2 - exp(x) - 3x + 2'],
    ['name' => 'f19', 'func' => function($x) { return pow($x - 1.0, 3.0) + 4.0*pow($x - 1.0, 2.0) - 10.0; }, 'a' => 0.0, 'b' => 3.0, 'desc' => '(x-1)^3 + 4(x-1)^2 - 10'],
    ['name' => 'f20', 'func' => function($x) { return exp(pow($x, 2.0)) - exp(sqrt(2.0)*$x); }, 'a' => 0.5, 'b' => 1.5, 'desc' => 'exp(x^2) - exp(sqrt(2)*x)'],
    ['name' => 'f21', 'func' => function($x) { return (pow($x, 2.0) - 4.0)*($x + 1.5)*($x - 0.5); }, 'a' => 0.0, 'b' => 2.0, 'desc' => '(x^2-4)(x+1.5)(x-0.5)'],
    ['name' => 'f22', 'func' => function($x) { return pow($x, 3.0) - 3.0*pow($x, 2.0) - 4.0*$x + 13.0; }, 'a' => -3.0, 'b' => -2.0, 'desc' => 'x^3 - 3x^2 - 4x + 13'],
    ['name' => 'f23', 'func' => function($x) { return -0.9*pow($x, 2.0) + 1.7*$x + 2.5; }, 'a' => 2.8, 'b' => 3.0, 'desc' => '-0.9x^2 + 1.7x + 2.5'],
    ['name' => 'f24', 'func' => function($x) { return 1.0 - 0.61*$x; }, 'a' => 1.5, 'b' => 2.0, 'desc' => '1 - 0.61x (linear)'],
    ['name' => 'f25', 'func' => function($x) { return pow($x, 2.0) * abs(sin($x)) - 4.1; }, 'a' => 0.0, 'b' => 4.0, 'desc' => 'x^2*|sin(x)| - 4.1'],
    ['name' => 'f26', 'func' => function($x) { return pow($x, 5.0) - 3.0*pow($x, 4.0) + 25.0; }, 'a' => -3.0, 'b' => -1.0, 'desc' => 'x^5 - 3x^4 + 25'],
    ['name' => 'f27', 'func' => function($x) { return pow($x, 4.0) - 2.0*pow($x, 2.0) - 4.0; }, 'a' => 1.0, 'b' => 3.0, 'desc' => 'x^4 - 2x^2 - 4'],
    ['name' => 'f28', 'func' => function($x) { return $x - 0.5*sin($x) - 1.0; }, 'a' => 0.0, 'b' => 3.0, 'desc' => 'x - 0.5*sin(x) - 1'],
    ['name' => 'f29', 'func' => function($x) { return exp(-$x) - cos(3.0*$x) - 0.5; }, 'a' => 0.0, 'b' => 1.0, 'desc' => 'exp(-x) - cos(3x) - 0.5'],
    ['name' => 'f30', 'func' => function($x) { return ($x-1.0)*($x-2.0)*($x-3.0)*($x-4.0)*($x-5.0)*($x-6.0)*($x-7.0)*($x-8.0)*($x-9.0)*($x-10.0)*($x-11.0)*($x-12.0)*($x-13.0)*($x-14.0)*($x-15.0)*($x-16.0)*($x-17.0)*($x-18.0)*($x-19.0)*($x-20.0); }, 'a' => 0.0, 'b' => 1.5, 'desc' => 'Wilkinson-like deg-20 polynomial'],
    ['name' => 'f31', 'func' => function($x) { return ($x-1.0)*($x-2.0)*($x-3.0)*($x-4.0)*($x-5.0)*($x-6.0)*($x-7.0)*($x-8.0)*($x-9.0)*($x-10.0)*($x-11.0)*($x-12.0)*($x-13.0)*($x-14.0)*($x-15.0)*($x-16.0)*($x-17.0)*($x-18.0)*($x-19.0)*($x-20.0); }, 'a' => 19.0, 'b' => 21.0, 'desc' => 'Wilkinson-like deg-20 at root 20'],
    ['name' => 'f32', 'func' => function($x) { return pow($x, 4.0) + 2.0*pow($x, 2.0) - $x - 1.0; }, 'a' => -0.5, 'b' => 0.0, 'desc' => 'x^4 + 2x^2 - x - 1'],
    ['name' => 'f33', 'func' => function($x) { return pow($x, 4.0) - 10.0*pow($x, 3.0) + 35.0*pow($x, 2.0) - 50.0*$x + 24.0; }, 'a' => 0.0, 'b' => 1.5, 'desc' => 'x^4 - 10x^3 + 35x^2 - 50x + 24'],
    ['name' => 'f34', 'func' => function($x) { return 4.0*sin($x) - $x + 1.0; }, 'a' => -1.0, 'b' => 0.0, 'desc' => '4sin(x) - x + 1'],
    ['name' => 'f35', 'func' => function($x) { return pow($x, 25.0) - 1.0; }, 'a' => 0.0, 'b' => 2.0, 'desc' => 'x^25 - 1'],
    ['name' => 'f36', 'func' => function($x) { return pow($x - 1.8, 6.0) * ($x - 1.81); }, 'a' => 0.0, 'b' => 2.0, 'desc' => '(x-1.8)^6*(x-1.81) - near multiple root'],
    ['name' => 'f37', 'func' => function($x) { return sin(20.0*$x) - 0.3*$x; }, 'a' => 0.05, 'b' => 0.25, 'desc' => 'sin(20x) - 0.3x'],
    ['name' => 'f38', 'func' => function($x) { return pow($x, 4.0) + 2.0*pow($x, 3.0) - 13.0*pow($x, 2.0) - 14.0*$x + 24.0; }, 'a' => -3.0, 'b' => 1.0, 'desc' => 'x^4 + 2x^3 - 13x^2 - 14x + 24'],
    ['name' => 'f39', 'func' => function($x) { return exp(pow($x, 2.0)) - exp(1.2*$x); }, 'a' => 0.0, 'b' => 2.0, 'desc' => 'exp(x^2) - exp(1.2x)'],
    ['name' => 'f40', 'func' => function($x) { return pow($x, 5.0) - 3.0*pow($x, 4.0) + 2.0*pow($x, 3.0) - $x + 0.1; }, 'a' => -1.0, 'b' => 3.0, 'desc' => 'x^5 - 3x^4 + 2x^3 - x + 0.1'],
    ['name' => 'f41', 'func' => function($x) { return pow($x + 0.3, 7.0) - 0.01; }, 'a' => -2.0, 'b' => 1.0, 'desc' => '(x+0.3)^7 - 0.01'],
    ['name' => 'f42', 'func' => function($x) { return pow($x, 6.0) - 8.0*pow($x, 5.0) + 24.0*pow($x, 4.0) - 32.0*pow($x, 3.0) + 16.0*pow($x, 2.0); }, 'a' => 0.0, 'b' => 4.0, 'desc' => 'x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2'],
    ['name' => 'f43', 'func' => function($x) { return -2.0*log10(0.000027027 + 2.51/(10000000.0*sqrt($x))) - 1.0/sqrt($x); }, 'a' => 0.008, 'b' => 0.03, 'desc' => 'Colebrook-White friction factor'],
    ['name' => 'f44', 'func' => function($x) { return $x - 0.99*sin($x) - 2.0; }, 'a' => 2.0, 'b' => 3.0, 'desc' => 'Kepler equation (e=0.99)'],
    ['name' => 'f45', 'func' => function($x) { return (10.0 + 3.592/pow($x, 2.0))*($x - 0.04267) - 0.08206*300.0; }, 'a' => 2.0, 'b' => 3.0, 'desc' => 'Van der Waals (CO2)'],
    ['name' => 'f46', 'func' => function($x) { return $x*exp($x/2.0) - 1.5; }, 'a' => 0.0, 'b' => 1.0, 'desc' => 'x*exp(x/2) - 1.5'],
    ['name' => 'f47', 'func' => function($x) { return cos($x) + 1.0*pow(1.0 - cos($x), 2.0) - 0.05*pow($x, 2.0); }, 'a' => 3.0, 'b' => 6.0, 'desc' => 'Beam deflection equation'],
    ['name' => 'f48', 'func' => function($x) { return 0.05 - pow($x, 3.0)/((1.0 - $x)*pow(0.8 - 2.0*$x, 2.0)); }, 'a' => 0.01, 'b' => 0.3, 'desc' => 'Chemical equilibrium'],
];

$tol = 1e-14;
$maxIter = 10000;

echo "HybridRoots Benchmark Suite - PHP Port\n";
echo "======================================\n";

$funcs = ['HybridRoots\Core::mpbf', 'HybridRoots\Core::mpbfms', 'HybridRoots\Core::mptf', 'HybridRoots\Core::mptfms'];
$names = ["mpbf", "mpbfms", "mptf", "mptfms"];

$times = [0, 0, 0, 0];
$convs = [0, 0, 0, 0];
$iters = [0, 0, 0, 0];
$nfes = [0, 0, 0, 0];

foreach ($benchmarks as $i => $b) {
    printf("\n[%2d/48] %s: %s\n", $i + 1, $b['name'], $b['desc']);

    for ($a = 0; $a < 4; $a++) {
        $funcs[$a]($b['func'], $b['a'], $b['b'], $tol, $maxIter); // Warmup

        $runs = 100;
        $result = null;
        $start = hrtime(true);
        for ($r = 0; $r < $runs; $r++) {
            $result = $funcs[$a]($b['func'], $b['a'], $b['b'], $tol, $maxIter);
        }
        $end = hrtime(true);
        $elapsedUs = ($end - $start) / 1000.0 / $runs;

        if ($result->converged) {
            printf("       %-8s: root=%.10f, iter=%2d, nfe=%3d\n", $names[$a], $result->root, $result->iterations, $result->functionCalls);
            $times[$a] += $elapsedUs;
            $convs[$a]++;
            $iters[$a] += $result->iterations;
            $nfes[$a] += $result->functionCalls;
        } else {
            printf("       %-8s: FAILED\n", $names[$a]);
        }
    }
}

echo "\nSUMMARY\n";
echo "======================================\n";
echo "Algorithm  | Converged  | Total Time (us)    | Avg NFE    | Avg Iterations\n";
echo "--------------------------------------------------------------------------------\n";
for ($a = 0; $a < 4; $a++) {
    $avgNfe = $nfes[$a] / max(1, $convs[$a]);
    $avgIter = $iters[$a] / max(1, $convs[$a]);
    printf("%-10s | %2d/%-7d | %18.2f | %10.2f | %15.2f\n", $names[$a], $convs[$a], count($benchmarks), $times[$a], $avgNfe, $avgIter);
}
