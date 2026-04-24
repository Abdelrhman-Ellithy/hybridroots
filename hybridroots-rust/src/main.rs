use std::time::Instant;
use hybridroots::*;

struct BenchmarkDef<'a> {
    name: &'a str,
    func: fn(f64) -> f64,
    a: f64,
    b: f64,
    desc: &'a str,
}

fn main() {
    let benchmarks = vec![
        BenchmarkDef { name: "f1", func: |x| x * f64::exp(x) - 7.0, a: 1.0, b: 2.0, desc: "x*exp(x) - 7" },
        BenchmarkDef { name: "f2", func: |x| f64::powf(x, 3.0) - x - 1.0, a: 1.0, b: 2.0, desc: "x^3 - x - 1" },
        BenchmarkDef { name: "f3", func: |x| f64::powf(x, 2.0) - x - 2.0, a: 1.0, b: 4.0, desc: "x^2 - x - 2" },
        BenchmarkDef { name: "f4", func: |x| x - f64::cos(x), a: 0.0, b: 1.0, desc: "x - cos(x)" },
        BenchmarkDef { name: "f5", func: |x| f64::powf(x, 2.0) - 10.0, a: 3.0, b: 4.0, desc: "x^2 - 10" },
        BenchmarkDef { name: "f6", func: |x| f64::sin(x) - f64::powf(x, 2.0), a: 0.5, b: 1.0, desc: "sin(x) - x^2" },
        BenchmarkDef { name: "f7", func: |x| x + f64::ln(x), a: 0.1, b: 1.0, desc: "x + ln(x)" },
        BenchmarkDef { name: "f8", func: |x| f64::exp(x) - 3.0*x - 2.0, a: 2.0, b: 3.0, desc: "exp(x) - 3x - 2" },
        BenchmarkDef { name: "f9", func: |x| f64::powf(x, 2.0) + f64::exp(x/2.0) - 5.0, a: 1.0, b: 2.0, desc: "x^2 + exp(x/2) - 5" },
        BenchmarkDef { name: "f10", func: |x| x * f64::sin(x) - 1.0, a: 0.0, b: 2.0, desc: "x*sin(x) - 1" },
        BenchmarkDef { name: "f11", func: |x| x * f64::cos(x) + 1.0, a: -2.0, b: 4.0, desc: "x*cos(x) + 1" },
        BenchmarkDef { name: "f12", func: |x| f64::powf(x, 10.0) - 1.0, a: 0.0, b: 1.3, desc: "x^10 - 1" },
        BenchmarkDef { name: "f13", func: |x| f64::powf(x, 2.0) + 2.0*x - 7.0, a: 1.0, b: 3.0, desc: "x^2 + 2x - 7" },
        BenchmarkDef { name: "f14", func: |x| f64::powf(x, 3.0) - 2.0*x - 5.0, a: 2.0, b: 3.0, desc: "x^3 - 2x - 5" },
        BenchmarkDef { name: "f15", func: |x| f64::exp(x) - 3.0*f64::powf(x, 2.0), a: 0.0, b: 1.0, desc: "exp(x) - 3x^2" },
        BenchmarkDef { name: "f16", func: |x| f64::sin(10.0*x) - 0.5*x, a: 0.1, b: 0.4, desc: "sin(10x) - 0.5x" },
        BenchmarkDef { name: "f17", func: |x| x - 0.8*f64::sin(x) - 1.2, a: 1.0, b: 3.0, desc: "x - 0.8*sin(x) - 1.2" },
        BenchmarkDef { name: "f18", func: |x| f64::powf(x, 2.0) - f64::exp(x) - 3.0*x + 2.0, a: 0.0, b: 1.0, desc: "x^2 - exp(x) - 3x + 2" },
        BenchmarkDef { name: "f19", func: |x| f64::powf(x - 1.0, 3.0) + 4.0*f64::powf(x - 1.0, 2.0) - 10.0, a: 0.0, b: 3.0, desc: "(x-1)^3 + 4(x-1)^2 - 10" },
        BenchmarkDef { name: "f20", func: |x| f64::exp(f64::powf(x, 2.0)) - f64::exp(f64::sqrt(2.0)*x), a: 0.5, b: 1.5, desc: "exp(x^2) - exp(sqrt(2)*x)" },
        BenchmarkDef { name: "f21", func: |x| (f64::powf(x, 2.0) - 4.0)*(x + 1.5)*(x - 0.5), a: 0.0, b: 2.0, desc: "(x^2-4)(x+1.5)(x-0.5)" },
        BenchmarkDef { name: "f22", func: |x| f64::powf(x, 3.0) - 3.0*f64::powf(x, 2.0) - 4.0*x + 13.0, a: -3.0, b: -2.0, desc: "x^3 - 3x^2 - 4x + 13" },
        BenchmarkDef { name: "f23", func: |x| -0.9*f64::powf(x, 2.0) + 1.7*x + 2.5, a: 2.8, b: 3.0, desc: "-0.9x^2 + 1.7x + 2.5" },
        BenchmarkDef { name: "f24", func: |x| 1.0 - 0.61*x, a: 1.5, b: 2.0, desc: "1 - 0.61x (linear)" },
        BenchmarkDef { name: "f25", func: |x| f64::powf(x, 2.0) * f64::abs(f64::sin(x)) - 4.1, a: 0.0, b: 4.0, desc: "x^2*|sin(x)| - 4.1" },
        BenchmarkDef { name: "f26", func: |x| f64::powf(x, 5.0) - 3.0*f64::powf(x, 4.0) + 25.0, a: -3.0, b: -1.0, desc: "x^5 - 3x^4 + 25" },
        BenchmarkDef { name: "f27", func: |x| f64::powf(x, 4.0) - 2.0*f64::powf(x, 2.0) - 4.0, a: 1.0, b: 3.0, desc: "x^4 - 2x^2 - 4" },
        BenchmarkDef { name: "f28", func: |x| x - 0.5*f64::sin(x) - 1.0, a: 0.0, b: 3.0, desc: "x - 0.5*sin(x) - 1" },
        BenchmarkDef { name: "f29", func: |x| f64::exp(-x) - f64::cos(3.0*x) - 0.5, a: 0.0, b: 1.0, desc: "exp(-x) - cos(3x) - 0.5" },
        BenchmarkDef { name: "f30", func: |x| (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), a: 0.0, b: 1.5, desc: "Wilkinson-like deg-20 polynomial" },
        BenchmarkDef { name: "f31", func: |x| (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), a: 19.0, b: 21.0, desc: "Wilkinson-like deg-20 at root 20" },
        BenchmarkDef { name: "f32", func: |x| f64::powf(x, 4.0) + 2.0*f64::powf(x, 2.0) - x - 1.0, a: -0.5, b: 0.0, desc: "x^4 + 2x^2 - x - 1" },
        BenchmarkDef { name: "f33", func: |x| f64::powf(x, 4.0) - 10.0*f64::powf(x, 3.0) + 35.0*f64::powf(x, 2.0) - 50.0*x + 24.0, a: 0.0, b: 1.5, desc: "x^4 - 10x^3 + 35x^2 - 50x + 24" },
        BenchmarkDef { name: "f34", func: |x| 4.0*f64::sin(x) - x + 1.0, a: -1.0, b: 0.0, desc: "4sin(x) - x + 1" },
        BenchmarkDef { name: "f35", func: |x| f64::powf(x, 25.0) - 1.0, a: 0.0, b: 2.0, desc: "x^25 - 1" },
        BenchmarkDef { name: "f36", func: |x| f64::powf(x - 1.8, 6.0) * (x - 1.81), a: 0.0, b: 2.0, desc: "(x-1.8)^6*(x-1.81) - near multiple root" },
        BenchmarkDef { name: "f37", func: |x| f64::sin(20.0*x) - 0.3*x, a: 0.1, b: 0.2, desc: "sin(20x) - 0.3x" },
        BenchmarkDef { name: "f38", func: |x| f64::powf(x, 4.0) + 2.0*f64::powf(x, 3.0) - 13.0*f64::powf(x, 2.0) - 14.0*x + 24.0, a: -3.0, b: 1.0, desc: "x^4 + 2x^3 - 13x^2 - 14x + 24" },
        BenchmarkDef { name: "f39", func: |x| f64::exp(f64::powf(x, 2.0)) - f64::exp(1.2*x), a: 0.0, b: 2.0, desc: "exp(x^2) - exp(1.2x)" },
        BenchmarkDef { name: "f40", func: |x| f64::powf(x, 5.0) - 3.0*f64::powf(x, 4.0) + 2.0*f64::powf(x, 3.0) - x + 0.1, a: -1.0, b: 3.0, desc: "x^5 - 3x^4 + 2x^3 - x + 0.1" },
        BenchmarkDef { name: "f41", func: |x| f64::powf(x + 0.3, 7.0) - 0.01, a: -2.0, b: 1.0, desc: "(x+0.3)^7 - 0.01" },
        BenchmarkDef { name: "f42", func: |x| f64::powf(x, 6.0) - 8.0*f64::powf(x, 5.0) + 24.0*f64::powf(x, 4.0) - 32.0*f64::powf(x, 3.0) + 16.0*f64::powf(x, 2.0), a: 0.0, b: 4.0, desc: "x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2" },
        BenchmarkDef { name: "f43", func: |x| -2.0*f64::log10(0.000027027 + 2.51/(10000000.0*f64::sqrt(x))) - 1.0/f64::sqrt(x), a: 0.0, b: 0.0, desc: "Colebrook-White friction factor" },
        BenchmarkDef { name: "f44", func: |x| x - 0.99*f64::sin(x) - 2.0, a: 2.0, b: 3.0, desc: "Kepler equation (e=0.99)" },
        BenchmarkDef { name: "f45", func: |x| (10.0 + 3.592/f64::powf(x, 2.0))*(x - 0.04267) - 0.08206*300.0, a: 2.0, b: 3.0, desc: "Van der Waals (CO2)" },
        BenchmarkDef { name: "f46", func: |x| x*f64::exp(x/2.0) - 1.5, a: 0.0, b: 1.0, desc: "x*exp(x/2) - 1.5" },
        BenchmarkDef { name: "f47", func: |x| f64::cos(x) + 1.0*f64::powf(1.0 - f64::cos(x), 2.0) - 0.05*f64::powf(x, 2.0), a: 3.0, b: 6.0, desc: "Beam deflection equation" },
        BenchmarkDef { name: "f48", func: |x| 0.05 - f64::powf(x, 3.0)/((1.0 - x)*f64::powf(0.8 - 2.0*x, 2.0)), a: 0.0, b: 0.3, desc: "Chemical equilibrium" },
    ];

    let tol = 1e-14;
    let max_iter = 10000;

    println!("HybridRoots Benchmark Suite - Rust Port");
    println!("======================================");

    let mut times = vec![0.0; 4];
    let mut convs = vec![0; 4];
    let mut iters = vec![0; 4];
    let mut nfes = vec![0; 4];

    type AlgType = fn(&(dyn Fn(f64) -> f64), f64, f64, f64, usize) -> (f64, HybridRootsInfo);
    
    // We wrap functions so they match the expected signature dynamically or just use simple closure array
    let names = ["mpbf", "mpbfms", "mptf", "mptfms"];

    for (i, b) in benchmarks.iter().enumerate() {
        println!("\n[{:2}/48] {}: {}", i + 1, b.name, b.desc);

        for a in 0..4 {
            let func: AlgType = match a {
                0 => |f, a, b, t, m| mpbf(f, a, b, t, m),
                1 => |f, a, b, t, m| mpbfms(f, a, b, t, m),
                2 => |f, a, b, t, m| mptf(f, a, b, t, m),
                3 => |f, a, b, t, m| mptfms(f, a, b, t, m),
                _ => unreachable!(),
            };

            // Warmup
            func(&b.func, b.a, b.b, tol, max_iter);

            let runs = 100;
            let mut root = 0.0;
            let mut last_info = HybridRootsInfo { iterations: 0, function_calls: 0, converged: false };
            
            let start = Instant::now();
            for _ in 0..runs {
                let (r, info) = func(&b.func, b.a, b.b, tol, max_iter);
                root = r;
                last_info = info;
            }
            let elapsed_us = start.elapsed().as_nanos() as f64 / 1000.0 / runs as f64;

            if last_info.converged {
                println!("       {:-8}: root={:.10}, iter={:2}, nfe={:3}", names[a], root, last_info.iterations, last_info.function_calls);
                times[a] += elapsed_us;
                convs[a] += 1;
                iters[a] += last_info.iterations;
                nfes[a] += last_info.function_calls;
            } else {
                println!("       {:-8}: FAILED", names[a]);
            }
        }
    }

    println!("\nSUMMARY");
    println!("======================================");
    println!("Algorithm  | Converged  | Total Time (us)    | Avg NFE    | Avg Iterations");
    println!("--------------------------------------------------------------------------------");
    for a in 0..4 {
        let avg_nfe = nfes[a] as f64 / convs[a] as f64;
        let avg_iter = iters[a] as f64 / convs[a] as f64;
        println!("{:-10} | {:2}/{:-7} | {:18.2} | {:10.2} | {:15.2}", names[a], convs[a], benchmarks.len(), times[a], avg_nfe, avg_iter);
    }
}
