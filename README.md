<div align="center">
  <table border="0" align="center">
    <tr>
      <td align="center">
        <h2>HybridRoots: Multi-Phase Hybrid Bracketing Algorithms</h2>
      </td>
    </tr>
    <tr>
       <td align="center">
          <a href="https://pypi.org/project/hybridroots/" target="_blank">
              <img alt="Python" src="https://img.shields.io/pypi/v/hybridroots?style=for-the-badge&color=blue&label=Python&logo=python">
          </a>
          <a href="https://crates.io/crates/hybridroots" target="_blank">
              <img alt="Rust" src="https://img.shields.io/crates/v/hybridroots?style=for-the-badge&color=orange&label=Rust&logo=rust">
          </a>
          <a href="https://central.sonatype.com/artifact/io.github.abdelrhman-ellithy/hybridroots" target="_blank">
              <img alt="Java" src="https://img.shields.io/maven-central/v/io.github.abdelrhman-ellithy/hybridroots?style=for-the-badge&color=red&label=Java&logo=java">
          </a>
          <a href="https://www.nuget.org/packages/HybridRoots/" target="_blank">
              <img alt="C#" src="https://img.shields.io/nuget/v/HybridRoots?style=for-the-badge&color=blueviolet&label=C%23&logo=dotnet">
          </a>
          <a href="https://www.npmjs.com/package/hybridroots" target="_blank">
              <img alt="Node" src="https://img.shields.io/npm/v/hybridroots?style=for-the-badge&color=cb3837&label=JS%2FTS&logo=npm">
          </a>
          <a href="https://packagist.org/packages/abdelrhman-ellithy/hybridroots" target="_blank">
              <img alt="PHP" src="https://img.shields.io/packagist/v/abdelrhman-ellithy/hybridroots?style=for-the-badge&color=8892BF&label=PHP&logo=php">
          </a>
          <a href="https://github.com/Abdelrhman-Ellithy/hybridroots/tree/main/hybridroots-c" target="_blank">
              <img alt="C" src="https://img.shields.io/badge/C-Source-A8B9CC?style=for-the-badge&logo=c">
          </a>
          <a href="https://github.com/Abdelrhman-Ellithy/hybridroots/tree/main/hybridroots-cpp" target="_blank">
              <img alt="C++" src="https://img.shields.io/badge/C++-Header%20Only-00599C?style=for-the-badge&logo=c%2B%2B">
          </a>
      </td>
    </tr>
  </table>
</div>

# Four New Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding

**Author:** Abdelrahman Ellithy

**Abstract:**
This repository contains the official implementation, experiments, and results for the paper "Four New Multi-Phase Hybrid Bracketing Algorithms for Numerical Root Finding", published in the **Journal of the Egyptian Mathematical Society (JOEM)** via **National Information and Documentation Centre (NIDOC), Academy of Scientific Research and Technology, ASRT**.

* **Paper Link:** [https://joems.journals.ekb.eg/article_498939.html](https://joems.journals.ekb.eg/article_498939.html)
* **DOI:** [10.21608/joems.2026.440115.1078](https://doi.org/10.21608/joems.2026.440115.1078)

The paper introduces four novel hybrid algorithms that combine classical bracketing methods (Bisection, Trisection, False Position) with accelerated steps (Modified Secant) to achieve superior convergence rates while maintaining guaranteed bracketing.

### 🚀 Available Packages
These algorithms are fully implemented and published as native packages for 8 languages:
1. **Python** (PyPI): [hybridroots](https://pypi.org/project/hybridroots/)
2. **Rust** (crates.io): [hybridroots](https://crates.io/crates/hybridroots)
3. **Java** (Maven Central): [io.github.abdelrhman-ellithy:hybridroots](https://central.sonatype.com/artifact/io.github.abdelrhman-ellithy/hybridroots)
4. **C# / .NET** (NuGet): [HybridRoots](https://www.nuget.org/packages/HybridRoots/)
5. **JavaScript / TypeScript** (npm): [hybridroots](https://www.npmjs.com/package/hybridroots)
6. **PHP** (Packagist): [abdelrhman-ellithy/hybridroots](https://packagist.org/packages/abdelrhman-ellithy/hybridroots)
7. **C**: [Source files available here](https://github.com/Abdelrhman-Ellithy/hybridroots/tree/main/hybridroots-c)
8. **C++**: [Header-only available here](https://github.com/Abdelrhman-Ellithy/hybridroots/tree/main/hybridroots-cpp)

---

## The Algorithms

All algorithms are deterministic and guarantee convergence for continuous functions with a valid bracket `f(a) * f(b) < 0`.

Every algorithm returns a standardized **`HybridRootsResult`** object containing:

| Field | Description |
|-------|-------------|
| `root` | Estimated root location |
| `iterations` | Number of iterations performed |
| `function_calls` | Number of function evaluations |
| `converged` | Whether `|f(root)| <= tol` |

### 1. Opt.BFMS (`mpbfms`)
**Multi-Phase Bisection–False Position–Modified Secant** — Extends Opt.BF with a modified secant acceleration step. (Section 3)

### 2. Opt.TFMS (`mptfms`)
**Multi-Phase Trisection–False Position–Modified Secant** — Combines trisection, false position, and modified secant for maximum efficiency. The fastest of the four. (Section 5)

### 3. Opt.BF (`mpbf`)
**Multi-Phase Bisection–False Position** — Combines the reliability of bisection with the speed of the false position method. (Section 2)

### 4. Opt.TF (`mptf`)
**Multi-Phase Trisection–False Position** — Uses trisection for faster interval reduction, followed by false position refinement. (Section 4)

**Common signature:** `(f, a, b, tol=1e-14, max_iter=10000)` → `HybridRootsResult`

---

## Repository Structure

```
├── hybridroots-python/    # Python (pip) – reference implementation
├── hybridroots-c/         # C (CMake)
├── hybridroots-cpp/       # C++ (CMake, header-only)
├── hybridroots-java/      # Java (Maven Central)
├── hybridroots-dotnet/    # C# / .NET (NuGet)
├── hybridroots-rust/      # Rust (crates.io)
├── hybridroots-js/        # JavaScript (npm)
├── hybridroots-php/       # PHP (Packagist / Composer)
└── Paper Experiment and Results/
```

---

## Quick Start by Language

### Python

```bash
pip install hybridroots
```

```python
from hybridroots import mptfms

root, info = mptfms(lambda x: x**3 - x - 2, 1, 2)
print(f"Root: {root:.15f}")
print(f"Iterations: {info['iterations']}, NFE: {info['function_calls']}, Converged: {info['converged']}")
```

### Java

```xml
<!-- Add to your pom.xml -->
<dependency>
    <groupId>com.hybridroots</groupId>
    <artifactId>hybridroots</artifactId>
    <version>1.0.0</version>
</dependency>
```

```java
import com.hybridroots.HybridRoots;
import com.hybridroots.HybridRootsResult;

HybridRootsResult result = HybridRoots.mptfms(x -> x * x * x - x - 2, 1.0, 2.0);
System.out.println("Root: " + result.root);           // root value
System.out.println("Converged: " + result.converged);  // true
```

### C# (.NET)

```xml
<!-- Add to your .csproj -->
<PackageReference Include="HybridRoots" Version="1.0.0" />
```

```csharp
using HybridRoots;

var result = Core.Mptfms(x => x * x * x - x - 2, 1.0, 2.0);
Console.WriteLine($"Root: {result.Root}, Converged: {result.Converged}");
```

### Rust

```toml
# Add to your Cargo.toml
[dependencies]
hybridroots = "1.0.0"
```

```rust
use hybridroots::mptfms;

let result = mptfms(&|x: f64| x.powi(3) - x - 2.0, 1.0, 2.0, 1e-14, 10000);
println!("Root: {}, Converged: {}", result.root, result.converged);
```

### JavaScript (Node.js)

```bash
npm install hybridroots
```

```javascript
import { mptfms } from 'hybridroots';

const result = mptfms(x => x**3 - x - 2, 1, 2);
console.log(`Root: ${result.root}, Converged: ${result.converged}`);
```

### C++

```cpp
#include "hybridroots.hpp"

auto result = hybridroots::mptfms([](double x) { return x*x*x - x - 2; }, 1.0, 2.0);
printf("Root: %.15f, Converged: %d\n", result.root, result.converged);
```

### C

```c
#include "hybridroots.h"

double f(double x) { return x*x*x - x - 2; }

HybridRootsResult result = mptfms(f, 1.0, 2.0, 1e-14, 10000);
printf("Root: %.15f, Converged: %d\n", result.root, result.converged);
```

### PHP

```json
{ "require": { "abdelrhman-ellithy/hybridroots": "^1.0" } }
```
```php
use HybridRoots\Core;

$result = Core::mptfms(fn($x) => $x**3 - $x - 2, 1.0, 2.0);
echo "Root: {$result->root}, Converged: " . ($result->converged ? 'true' : 'false');
```

---

## Running Benchmarks

Each port includes a benchmark suite of 48 test functions. Here's how to run them:

### Python
```bash
cd hybridroots-python
pip install -e .
python -m hybridroots.benchmarks
```

### Java
```bash
cd hybridroots-java
mvn clean package -q
mvn exec:java "-Dexec.mainClass=com.hybridroots.Benchmarks"
```

### C# (.NET)
```bash
cd hybridroots-dotnet
dotnet run -c Release
```

### Rust
```bash
cd hybridroots-rust
cargo run --release --bin benchmarks
```

### JavaScript
```bash
cd hybridroots-js
node benchmarks.js
```

### C++
```bash
cd hybridroots-cpp
cmake -B build -S .
cmake --build build --config Release
./build/benchmarks       # Linux/macOS
.\build\benchmarks.exe   # Windows
```

### C
```bash
cd hybridroots-c
cmake -B build -S .
cmake --build build --config Release
./build/benchmarks       # Linux/macOS
.\build\benchmarks.exe   # Windows
```

### PHP
```bash
cd hybridroots-php
php benchmarks.php
```

---


### C / C++
C and C++ libraries are typically distributed as source. Users include the header and source files directly, or use CMake's `FetchContent`:

```cmake
# In the user's CMakeLists.txt:
include(FetchContent)
FetchContent_Declare(
  hybridroots
  GIT_REPOSITORY https://github.com/Abdelrhman-Ellithy/hybridroots.git
  GIT_TAG        v1.0.0
)
FetchContent_MakeAvailable(hybridroots)
target_link_libraries(myapp PRIVATE hybridroots)
```

For system-wide install:
```bash
cd hybridroots-c   # or hybridroots-cpp
cmake -B build -S . -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build build
cmake --install build
```

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
  publisher={National Information and Documentation Centre (NIDOC), Academy of Scientific Research and Technology, ASRT}
}
```

## License

MIT License — See [LICENSE](./LICENSE) for details.
