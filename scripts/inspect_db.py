import sqlite3
import pandas as pd

conn = sqlite3.connect('Results.db')
print('Connected to Results.db')

# Basic results info
df_all = pd.read_sql_query('SELECT * FROM results LIMIT 20', conn)
print('\nSample rows (first 20):')
print(df_all.head())

# method_name distinct list and counts (with repr to show whitespace)
method_counts = pd.read_sql_query('SELECT method_name, COUNT(*) as cnt FROM results GROUP BY method_name ORDER BY cnt DESC', conn)
print('\nMethod name counts (raw):')
for _, r in method_counts.iterrows():
    print(repr(r['method_name']), r['cnt'])

# show unique repr sorted
unique_methods = [m for m in method_counts['method_name'].tolist()]
print('\nUnique method names (repr):')
for m in unique_methods:
    print(repr(m))

# pivot overview
df_prob = pd.read_sql_query("SELECT problemId, method_name, AVG(CPU_Time) as avg_cpu FROM results GROUP BY problemId, method_name", conn)
print('\nNumber of problem-method pairs:', len(df_prob))

pivot = df_prob.pivot(index='problemId', columns='method_name', values='avg_cpu')
print('\nPivot columns (repr):')
for c in pivot.columns:
    print(repr(c))

print('\nNon-null counts per column:')
print(pivot.notna().sum().sort_values(ascending=False))

# check for near-duplicate names by normalized (strip and lowercase)
norm = [(m, m.strip().lower()) for m in unique_methods]
from collections import defaultdict
groups = defaultdict(list)
for orig, n in norm:
    groups[n].append(orig)

print('\nNormalized name groups (strip+lower):')
for k, lst in groups.items():
    if len(lst) > 1:
        print(k, '->', lst)

# show schema
print('\nResults table schema:')
print([r[1] for r in conn.execute('PRAGMA table_info(results)').fetchall()])

conn.close()
print('\nDone')
