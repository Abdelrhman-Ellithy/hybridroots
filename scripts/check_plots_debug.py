import sqlite3, pandas as pd
conn=sqlite3.connect('Results.db')
df_alg=pd.read_sql_query('SELECT method_name, AVG(CPU_Time) as avg_cpu FROM results GROUP BY method_name ORDER BY avg_cpu',conn)
df_prob=pd.read_sql_query('SELECT problemId, method_name, AVG(CPU_Time) as avg_cpu FROM results GROUP BY problemId, method_name ORDER BY problemId, method_name',conn)
# display mapping
def make_display(name, maxlen=40):
    if name is None: return ''
    d = name.replace('.py','').replace('_','-').strip()
    if len(d)>maxlen: return d[:maxlen-3]+'...'
    return d
base_map={m: make_display(m) for m in sorted(df_alg['method_name'].unique())}
# uniqueness
seen={}
display_map={}
for m, base in base_map.items():
    key=base
    if key in seen:
        seen[key]+=1
        key=f"{base} ({seen[key]})"
    else:
        seen[key]=1
    display_map[m]=key

pivot=df_prob.pivot(index='problemId', columns='method_name', values='avg_cpu')
print('num methods in df_alg:', len(df_alg))
print('num pivot columns:', len(pivot.columns))
algs_ordered = df_alg.sort_values('avg_cpu')['method_name'].tolist()
algs_in_pivot=[a for a in algs_ordered if a in pivot.columns]
print('algs_in_pivot len:', len(algs_in_pivot))
print('algs_in_pivot display names:')
for a in algs_in_pivot:
    print('-',repr(a),'->',repr(display_map.get(a)))

conn.close()
