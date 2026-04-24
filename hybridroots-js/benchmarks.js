import { mpbf, mpbfms, mptf, mptfms } from './core.js';

const benchmarks = [
    { name: 'f1', func: x => x * Math.exp(x) - 7.0, a: 1.0, b: 2.0, desc: 'x*exp(x) - 7' },
    { name: 'f2', func: x => Math.pow(x, 3.0) - x - 1.0, a: 1.0, b: 2.0, desc: 'x^3 - x - 1' },
    { name: 'f3', func: x => Math.pow(x, 2.0) - x - 2.0, a: 1.0, b: 4.0, desc: 'x^2 - x - 2' },
    { name: 'f4', func: x => x - Math.cos(x), a: 0.0, b: 1.0, desc: 'x - cos(x)' },
    { name: 'f5', func: x => Math.pow(x, 2.0) - 10.0, a: 3.0, b: 4.0, desc: 'x^2 - 10' },
    { name: 'f6', func: x => Math.sin(x) - Math.pow(x, 2.0), a: 0.5, b: 1.0, desc: 'sin(x) - x^2' },
    { name: 'f7', func: x => x + Math.log(x), a: 0.1, b: 1.0, desc: 'x + ln(x)' },
    { name: 'f8', func: x => Math.exp(x) - 3.0*x - 2.0, a: 2.0, b: 3.0, desc: 'exp(x) - 3x - 2' },
    { name: 'f9', func: x => Math.pow(x, 2.0) + Math.exp(x/2.0) - 5.0, a: 1.0, b: 2.0, desc: 'x^2 + exp(x/2) - 5' },
    { name: 'f10', func: x => x * Math.sin(x) - 1.0, a: 0.0, b: 2.0, desc: 'x*sin(x) - 1' },
    { name: 'f11', func: x => x * Math.cos(x) + 1.0, a: -2.0, b: 4.0, desc: 'x*cos(x) + 1' },
    { name: 'f12', func: x => Math.pow(x, 10.0) - 1.0, a: 0.0, b: 1.3, desc: 'x^10 - 1' },
    { name: 'f13', func: x => Math.pow(x, 2.0) + 2.0*x - 7.0, a: 1.0, b: 3.0, desc: 'x^2 + 2x - 7' },
    { name: 'f14', func: x => Math.pow(x, 3.0) - 2.0*x - 5.0, a: 2.0, b: 3.0, desc: 'x^3 - 2x - 5' },
    { name: 'f15', func: x => Math.exp(x) - 3.0*Math.pow(x, 2.0), a: 0.0, b: 1.0, desc: 'exp(x) - 3x^2' },
    { name: 'f16', func: x => Math.sin(10.0*x) - 0.5*x, a: 0.1, b: 0.4, desc: 'sin(10x) - 0.5x' },
    { name: 'f17', func: x => x - 0.8*Math.sin(x) - 1.2, a: 1.0, b: 3.0, desc: 'x - 0.8*sin(x) - 1.2' },
    { name: 'f18', func: x => Math.pow(x, 2.0) - Math.exp(x) - 3.0*x + 2.0, a: 0.0, b: 1.0, desc: 'x^2 - exp(x) - 3x + 2' },
    { name: 'f19', func: x => Math.pow(x - 1.0, 3.0) + 4.0*Math.pow(x - 1.0, 2.0) - 10.0, a: 0.0, b: 3.0, desc: '(x-1)^3 + 4(x-1)^2 - 10' },
    { name: 'f20', func: x => Math.exp(Math.pow(x, 2.0)) - Math.exp(Math.sqrt(2.0)*x), a: 0.5, b: 1.5, desc: 'exp(x^2) - exp(sqrt(2)*x)' },
    { name: 'f21', func: x => (Math.pow(x, 2.0) - 4.0)*(x + 1.5)*(x - 0.5), a: 0.0, b: 2.0, desc: '(x^2-4)(x+1.5)(x-0.5)' },
    { name: 'f22', func: x => Math.pow(x, 3.0) - 3.0*Math.pow(x, 2.0) - 4.0*x + 13.0, a: -3.0, b: -2.0, desc: 'x^3 - 3x^2 - 4x + 13' },
    { name: 'f23', func: x => -0.9*Math.pow(x, 2.0) + 1.7*x + 2.5, a: 2.8, b: 3.0, desc: '-0.9x^2 + 1.7x + 2.5' },
    { name: 'f24', func: x => 1.0 - 0.61*x, a: 1.5, b: 2.0, desc: '1 - 0.61x (linear)' },
    { name: 'f25', func: x => Math.pow(x, 2.0) * Math.abs(Math.sin(x)) - 4.1, a: 0.0, b: 4.0, desc: 'x^2*|sin(x)| - 4.1' },
    { name: 'f26', func: x => Math.pow(x, 5.0) - 3.0*Math.pow(x, 4.0) + 25.0, a: -3.0, b: -1.0, desc: 'x^5 - 3x^4 + 25' },
    { name: 'f27', func: x => Math.pow(x, 4.0) - 2.0*Math.pow(x, 2.0) - 4.0, a: 1.0, b: 3.0, desc: 'x^4 - 2x^2 - 4' },
    { name: 'f28', func: x => x - 0.5*Math.sin(x) - 1.0, a: 0.0, b: 3.0, desc: 'x - 0.5*sin(x) - 1' },
    { name: 'f29', func: x => Math.exp(-x) - Math.cos(3.0*x) - 0.5, a: 0.0, b: 1.0, desc: 'exp(-x) - cos(3x) - 0.5' },
    { name: 'f30', func: x => (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), a: 0.0, b: 1.5, desc: 'Wilkinson-like deg-20 polynomial' },
    { name: 'f31', func: x => (x-1.0)*(x-2.0)*(x-3.0)*(x-4.0)*(x-5.0)*(x-6.0)*(x-7.0)*(x-8.0)*(x-9.0)*(x-10.0)*(x-11.0)*(x-12.0)*(x-13.0)*(x-14.0)*(x-15.0)*(x-16.0)*(x-17.0)*(x-18.0)*(x-19.0)*(x-20.0), a: 19.0, b: 21.0, desc: 'Wilkinson-like deg-20 at root 20' },
    { name: 'f32', func: x => Math.pow(x, 4.0) + 2.0*Math.pow(x, 2.0) - x - 1.0, a: -0.5, b: 0.0, desc: 'x^4 + 2x^2 - x - 1' },
    { name: 'f33', func: x => Math.pow(x, 4.0) - 10.0*Math.pow(x, 3.0) + 35.0*Math.pow(x, 2.0) - 50.0*x + 24.0, a: 0.0, b: 1.5, desc: 'x^4 - 10x^3 + 35x^2 - 50x + 24' },
    { name: 'f34', func: x => 4.0*Math.sin(x) - x + 1.0, a: -1.0, b: 0.0, desc: '4sin(x) - x + 1' },
    { name: 'f35', func: x => Math.pow(x, 25.0) - 1.0, a: 0.0, b: 2.0, desc: 'x^25 - 1' },
    { name: 'f36', func: x => Math.pow(x - 1.8, 6.0) * (x - 1.81), a: 0.0, b: 2.0, desc: '(x-1.8)^6*(x-1.81) - near multiple root' },
    { name: 'f37', func: x => Math.sin(20.0*x) - 0.3*x, a: 0.05, b: 0.25, desc: 'sin(20x) - 0.3x' },
    { name: 'f38', func: x => Math.pow(x, 4.0) + 2.0*Math.pow(x, 3.0) - 13.0*Math.pow(x, 2.0) - 14.0*x + 24.0, a: -3.0, b: 1.0, desc: 'x^4 + 2x^3 - 13x^2 - 14x + 24' },
    { name: 'f39', func: x => Math.exp(Math.pow(x, 2.0)) - Math.exp(1.2*x), a: 0.0, b: 2.0, desc: 'exp(x^2) - exp(1.2x)' },
    { name: 'f40', func: x => Math.pow(x, 5.0) - 3.0*Math.pow(x, 4.0) + 2.0*Math.pow(x, 3.0) - x + 0.1, a: -1.0, b: 3.0, desc: 'x^5 - 3x^4 + 2x^3 - x + 0.1' },
    { name: 'f41', func: x => Math.pow(x + 0.3, 7.0) - 0.01, a: -2.0, b: 1.0, desc: '(x+0.3)^7 - 0.01' },
    { name: 'f42', func: x => Math.pow(x, 6.0) - 8.0*Math.pow(x, 5.0) + 24.0*Math.pow(x, 4.0) - 32.0*Math.pow(x, 3.0) + 16.0*Math.pow(x, 2.0), a: 0.0, b: 4.0, desc: 'x^6 - 8x^5 + 24x^4 - 32x^3 + 16x^2' },
    { name: 'f43', func: x => -2.0*Math.log10(0.000027027 + 2.51/(10000000.0*Math.sqrt(x))) - 1.0/Math.sqrt(x), a: 0.008, b: 0.03, desc: 'Colebrook-White friction factor' },
    { name: 'f44', func: x => x - 0.99*Math.sin(x) - 2.0, a: 2.0, b: 3.0, desc: 'Kepler equation (e=0.99)' },
    { name: 'f45', func: x => (10.0 + 3.592/Math.pow(x, 2.0))*(x - 0.04267) - 0.08206*300.0, a: 2.0, b: 3.0, desc: 'Van der Waals (CO2)' },
    { name: 'f46', func: x => x*Math.exp(x/2.0) - 1.5, a: 0.0, b: 1.0, desc: 'x*exp(x/2) - 1.5' },
    { name: 'f47', func: x => Math.cos(x) + 1.0*Math.pow(1.0 - Math.cos(x), 2.0) - 0.05*Math.pow(x, 2.0), a: 3.0, b: 6.0, desc: 'Beam deflection equation' },
    { name: 'f48', func: x => 0.05 - Math.pow(x, 3.0)/((1.0 - x)*Math.pow(0.8 - 2.0*x, 2.0)), a: 0.01, b: 0.3, desc: 'Chemical equilibrium' },
];

const tol = 1e-14;
const maxIter = 10000;

console.log("HybridRoots Benchmark Suite - JavaScript Port");
console.log("======================================");

const funcs = [mpbf, mpbfms, mptf, mptfms];
const names = ["mpbf", "mpbfms", "mptf", "mptfms"];

let times = [0, 0, 0, 0];
let convs = [0, 0, 0, 0];
let iters = [0, 0, 0, 0];
let nfes = [0, 0, 0, 0];

for (let i = 0; i < benchmarks.length; i++) {
    const b = benchmarks[i];
    console.log(`\n[${(i + 1).toString().padStart(2, ' ')}/48] ${b.name}: ${b.desc}`);

    for (let a = 0; a < 4; a++) {
        funcs[a](b.func, b.a, b.b, tol, maxIter); // Warmup

        let runs = 100;
        let result;
        const start = process.hrtime.bigint();
        for (let r = 0; r < runs; r++) {
            result = funcs[a](b.func, b.a, b.b, tol, maxIter);
        }
        const end = process.hrtime.bigint();
        const elapsedUs = Number(end - start) / 1000.0 / runs;

        if (result.converged) {
            console.log(`       ${names[a].padEnd(8, ' ')}: root=${result.root.toFixed(10)}, iter=${result.iterations.toString().padStart(2, ' ')}, nfe=${result.functionCalls.toString().padStart(3, ' ')}`);
            times[a] += elapsedUs;
            convs[a]++;
            iters[a] += result.iterations;
            nfes[a] += result.functionCalls;
        } else {
            console.log(`       ${names[a].padEnd(8, ' ')}: FAILED`);
        }
    }
}

console.log("\nSUMMARY");
console.log("======================================");
console.log("Algorithm  | Converged  | Total Time (us)    | Avg NFE    | Avg Iterations");
console.log("--------------------------------------------------------------------------------");
for (let a = 0; a < 4; a++) {
    const avgNfe = (nfes[a] / convs[a]).toFixed(2);
    const avgIter = (iters[a] / convs[a]).toFixed(2);
    const t = times[a].toFixed(2).padStart(18, ' ');
    console.log(`${names[a].padEnd(10, ' ')} | ${convs[a].toString().padStart(2, ' ')}/${benchmarks.length.toString().padEnd(7, ' ')} | ${t} | ${avgNfe.padStart(10, ' ')} | ${avgIter.padStart(15, ' ')}`);
}
