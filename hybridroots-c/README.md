# HybridRoots (C Port)

**Four Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding**

A standard C99 library implementing four novel root-finding algorithms that combine bisection/trisection, false position, and modified secant methods for efficient, reliable nonlinear equation solving.

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

You can copy `include/hybridroots.h` and `src/hybridroots.c` directly into your project, or use CMake's `FetchContent`:

```cmake
include(FetchContent)
FetchContent_Declare(
  hybridroots
  GIT_REPOSITORY https://github.com/Abdelrhman-Ellithy/hybridroots.git
  GIT_TAG        v1.0.0
)
FetchContent_MakeAvailable(hybridroots)
target_link_libraries(your_target PRIVATE hybridroots)
```

## Usage

```c
#include <stdio.h>
#include "hybridroots.h"

double my_func(double x) {
    return x*x*x - x - 2;
}

int main() {
    // Find root of x^3 - x - 2 in interval [1.0, 2.0] using Opt.TFMS
    HybridRootsResult result = mptfms(my_func, 1.0, 2.0, 1e-14, 10000);
    
    printf("Root: %.15f\n", result.root);
    printf("Iterations: %d\n", result.iterations);
    printf("Converged: %d\n", result.converged);
    return 0;
}
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
