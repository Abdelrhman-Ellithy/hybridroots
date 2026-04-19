# Four New Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding

**Authors:** Abdelrahman Ellithy

**Abstract:**
This repository contains the official implementation, experiments, and results for the paper "Four New Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding", published in the **Journal of the Egyptian Mathematical Society (JOEM)** via **Springer**.

* **Paper Link:** [https://joems.journals.ekb.eg/article_498939.html](https://joems.journals.ekb.eg/article_498939.html)
* **DOI:** [10.21608/joems.2026.440115.1078](https://doi.org/10.21608/joems.2026.440115.1078)

The paper introduces four novel hybrid algorithms that combine classical bracketing methods (Bisection, Trisection, False Position) with accelerated steps (Modified Secant) to achieve superior convergence rates while maintaining guaranteed bracketing.

---

## Repository Structure

This repository is organized into the following components:

- **[hybridroots python package/](./hybridroots python package/)**
  The production-ready Python package implementation of the algorithms. Use this for installing and using the algorithms in your own projects.
  
- **[Paper Experiment and Results/](./Paper Experiment and Results/)**
  Contains the raw experimental data, benchmark scripts, and analysis results used in the paper.
  
---

## The Algorithms

All algorithms are deterministic and guarantee convergence for continuous functions with a valid bracket.

### 1. Opt.BF (`mpbf`)
**Multi-Phase Bisection-False Position**
Combines the reliability of bisection with the speed of the false position method.
- **Signature:** `mpbf(f, a, b, tol=1e-14, max_iter=10000)`

### 2. Opt.BFMS (`mpbfms`)
**Multi-Phase Bisection-False Position-Modified Secant**
Extends Opt.BF by adding a modified secant step with adaptive delta for faster convergence.
- **Signature:** `mpbfms(f, a, b, tol=1e-14, max_iter=10000)`

### 3. Opt.TF (`mptf`)
**Multi-Phase Trisection-False Position**
Uses trisection (dividing interval into thirds) for faster interval reduction, followed by false position refinement.
- **Signature:** `mptf(f, a, b, tol=1e-14, max_iter=10000)`

### 4. Opt.TFMS (`mptfms`)
**Multi-Phase Trisection-False Position-Modified Secant**
Combines trisection, false position, and modified secant steps for maximum efficiency.
- **Signature:** `mptfms(f, a, b, tol=1e-14, max_iter=10000)`

---

## Citation

If you use this work, please cite:

```bibtex
@article{ellithy2026hybrid,
  title={Four New Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding},
  author={Ellithy, Abdelrahman},
  journal={Journal of the Egyptian Mathematical Society},
  volume={34},
  year={2026},
  publisher={Springer}
}
```

## License

See [LICENSE](./LICENSE) for details.
