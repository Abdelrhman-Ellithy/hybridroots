import re
from statistics import median, pstdev
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tex_path = ROOT / 'hybrid_root_bracketing_paper.tex'

text = tex_path.read_text(encoding='utf-8')

# Extract the iteration table block between label lines
pattern = re.compile(r"\\begin\{table\}\[H\][\s\S]*?\\label\{tab:iteration_count_results\}[\s\S]*?\\resizebox\{\\textwidth\}\{!\}\{[\s\S]*?\\end\{tabular\}\}\s*\\end\{table\}")
m = pattern.search(text)
if not m:
    raise SystemExit('Iteration table not found')
block = m.group(0)

# Extract rows
lines = []
for ln in block.splitlines():
    ln = ln.strip()
    if not ln:
        continue
    lines.append(ln)

# Find header line
header_idx = None
for i, ln in enumerate(lines):
    if ln.startswith('\\begin{tabular'):
        header_idx = i+1
        break
if header_idx is None:
    raise SystemExit('Header not found')

# Next non-hline is header
while header_idx < len(lines) and ('\\hline' in lines[header_idx] or not lines[header_idx].strip()):
    header_idx += 1
header = lines[header_idx]
header = header.rstrip(' \\')
algs = [s.strip() for s in re.split(r'\s*&\s*', header)][1:]

# Data rows: find first line starting with 'Problem'
data_start = None
for i in range(header_idx+1, len(lines)):
    ln = lines[i]
    if ln.startswith('Problem '):
        data_start = i
        break
if data_start is None:
    raise SystemExit('Problem rows not found')
data = []
for ln in lines[data_start:]:
    if '\\hline' in ln:
        break
    if not ln.endswith('\\'):
        pass
    row = [s.strip() for s in re.split(r'\s*&\s*', ln.rstrip(' \\'))]
    if not row or not row[0].startswith('Problem'):
        continue
    values = []
    for cell in row[1:1+len(algs)]:
        if cell == '--':
            values.append(None)
        else:
            try:
                values.append(int(cell))
            except ValueError:
                values.append(None)
    data.append(values)

# Compute stats
def safe_pstdev(xs):
    return pstdev(xs) if len(xs) > 1 else 0.0

cols = list(zip(*data))
print(f"Parsed problems: {len(data)}; algs: {len(algs)}")
stats_rows = []
for alg, col in zip(algs, cols):
    vals = [v for v in col if v is not None]
    avg = sum(vals)/len(vals) if vals else 0.0
    med = median(vals) if vals else 0.0
    sd = safe_pstdev(vals) if vals else 0.0
    stats_rows.append((alg, avg, med, sd))

# Compute wins: per problem, fewest iterations among present values
wins = {alg: 0 for alg in algs}
for row in data:
    present = [(alg, v) for alg, v in zip(algs, row) if v is not None]
    if not present:
        continue
    minv = min(v for _, v in present)
    for alg, v in present:
        if v == minv:
            wins[alg] += 1

# Predefined order to match other tables
order = [
    'Opt.BFMS','Opt.TFMS','Opt.BF','Opt.TF',
    'Brent (SciPy)','Brent (Impl.)','HybridBlendBF','HybridBlendTF',
    'QIR','Bisection','Trisection','False Position'
]
order_map = {a:i for i,a in enumerate(order)}
stats_map = {a:(avg,med,sd) for a,avg,med,sd in stats_rows}

rows = []
for alg in order:
    if alg not in stats_map:
        continue
    avg, med, sd = stats_map[alg]
    w = wins.get(alg, 0)
    rows.append((order_map[alg], alg, avg, med, sd, w))

rows.sort()

print('Algorithm|Avg|Median|StdDev|Wins')
for _, alg, avg, med, sd, w in rows:
    print(f"{alg}|{avg:.2f}|{med:.2f}|{sd:.2f}|{w}")


