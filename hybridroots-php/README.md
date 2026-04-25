# HybridRoots (PHP Port)

**Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding**

A PHP library implementing four novel root-finding algorithms that combine bisection/trisection, false position, and modified secant methods for efficient, reliable nonlinear equation solving.

## Why HybridRoots is Powerful

Classical root-finding algorithms face a tradeoff: methods like Bisection are 100% reliable but slow (averaging >40 iterations), while methods like Secant or Newton-Raphson are fast but can fail to converge or shoot out of bounds.

HybridRoots solves this by introducing multi-phase bracketing:
1. **Guaranteed Convergence**: It maintains a strict bracket `[a, b]` where `f(a) * f(b) < 0` at all times.
2. **Superior Speed**: By combining Trisection, False Position, and an adaptive Modified Secant step, it drastically reduces the search space. The `mptfms` algorithm converges in an average of just **2.33 iterations** across 48 complex benchmark functions.

### The Algorithms
- **Opt.BFMS (`mpbfms`)**: Bisection + False Position + Modified Secant (Avg 2.69 iterations)
- **Opt.TFMS (`mptfms`)**: Trisection + False Position + Modified Secant (Avg 2.33 iterations)
- **Opt.BF (`mpbf`)**: Bisection + False Position (Avg 6.58 iterations)
- **Opt.TF (`mptf`)**: Trisection + False Position (Avg 5.19 iterations)

## Installation

```json
{
    "require": {
        "abdelrhman-ellithy/hybridroots": "^1.0"
    }
}
```
Or via CLI:
```bash
composer require abdelrhman-ellithy/hybridroots
```

## Usage

```php
<?php
require 'vendor/autoload.php';

use HybridRoots\Core;

// Find root of x^3 - x - 2 in interval [1.0, 2.0] using Opt.TFMS
$result = Core::mptfms(fn($x) => $x**3 - $x - 2, 1.0, 2.0);

echo "Root: {$result->root}\n";
echo "Iterations: {$result->iterations}\n";
echo "Converged: " . ($result->converged ? 'true' : 'false') . "\n";
```

## Citation

If you use this package in your research, please cite:

```bibtex
@article{ellithy2026hybrid,
  title={Four New Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding},
  author={Ellithy, Abdelrahman},
  journal={Journal of the Egyptian Mathematical Society},
  volume={34},
  year={2026},
  publisher={National Information and Documentation Centre (NIDOC), Academy of Scientific Research and Technology, ASRT}
}
```

- **Paper DOI:** [10.21608/joems.2026.440115.1078](https://doi.org/10.21608/joems.2026.440115.1078)
