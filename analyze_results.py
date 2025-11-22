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

# --- DEFINING SORT ORDER ---
# We map the user's display preference to the actual DB keys (based on update_db_names.py)
# This ensures sorting works even if there are slight spacing differences
target_order = [
    "Bisection",
    "False Position",  # DB Key (User asked for "False Position")
    "Trisection",
    "HybridBlendTF",
    "HybridBlendBF",
    "QIR",
    "Brent (Impl.)",   # DB Key (User asked for "Brent (Impl.)")
    "Brent (SciPy)",    # Added to ensure it appears if present
    "Opt.BF",
    "Opt.BFMS",
    "Opt.TF",
    "Opt.TFMS"
]

# Function to sort a list of methods based on target_order
def sort_methods(methods_list):
    # Create a rank map. Items not in target_order get a high rank (placed at end)
    rank = {name: i for i, name in enumerate(target_order)}
    return sorted(methods_list, key=lambda x: rank.get(x, 999))

# --- 2. GENERATE MATRIX CSVs ---
print("--- Generating Matrix CSVs ---")

# A. Iteration Matrix
if has_iterations:
    pivot_iter = df_raw.pivot_table(index='problemId', columns='method_name', values='iterations', aggfunc='mean')
    # Reorder columns based on target_order
    sorted_cols = sort_methods(pivot_iter.columns)
    pivot_iter = pivot_iter.reindex(columns=sorted_cols)
    
    pivot_iter.index = [f"Problem {i}" for i in pivot_iter.index]
    pivot_iter = pivot_iter.fillna(0).astype(int)
    
    csv_iter_name = 'Algorithm_Iterations_Matrix.csv'
    pivot_iter.to_csv(csv_iter_name)
    print(f"Generated Iteration Matrix: {csv_iter_name}")

# B. CPU Time Matrix (Microseconds)
pivot_cpu = df_raw.pivot_table(index='problemId', columns='method_name', values='CPU_Time', aggfunc='mean')
# Save raw pivot for internal calculations before renaming indices
raw_pivot = pivot_cpu.copy() 

# Reorder columns based on target_order
sorted_cols = sort_methods(pivot_cpu.columns)
pivot_cpu = pivot_cpu.reindex(columns=sorted_cols)

pivot_cpu.index = [f"Problem {i}" for i in pivot_cpu.index]
csv_cpu_name = 'Algorithm_CPU_Time_us_Matrix.csv' 
pivot_cpu.to_csv(csv_cpu_name)
print(f"Generated CPU Time Matrix: {csv_cpu_name}")

# --- 3. CALCULATE AGGREGATE STATISTICS (CPU TIME) ---

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

# Remove display_name logic as requested (using raw method_name)

# Calculate CPU Wins (Fastest Time)
fastest_rows = df_raw.loc[df_raw.groupby('problemId')['CPU_Time'].idxmin()]
win_counts = fastest_rows['method_name'].value_counts().rename('wins').reset_index()
win_counts.columns = ['method_name', 'wins'] 
df_alg = df_alg.merge(win_counts, on='method_name', how='left')
df_alg['wins'] = df_alg['wins'].fillna(0).astype(int)

# Apply Sorting to Aggregate DF
df_alg['sort_rank'] = df_alg['method_name'].apply(lambda x: target_order.index(x) if x in target_order else 999)
df_alg = df_alg.sort_values('sort_rank').drop(columns=['sort_rank'])

# --- 3.5 CALCULATE AGGREGATE STATISTICS (ITERATIONS) ---
# New section to generate Iterations_Per_Algorithm.csv
if has_iterations:
    print("--- Calculating Iteration Statistics ---")
    # 1. Basic Aggregations via Pandas
    df_iter_stats = df_raw.groupby('method_name')['iterations'].agg(
        avg_iter='mean',
        min_iter='min',
        max_iter='max',
        median_iter='median',
        std_iter='std',
        runs='count'
    ).reset_index()

    # 2. Calculate Iteration Wins (Fewest Iterations per problem)
    # Find the row with min iterations for each problem
    fewest_iter_rows = df_raw.loc[df_raw.groupby('problemId')['iterations'].idxmin()]
    iter_win_counts = fewest_iter_rows['method_name'].value_counts().rename('wins').reset_index()
    iter_win_counts.columns = ['method_name', 'wins']

    # 3. Merge Wins
    df_iter_stats = df_iter_stats.merge(iter_win_counts, on='method_name', how='left')
    df_iter_stats['wins'] = df_iter_stats['wins'].fillna(0).astype(int)

    # 4. Apply Sorting
    df_iter_stats['sort_rank'] = df_iter_stats['method_name'].apply(lambda x: target_order.index(x) if x in target_order else 999)
    df_iter_stats = df_iter_stats.sort_values('sort_rank').drop(columns=['sort_rank'])

    # 5. Save Iteration Summary CSV
    iter_final_csv = 'Iterations_Per_Algorithm.csv'
    iter_cols = ['method_name', 'avg_iter', 'min_iter', 'max_iter', 'median_iter', 'std_iter', 'runs', 'wins']
    df_iter_stats[iter_cols].to_csv(iter_final_csv, index=False)
    print(f"Saved detailed iteration summary to {iter_final_csv}")

# --- 4. PAIRWISE SPEEDUP RATIOS ---
print("--- Computing Pairwise Ratios ---")
# Use the explicit target order for the ratio matrix
ordered_algs = [m for m in target_order if m in df_alg['method_name'].values]
# Add any missing ones
for m in df_alg['method_name'].unique():
    if m not in ordered_algs:
        ordered_algs.append(m)

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

# --- 5. SAVE FINAL CPU SUMMARY CSV ---
final_csv = 'CPU_Times_Per_Algorithm.csv'
final_cols = ['method_name', 'avg_cpu', 'min_cpu', 'max_cpu', 'median_cpu', 'std_cpu', 'runs', 'wins']
existing_cols = [c for c in final_cols if c in df_alg.columns]
df_alg[existing_cols].to_csv(final_csv, index=False)
print(f"Saved detailed CPU summary to {final_csv}")


# --- 6. VISUALIZATIONS ---
print("--- Generating Plots ---")

# A. Bar Plot: Average CPU Time with Wins
plt.figure(figsize=(12, 6))
# Use df_alg which is already sorted by target_order
ax = sns.barplot(data=df_alg, x='method_name', y='avg_cpu', palette='viridis')

for p, (_, row) in zip(ax.patches, df_alg.iterrows()):
    height = p.get_height()
    if height > 0:
        ax.annotate(f"wins={int(row['wins'])}", 
                   (p.get_x() + p.get_width() / 2., height), 
                   ha='center', va='bottom', fontsize=9, color='black')

ax.set_xticklabels(df_alg['method_name'], rotation=45, ha='right')
ax.set_title('Average CPU Time per Algorithm (Microseconds)')
ax.set_ylabel('Avg Time (us)')
plt.tight_layout()
plt.savefig('avg_cpu_time_per_algorithm.png', dpi=150)
plt.close()

# B. Line Plot: CPU Time per Problem (All Algs)
plt.figure(figsize=(16, 8))
markers = ['o', 's', '^', 'D', 'v', 'P', 'X', '*', '<', '>']
# Filter/Sort algs based on target order
algs_in_pivot = [a for a in target_order if a in raw_pivot.columns]
# Append any extras found in DB but not in target list
for col in raw_pivot.columns:
    if col not in algs_in_pivot:
        algs_in_pivot.append(col)

palette = sns.color_palette('tab20', n_colors=max(1, len(algs_in_pivot)))

for i, alg in enumerate(algs_in_pivot):
    plt.plot(raw_pivot.index, raw_pivot[alg], 
             marker=markers[i % len(markers)], 
             label=alg, 
             color=palette[i % len(palette)], 
             linewidth=1.5, alpha=0.8)

plt.title('CPU Time per Problem (Microseconds)')
plt.xlabel('Problem ID')
plt.ylabel('Time (us)')
plt.xlim(raw_pivot.index.min(), raw_pivot.index.max())
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig('cpu_time_lineplot_per_problem.png', dpi=150)
plt.close()

# C. Line Plot: Overall Average Trend
# Ensure this plot follows the target order
plt.figure(figsize=(12, 6))
ax = df_alg.set_index('method_name')['avg_cpu'].plot(marker='o', linestyle='-', linewidth=2)
plt.title('Average CPU Time per Algorithm (Overall Trend)')
plt.ylabel('Avg Time (us)')
plt.xlabel('Algorithm')
ax.set_xticks(range(len(df_alg)))
ax.set_xticklabels(df_alg['method_name'], rotation=45, ha='right')
plt.tight_layout()
plt.savefig('avg_cpu_time_lineplot_overall.png', dpi=150)
plt.close()

# D. Scatter Plot: Fastest Algorithm per Problem
plt.figure(figsize=(12, 6))
fastest = df_raw.loc[df_raw.groupby('problemId')['CPU_Time'].idxmin()]
# Sort legends by target order
algs_in_fastest = [a for a in target_order if a in fastest['method_name'].unique()]
for m in fastest['method_name'].unique():
    if m not in algs_in_fastest: algs_in_fastest.append(m)

for i, alg in enumerate(algs_in_fastest):
    subset = fastest[fastest['method_name'] == alg]
    plt.scatter(subset['problemId'], subset['CPU_Time'], 
                label=alg, s=80, alpha=0.8)

plt.title('Fastest Algorithm per Problem (CPU Time)')
plt.xlabel('Problem ID')
plt.ylabel('Fastest Time (us)')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title='Algorithm')
plt.tight_layout()
plt.savefig('fastest_algorithm_per_problem_lineplot.png', dpi=150)
plt.close()

# E. Line Plot: Top 3 Fastest Algorithms (Dynamically calculated, but respecting label format)
# Calculate top 3 based on actual data (lowest time)
top3_algs = df_alg.sort_values('avg_cpu')['method_name'].head(3).tolist()

plt.figure(figsize=(12, 6))
for i, alg in enumerate(top3_algs):
    if alg not in raw_pivot.columns: continue
    plt.plot(raw_pivot.index, raw_pivot[alg], 
             marker=markers[i % len(markers)], 
             label=alg, 
             linewidth=2)

plt.title('Top 3 Fastest Algorithms: CPU Time per Problem')
plt.xlabel('Problem ID')
plt.ylabel('Time (us)')
plt.xlim(raw_pivot.index.min(), raw_pivot.index.max())
plt.legend()
plt.tight_layout()
plt.savefig('top3_fastest_algorithms_lineplot.png', dpi=150)
plt.close()

conn.close()
print("--- Analysis Complete ---")