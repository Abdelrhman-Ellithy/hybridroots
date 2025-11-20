import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Set plot style
sns.set(style='whitegrid')

# Connect to the database
db_path = 'Results.db'
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found. Run the benchmark first.")
    exit()

conn = sqlite3.connect(db_path)

print("--- Loading Data ---")

# 1. LOAD RAW DATA
try:
    df_raw = pd.read_sql_query("SELECT * FROM results", conn)
    has_iterations = 'iterations' in df_raw.columns
except Exception as e:
    print(f"Error reading DB: {e}")
    conn.close()
    exit()

# --- 2. GENERATE MATRIX CSVs ---
print("--- Generating Matrix CSVs ---")

# A. Iteration Matrix
if has_iterations:
    pivot_iter = df_raw.pivot_table(index='problemId', columns='method_name', values='iterations', aggfunc='mean')
    pivot_iter.index = [f"Problem {i}" for i in pivot_iter.index]
    pivot_iter = pivot_iter.fillna(0).astype(int)
    
    csv_iter_name = 'Algorithm_Iterations_Matrix.csv'
    pivot_iter.to_csv(csv_iter_name)
    print(f"Generated Iteration Matrix: {csv_iter_name}")

# B. CPU Time Matrix (Microseconds)
pivot_cpu = df_raw.pivot_table(index='problemId', columns='method_name', values='CPU_Time', aggfunc='mean')
# Save raw pivot for internal calculations before renaming indices
raw_pivot = pivot_cpu.copy() 

pivot_cpu.index = [f"Problem {i}" for i in pivot_cpu.index]
csv_cpu_name = 'Algorithm_CPU_Time_us_Matrix.csv' # Renamed file
pivot_cpu.to_csv(csv_cpu_name)
print(f"Generated CPU Time Matrix: {csv_cpu_name}")

# --- 3. CALCULATE AGGREGATE STATISTICS ---

# Basic Stats from SQL
query_agg = '''
    SELECT method_name, 
           AVG(CPU_Time) as avg_cpu, 
           MIN(CPU_Time) as min_cpu, 
           MAX(CPU_Time) as max_cpu, 
           COUNT(*) as runs
    FROM results
    GROUP BY method_name
    ORDER BY avg_cpu
'''
df_alg = pd.read_sql_query(query_agg, conn)

# Calculate Median and Std Dev (Python side)
grouped = df_raw.groupby('method_name')['CPU_Time']
df_alg['std_cpu'] = grouped.std().reindex(df_alg['method_name']).values
df_alg['median_cpu'] = grouped.median().reindex(df_alg['method_name']).values

# Helper: Display names
def make_display(name, maxlen=40):
    if name is None: return ''
    d = name.replace('.py', '').replace('_', '-').strip()
    return d[: maxlen - 3] + '...' if len(d) > maxlen else d

all_methods = sorted(df_alg['method_name'].unique())
display_map = {m: make_display(m) for m in all_methods}
df_alg['display_name'] = df_alg['method_name'].map(display_map)

# Calculate Wins
fastest_rows = df_raw.loc[df_raw.groupby('problemId')['CPU_Time'].idxmin()]
win_counts = fastest_rows['method_name'].value_counts().rename('wins').reset_index()
win_counts.columns = ['method_name', 'wins'] 
df_alg = df_alg.merge(win_counts, on='method_name', how='left')
df_alg['wins'] = df_alg['wins'].fillna(0).astype(int)

# --- 4. PAIRWISE SPEEDUP RATIOS ---
print("--- Computing Pairwise Ratios ---")
ordered_algs = df_alg.sort_values('avg_cpu')['method_name'].tolist()
ratios = []

for a in ordered_algs:
    for b in ordered_algs:
        if a == b: continue
        if a in raw_pivot.columns and b in raw_pivot.columns:
            valid = raw_pivot[[a,b]].dropna()
            if len(valid) > 0:
                median_ratio = (valid[a] / valid[b]).median()
            else:
                median_ratio = float('nan')
        else:
            median_ratio = float('nan')
        ratios.append({'alg_a': a, 'alg_b': b, 'median_ratio_a_over_b': median_ratio})

df_ratios = pd.DataFrame(ratios)
df_ratios.to_csv('Pairwise_Median_Ratios.csv', index=False)
print("Saved Pairwise_Median_Ratios.csv")

# --- 5. SAVE FINAL SUMMARY CSV ---
final_csv = 'CPU_Times_Per_Algorithm.csv'
final_cols = ['method_name', 'display_name', 'avg_cpu', 'min_cpu', 'max_cpu', 'median_cpu', 'std_cpu', 'runs', 'wins']
# Ensure columns exist
existing_cols = [c for c in final_cols if c in df_alg.columns]
df_alg[existing_cols].to_csv(final_csv, index=False)
print(f"Saved detailed summary to {final_csv}")


# --- 6. VISUALIZATIONS ---
print("--- Generating Plots ---")

# A. Bar Plot: Average CPU Time with Wins
plt.figure(figsize=(12, 6))
df_sorted = df_alg.sort_values('avg_cpu')
ax = sns.barplot(data=df_sorted, x='display_name', y='avg_cpu', palette='viridis')

for p, (_, row) in zip(ax.patches, df_sorted.iterrows()):
    height = p.get_height()
    if height > 0:
        ax.annotate(f"wins={int(row['wins'])}", 
                   (p.get_x() + p.get_width() / 2., height), 
                   ha='center', va='bottom', fontsize=9, color='black')

ax.set_xticklabels(df_sorted['display_name'], rotation=45, ha='right')
ax.set_title('Average CPU Time per Algorithm (Microseconds)') # Label Update
ax.set_ylabel('Avg Time (us)') # Label Update
plt.tight_layout()
plt.savefig('avg_cpu_time_per_algorithm.png', dpi=150)
plt.close()

# B. Line Plot: CPU Time per Problem (All Algs)
plt.figure(figsize=(16, 8))
markers = ['o', 's', '^', 'D', 'v', 'P', 'X', '*', '<', '>']
# Filter only algs present in pivot
algs_in_pivot = [a for a in ordered_algs if a in raw_pivot.columns]
palette = sns.color_palette('tab20', n_colors=max(1, len(algs_in_pivot)))

for i, alg in enumerate(algs_in_pivot):
    plt.plot(raw_pivot.index, raw_pivot[alg], 
             marker=markers[i % len(markers)], 
             label=display_map.get(alg, alg), 
             color=palette[i % len(palette)], 
             linewidth=1.5, alpha=0.8)

plt.title('CPU Time per Problem (Microseconds)') # Label Update
plt.xlabel('Problem ID')
plt.ylabel('Time (us)') # Label Update
plt.xlim(raw_pivot.index.min(), raw_pivot.index.max())
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig('cpu_time_lineplot_per_problem.png', dpi=150)
plt.close()

# C. Line Plot: Overall Average Trend
avg_cpu_series = df_alg.set_index('display_name')['avg_cpu'].sort_values()
plt.figure(figsize=(12, 6))
ax = avg_cpu_series.plot(marker='o', linestyle='-', linewidth=2)
plt.title('Average CPU Time per Algorithm (Overall Trend)')
plt.ylabel('Avg Time (us)') # Label Update
plt.xlabel('Algorithm')
ax.set_xticks(range(len(avg_cpu_series)))
ax.set_xticklabels(avg_cpu_series.index, rotation=45, ha='right')
plt.tight_layout()
plt.savefig('avg_cpu_time_lineplot_overall.png', dpi=150)
plt.close()

# D. Scatter Plot: Fastest Algorithm per Problem
plt.figure(figsize=(12, 6))
# Use raw dataframe for problem-level granularity
fastest = df_raw.loc[df_raw.groupby('problemId')['CPU_Time'].idxmin()]
algs_in_fastest = [a for a in ordered_algs if a in fastest['method_name'].unique()]

for i, alg in enumerate(algs_in_fastest):
    subset = fastest[fastest['method_name'] == alg]
    plt.scatter(subset['problemId'], subset['CPU_Time'], 
                label=display_map.get(alg, alg), s=80, alpha=0.8)

plt.title('Fastest Algorithm per Problem (CPU Time)')
plt.xlabel('Problem ID')
plt.ylabel('Fastest Time (us)') # Label Update
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title='Algorithm')
plt.tight_layout()
plt.savefig('fastest_algorithm_per_problem_lineplot.png', dpi=150)
plt.close()

# E. Line Plot: Top 3 Fastest Algorithms
top3_algs = avg_cpu_series.head(3).index.tolist()
inv_map = {v: k for k, v in display_map.items()}
top3_method_names = [inv_map.get(disp, disp) for disp in top3_algs]

plt.figure(figsize=(12, 6))
for i, alg in enumerate(top3_method_names):
    if alg not in raw_pivot.columns: continue
    plt.plot(raw_pivot.index, raw_pivot[alg], 
             marker=markers[i % len(markers)], 
             label=display_map.get(alg, alg), 
             linewidth=2)

plt.title('Top 3 Fastest Algorithms: CPU Time per Problem')
plt.xlabel('Problem ID')
plt.ylabel('Time (us)') # Label Update
plt.xlim(raw_pivot.index.min(), raw_pivot.index.max())
plt.legend()
plt.tight_layout()
plt.savefig('top3_fastest_algorithms_lineplot.png', dpi=150)
plt.close()

conn.close()
print("--- Analysis Complete ---")