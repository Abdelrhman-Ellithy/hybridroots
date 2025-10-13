import re
from pathlib import Path
from statistics import median, pstdev

TEX_PATH = Path('hybrid_root_bracketing_paper.tex')
text = TEX_PATH.read_text(encoding='utf-8')

block_re = re.compile(
    r"\\label\{tab:iteration_count_results\}[\s\S]*?"  # label
    r"\\begin\{tabular\}\{l[^}]*\}\s*\n"              # begin tabular
    r"\\hline\s*\n"                                       # hline
    r"(?P<header>[^\n]+?)\\\\\s*\n"                   # header line
    r"\\hline\s*\n"                                       # hline
    r"(?P<body>[\s\S]*?)\n\\hline",                     # body until hline
    re.M
)
m = block_re.search(text)
if not m:
    raise SystemExit('iteration table block not found')

header = m.group('header').strip()
algs = [x.strip() for x in header.split('&')][1:]
body = m.group('body')

rows = []
for line in body.splitlines():
    line = line.strip()
    if not line or not line.startswith('Problem'):
        continue
    if line.endswith('\\'):
        line = line[:-2]
    parts = [x.strip() for x in line.split('&')]
    vals = []
    for cell in parts[1:1+len(algs)]:
        if cell == '--':
            vals.append(None)
        else:
            try:
                vals.append(int(cell))
            except Exception:
                vals.append(None)
    rows.append(vals)

if not rows:
    raise SystemExit('no data rows parsed')

# stats
def safe_pstdev(xs):
    return pstdev(xs) if len(xs) > 1 else 0.0

cols = list(zip(*rows))
avg = {}
med = {}
sdv = {}
for alg, col in zip(algs, cols):
    vals = [v for v in col if v is not None]
    avg[alg] = sum(vals)/len(vals) if vals else 0.0
    med[alg] = median(vals) if vals else 0.0
    sdv[alg] = safe_pstdev(vals) if vals else 0.0

# wins with fractional ties
wins = {alg: 0.0 for alg in algs}
for r in rows:
    present = [(i, v) for i, v in enumerate(r) if v is not None]
    if not present:
        continue
    minv = min(v for _, v in present)
    tied = [i for i, v in present if v == minv]
    inc = 1.0/len(tied)
    for i in tied:
        wins[algs[i]] += inc

order = [
    'Opt.BFMS','Opt.TFMS','Opt.BF','Opt.TF',
    'Brent (SciPy)','Brent (Impl.)','HybridBlendBF','HybridBlendTF',
    'QIR','Bisection','Trisection','False Position'
]

print('Algorithm|Avg|Median|StdDev|Wins')
for alg in order:
    if alg in avg:
        print(f"{alg}|{avg[alg]:.2f}|{med[alg]:.2f}|{sdv[alg]:.2f}|{wins[alg]:.2f}")


