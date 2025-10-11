import sqlite3
import pandas as pd

conn = sqlite3.connect('Results.db')
# average CPU per algorithm across problems (same as df_alg in analyze_results.py)
df_prob = pd.read_sql_query("SELECT problemId, method_name, AVG(CPU_Time) as avg_cpu FROM results GROUP BY problemId, method_name", conn)
avg_cpu_per_alg = df_prob.groupby('method_name')['avg_cpu'].mean().sort_values()

def make_display(name, maxlen=40):
    if name is None: return ''
    d = name.replace('.py','').replace('_','-').strip()
    if len(d)>maxlen: return d[:maxlen-3]+'...'
    return d

all_methods = sorted(avg_cpu_per_alg.index.tolist())
base_map = {m: make_display(m) for m in all_methods}
seen = {}
display_map = {}
for m, base in base_map.items():
    key = base
    if key in seen:
        seen[key] += 1
        key = f"{base} ({seen[base]})"
    else:
        seen[key] = 1
    display_map[m] = key

print('Overall avg series (method_name -> avg_cpu -> display_name):')
for m, v in avg_cpu_per_alg.items():
    print(repr(m), v, '->', repr(display_map.get(m)))

print('\nSeries index list:')
print(list(avg_cpu_per_alg.index))

# Also print CPU_Times_Per_Algorithm.csv top rows if present
try:
    csv = pd.read_csv('CPU_Times_Per_Algorithm.csv')
    print('\nCPU_Times_Per_Algorithm.csv head:')
    print(csv[['method_name','display_name','avg_cpu']].head(20).to_string(index=False))
except Exception as e:
    print('Could not read CSV:', e)

conn.close()
