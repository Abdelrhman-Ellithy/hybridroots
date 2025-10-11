import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Connect to the database
conn = sqlite3.connect('Results.db')

# Query: Average, min, max CPU time per algorithm
df_alg = pd.read_sql_query('''
    SELECT method_name, 
           AVG(CPU_Time) as avg_cpu, 
           MIN(CPU_Time) as min_cpu, 
           MAX(CPU_Time) as max_cpu, 
           COUNT(*) as runs
    FROM results
    GROUP BY method_name
    ORDER BY avg_cpu
''', conn)

print('Average CPU time per algorithm:')
print(df_alg)

# Save aggregated algorithm-level stats to CSV for downstream use
out_csv = 'CPU_Times_Per_Algorithm.csv'
df_alg.to_csv(out_csv, index=False)
print(f"Saved aggregated algorithm CPU stats to {out_csv}")

# Query: Average CPU time per problem per algorithm
df_prob = pd.read_sql_query('''
    SELECT problemId, method_name, AVG(CPU_Time) as avg_cpu
    FROM results
    GROUP BY problemId, method_name
    ORDER BY problemId, method_name
''', conn)

# Create a human-friendly display name for plotting to avoid duplicated/awkward labels
# strip .py suffixes and normalize underscores to dashes; also cap length for readability
def make_display(name, maxlen=40):
    if name is None:
        return ''
    d = name.replace('.py', '').replace('_', '-').strip()
    if len(d) > maxlen:
        return d[: maxlen - 3] + '...'
    return d

# mapping from raw method_name -> display label
# make display names and ensure uniqueness (avoid collisions after truncation)
all_methods = sorted(df_alg['method_name'].unique(), key=lambda m: m)
base_map = {m: make_display(m) for m in all_methods}
display_map = {}
seen = {}
for m, base in base_map.items():
    key = base
    if key in seen:
        seen[key] += 1
        key = f"{base} ({seen[base]})"
    else:
        seen[key] = 1
    display_map[m] = key
# add display column to dataframes for convenience
df_alg['display_name'] = df_alg['method_name'].map(display_map)
df_prob['display_name'] = df_prob['method_name'].map(display_map)

# Pivot: problems x algorithms table for easier comparisons
pivot = df_prob.pivot(index='problemId', columns='method_name', values='avg_cpu')
# Save pivot to CSV as well for external analysis
pivot_csv = 'CPU_Times_Per_Problem_Per_Algorithm.csv'
pivot.fillna(float('nan')).to_csv(pivot_csv)
print(f"Saved problem x algorithm pivot to {pivot_csv}")

# Compute wins (which algorithm is fastest per problem)
fastest_per_problem = df_prob.loc[df_prob.groupby('problemId')['avg_cpu'].idxmin()]
win_counts = fastest_per_problem['method_name'].value_counts().rename('wins').reset_index().rename(columns={'index':'method_name'})
df_alg = df_alg.merge(win_counts, on='method_name', how='left')
df_alg['wins'] = df_alg['wins'].fillna(0).astype(int)

# Determine algorithm order by overall average CPU time (fastest first)
ordered_algs = df_alg.sort_values('avg_cpu')['method_name'].tolist()

# Pairwise speedup ratios: for each pair A,B compute median(A/B) across problems where both present
# use fastest-first ordering for consistency in outputs
algs = ordered_algs
ratios = []
for a in algs:
    for b in algs:
        if a == b:
            continue
        if a in pivot.columns and b in pivot.columns:
            valid = pivot[[a,b]].dropna()
            if len(valid) > 0:
                median_ratio = (valid[a] / valid[b]).median()
            else:
                median_ratio = float('nan')
        else:
            median_ratio = float('nan')
        ratios.append({'alg_a': a, 'alg_b': b, 'median_ratio_a_over_b': median_ratio})
df_ratios = pd.DataFrame(ratios)
ratios_csv = 'Pairwise_Median_Ratios.csv'
df_ratios.to_csv(ratios_csv, index=False)
print(f"Saved pairwise median ratios to {ratios_csv}")

## Improved barplot: average CPU time per algorithm with wins and errorbars
sns.set(style='whitegrid')
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=df_alg.sort_values('avg_cpu'), x='method_name', y='avg_cpu', palette='tab10', ci=None)
# annotate bars with wins
# replace x tick labels with display names and annotate
df_sorted = df_alg.sort_values('avg_cpu').reset_index(drop=True)
ax = sns.barplot(data=df_sorted, x='display_name', y='avg_cpu', palette='tab10', ci=None)
for p, (_, row) in zip(ax.patches, df_sorted.iterrows()):
    height = p.get_height()
    ax.annotate(f"wins={int(row['wins'])}", (p.get_x() + p.get_width() / 2., height), ha='center', va='bottom', fontsize=9, rotation=0)
ax.set_xticklabels(df_sorted['display_name'], rotation=45, ha='right')
ax.set_title('Average CPU Time per Algorithm')
ax.set_ylabel('Avg CPU Time (s)')
ax.set_xlabel('Algorithm')
plt.tight_layout()
plt.subplots_adjust(bottom=0.30)
plt.savefig('avg_cpu_time_per_algorithm.png', dpi=150)
plt.close()

## Additional summary statistics for CPU time per algorithm
cpu_stats = df_alg.copy()
grouped = df_prob.groupby('method_name')['avg_cpu']
cpu_stats['std_cpu'] = grouped.std().reindex(cpu_stats['method_name']).values
cpu_stats['median_cpu'] = grouped.median().reindex(cpu_stats['method_name']).values
cpu_stats = cpu_stats.sort_values('avg_cpu')
print('\nCPU time statistics per algorithm:')
print(cpu_stats)
# Save enhanced CPU stats
enhanced_csv = 'CPU_Times_Per_Algorithm_Enhanced.csv'
cpu_stats.to_csv(enhanced_csv, index=False)
print(f"Saved enhanced CPU stats to {enhanced_csv}")

## Line plot: CPU time per problem for each algorithm (clearer, distinct markers/colors)
# increase figure size to accommodate many lines and place legend below
plt.figure(figsize=(16, 8))
# respect the global fastest-first ordering but only include algorithms that appear in the pivot
algs_in_pivot = [a for a in algs if a in pivot.columns]
palette = sns.color_palette('tab20', n_colors=max(1, len(algs_in_pivot)))
markers = ['o', 's', '^', 'D', 'v', 'P', 'X', '*', '<', '>']
for i, alg in enumerate(algs_in_pivot):
    y = pivot[alg]
    plt.plot(pivot.index, y, marker=markers[i % len(markers)], label=display_map.get(alg, alg), color=palette[i % len(palette)], linewidth=1.5)
plt.title('CPU Time per Problem for Each Algorithm')
plt.xlabel('Problem ID')
plt.ylabel('Avg CPU Time (s)')
plt.xlim(pivot.index.min(), pivot.index.max())
plt.ylim(bottom=0)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.subplots_adjust(right=0.75)
plt.savefig('cpu_time_lineplot_per_problem.png', dpi=150)
plt.close()

# Query: Average iterations per algorithm (if available)
try:
    df_iter = pd.read_sql_query('''
        SELECT method_name, AVG(iterations) as avg_iter
        FROM results
        GROUP BY method_name
        ORDER BY avg_iter
    ''', conn)
    print('Average iterations per algorithm:')
    print(df_iter)
    # merge into cpu_stats if present
    cpu_stats = cpu_stats.merge(df_iter, on='method_name', how='left')
except Exception:
    print('No iterations data found in the database.')

## 1. Line plot: Average CPU time per algorithm across all problems
avg_cpu_per_alg = df_prob.groupby('method_name')['avg_cpu'].mean().sort_values()
# map index to display names for plotting and ensure tick labels align to positions
avg_cpu_per_alg_disp = avg_cpu_per_alg.rename(index=display_map)
plt.figure(figsize=(12, 6))
ax = avg_cpu_per_alg_disp.plot(marker='o', linestyle='-', linewidth=2)
plt.title('Average CPU Time per Algorithm (Overall)')
plt.ylabel('Avg CPU Time (s)')
plt.xlabel('Algorithm')
# Explicitly set xticks to the integer positions and labels to the ordered display names so labels
# cannot drift relative to the plotted points
positions = list(range(len(avg_cpu_per_alg_disp.index)))
labels = list(avg_cpu_per_alg_disp.index)
ax.set_xticks(positions)
ax.set_xticklabels(labels, rotation=45, ha='right')
plt.ylim(bottom=0)
plt.tight_layout()
plt.subplots_adjust(bottom=0.30)
plt.savefig('avg_cpu_time_lineplot_overall.png', dpi=150)
plt.close()

## 2. Scatter: Fastest algorithm for each problem (min CPU time per problem)
fastest = df_prob.loc[df_prob.groupby('problemId')['avg_cpu'].idxmin()]
plt.figure(figsize=(12, 6))
# plot scatter points ordered by the global fastest-first algorithm ordering
algs_in_fastest = [a for a in ordered_algs if a in fastest['method_name'].unique()]
for i, alg in enumerate(algs_in_fastest):
    subset = fastest[fastest['method_name'] == alg]
    plt.scatter(subset['problemId'], subset['avg_cpu'], label=display_map.get(alg, alg), s=80)
plt.title('Fastest Algorithm per Problem (CPU Time)')
plt.xlabel('Problem ID')
plt.ylabel('Fastest CPU Time (s)')
plt.xlim(pivot.index.min(), pivot.index.max())
plt.ylim(bottom=0)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title='Algorithm')
plt.tight_layout()
plt.savefig('fastest_algorithm_per_problem_lineplot.png', dpi=150)
plt.close()

## 3. Line plot: Top 3 fastest algorithms (by overall average CPU time) across all problems
top3_algs = avg_cpu_per_alg.head(3).index.tolist()
plt.figure(figsize=(12, 6))
for i, alg in enumerate(top3_algs):
    if alg not in pivot.columns:
        continue
    plt.plot(pivot.index, pivot[alg], marker=markers[i % len(markers)], label=display_map.get(alg, alg), linewidth=2)
plt.title('Top 3 Fastest Algorithms: CPU Time per Problem')
plt.xlabel('Problem ID')
plt.ylabel('Avg CPU Time (s)')
plt.xlim(pivot.index.min(), pivot.index.max())
plt.ylim(bottom=0)
plt.legend()
plt.tight_layout()
plt.savefig('top3_fastest_algorithms_lineplot.png', dpi=150)
plt.close()

# Persist final combined CSV with key stats for easy consumption (overwrite requested output)
final_csv = 'CPU_Times_Per_Algorithm.csv'
# ensure we include the fields the user expects: method_name, avg_cpu, min_cpu, max_cpu, runs, wins, median_cpu, std_cpu
# Also include a small note if histogram data is missing
final_df = cpu_stats[['method_name', 'display_name', 'avg_cpu', 'min_cpu', 'max_cpu', 'runs', 'wins', 'median_cpu', 'std_cpu']].copy()
# ensure final CSV is sorted fastest-first by avg_cpu
if 'avg_cpu' in final_df.columns:
    final_df = final_df.sort_values('avg_cpu')
final_df.to_csv(final_csv, index=False)
print(f"Wrote final summary CSV to {final_csv}")
conn.close()