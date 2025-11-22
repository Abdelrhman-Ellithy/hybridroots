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
    
    csv_iter_name ='Algorithm_Iterations_Matrix.csv'
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

# --- 7. ESTIMATE TOTAL NFE AND FLOPS PER PROBLEM ---
print("--- Estimating Total NFE and FLOPs ---")

# Load iteration statistics (just created)
iter_csv = 'Iterations_Per_Algorithm.csv'
if not os.path.exists(iter_csv):
    print(f"Warning: {iter_csv} not found. Skipping NFE/FLOPs estimation.")
else:
    df_iter = pd.read_csv(iter_csv)

    # Load complexity data
    complexity_csv = 'Complexity_Per_Algorithm.csv'
    if not os.path.exists(complexity_csv):
        print(f"Error: {complexity_csv} not found. Cannot compute total workload.")
    else:
        df_complex = pd.read_csv(complexity_csv)

        # Merge on Algorithm
        df_merged = df_iter.merge(df_complex, on='method_name', how='left')

        # Compute Total NFE (avg_iter * NFE_per_iter)
        df_merged['total_nfe_low']  = df_merged['avg_iter'] * df_merged['NFE_per_iter_low']
        df_merged['total_nfe_high'] = df_merged['avg_iter'] * df_merged['NFE_per_iter_high']

        # Compute Total FLOPs (avg_iter * NFE_per_iter * FLOPs_per_iter)
        df_merged['total_flops_low']  = df_merged['avg_iter'] * df_merged['NFE_per_iter_low'] * df_merged['FLOPs_per_iter_low']
        df_merged['total_flops_high'] = df_merged['avg_iter'] * df_merged['NFE_per_iter_high'] * df_merged['FLOPs_per_iter_high']

        # Format nicely
        def format_range(low, high, is_flops=False):
            if pd.isna(low) or pd.isna(high):
                return "N/A"
            low = round(low, 1)
            high = round(high, 1)
            if is_flops:
                if high >= 1000:
                    return f"{int(low//1000)}--{int(high//1000)}k" if low < 1000 else f"{int(low//1000)}--{int(high//1000)}k"
                else:
                    return f"{int(low)}--{int(high)}"
            else:
                return f"{low:.2f}--{high:.2f}".rstrip('0').rstrip('.') if '.' in f"{low:.2f}" else f"{int(low)}--{int(high)}"

        df_merged['Avg Total NFE'] = df_merged.apply(
            lambda row: f"{format_range(row['total_nfe_low'], row['total_nfe_high'])} "
                        f"(avg_iter × NFE/iter)" if pd.notna(row['total_nfe_low']) else "N/A", axis=1)

        df_merged['Estimated Total FLOPs'] = df_merged.apply(
            lambda row: format_range(row['total_flops_low'], row['total_flops_high'], is_flops=True), axis=1)

        # Select and reorder columns for output
        summary_cols = ['method_name', 'avg_iter', 'wins', 'Avg Total NFE', 'Estimated Total FLOPs']
        df_summary = df_merged[summary_cols].copy()
        df_summary.columns = ['Algorithm', 'Avg Iterations', 'Iter Wins', 'Avg Total NFE', 'Estimated Total FLOPs (per problem)']

        # Sort by performance (same order as before)
        df_summary['rank'] = df_summary['Algorithm'].apply(lambda x: target_order.index(x) if x in target_order else 999)
        df_summary = df_summary.sort_values('rank').drop('rank', axis=1)

        # Save LaTeX-ready CSV
        nfe_flops_csv = 'Total_NFE_and_FLOPs_Summary.csv'
        df_summary.to_csv(nfe_flops_csv, index=False)
        print(f"Saved total NFE and FLOPs summary → {nfe_flops_csv}")

        # Also save pure LaTeX table fragment (optional)
        latex_table = "\\begin{tabular}{lcc}\n\\hline\nAlgorithm & Avg Total NFE & Estimated Total FLOPs \\\\\n\\hline\n"
        for _, row in df_summary.iterrows():
            alg = row['Algorithm'].replace('_', ' ')
            nfe = row['Avg Total NFE'].replace('avg_iter × NFE/iter', '')
            flops = row['Estimated Total FLOPs (per problem)']
            if 'Opt.BFMS' in alg or 'Opt.TFMS' in alg:
                latex_table += f"\\textbf{{{alg}}} & \\textbf{{{nfe}}} & \\textbf{{{flops}}} \\\\\n"
            else:
                latex_table += f"{alg} & {nfe} & {flops} \\\\\n"
        latex_table += "\\hline\n\\end{tabular}"
        with open('Total_NFE_FLOPs_Table.tex', 'w') as f:
            f.write(latex_table)
        print("Saved LaTeX table fragment → Total_NFE_FLOPs_Table.tex")

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

# --- 8. ADVANCED VISUALIZATIONS: NFE & FLOPs ---
print("--- Generating NFE and FLOPs Visualizations ---")

# Only proceed if the summary was created
summary_csv = 'Total_NFE_and_FLOPs_Summary.csv'
if not os.path.exists(summary_csv):
    print(f"Warning: {summary_csv} not found. Skipping advanced plots.")
else:
    df_plot = pd.read_csv(summary_csv)

    # Ensure correct order
    df_plot['rank'] = df_plot['Algorithm'].apply(lambda x: target_order.index(x) if x in target_order else 999)
    df_plot = df_plot.sort_values('rank').drop('rank', axis=1)

    # Extract low/high for plotting
    def extract_bounds(s, is_flops=False):
        if pd.isna(s) or 'N/A' in str(s):
            return [0, 0]
        s = str(s).replace('k', '000').replace('approximately', '').replace(' ', '')
        parts = s.replace('--', '-').split('-')
        try:
            low = float(parts[0])
            high = float(parts[1]) if len(parts) > 1 else low
            return [low, high]
        except:
            return [0, 0]

    # 1. Bar Chart: Average Total NFE (with range as error bars)
    plt.figure(figsize=(12, 7))
    low_nfe = [extract_bounds(x)[0] for x in df_plot['Avg Total NFE']]
    high_nfe = [extract_bounds(x)[1] for x in df_plot['Avg Total NFE']]
    mid_nfe = [(l + h) / 2 for l, h in zip(low_nfe, high_nfe)]
    err_nfe = [(m - l, h - m) for l, m, h in zip(low_nfe, mid_nfe, high_nfe)]

    bars = plt.bar(df_plot['Algorithm'], mid_nfe, yerr=np.array(err_nfe).T,
                   capsize=5, color='skyblue', edgecolor='navy', alpha=0.9, label='Total NFE Range')

    # Annotate wins
    for bar, wins in zip(bars, df_plot['Iter Wins']):
        if wins > 0:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                     f"{int(wins)} wins", ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Average Total Function Evaluations (NFE)')
    plt.title('Total Function Evaluations per Problem (Lower = Better)')
    plt.tight_layout()
    plt.savefig('total_nfe_per_algorithm.png', dpi=200)
    plt.close()

    # 2. Bar Chart: Estimated Total FLOPs (in thousands)
    plt.figure(figsize=(12, 7))
    low_flops = [extract_bounds(x, is_flops=True)[0] for x in df_plot['Estimated Total FLOPs (per problem)']]
    high_flops = [extract_bounds(x, is_flops=True)[1] for x in df_plot['Estimated Total FLOPs (per problem)']]
    mid_flops = [(l + h) / 2 for l, h in zip(low_flops, high_flops)]
    err_flops = [(m - l, h - m) for l, m, h in zip(low_flops, mid_flops, high_flops)]

    colors = ['goldenrod' if 'Opt.BFMS' in alg else 'lightcoral' if 'Opt.TFMS' in alg else 'lightgray' 
              for alg in df_plot['Algorithm']]
    bars = plt.bar(df_plot['Algorithm'], mid_flops, yerr=np.array(err_flops).T if any(err_flops) else None,
                   capsize=5, color=colors, edgecolor='black', alpha=0.9)

    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Estimated Total FLOPs (thousands)')
    plt.title('Total Computational Workload per Problem (Lower = Better)')
    plt.tight_layout()
    plt.savefig('total_flops_per_algorithm.png', dpi=200)
    plt.close()

    # 3. Combined Dual-Axis Plot: NFE vs FLOPs
    fig, ax1 = plt.subplots(figsize=(13, 7))

    # NFE (left axis)
    ax1.bar([i - 0.2 for i in range(len(df_plot))], mid_nfe, width=0.4,
            yerr=np.array(err_nfe).T, label='Total NFE', color='steelblue', alpha=0.8, capsize=4)
    ax1.set_ylabel('Total Function Evaluations (NFE)', color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')

    # FLOPs (right axis)
    ax2 = ax1.twinx()
    ax2.bar([i + 0.2 for i in range(len(df_plot))], mid_flops, width=0.4,
            yerr=np.array(err_flops).T if any(err_flops) else None,
            label='Total FLOPs (k)', color='darkorange', alpha=0.8, capsize=4)
    ax2.set_ylabel('Total FLOPs (thousands)', color='darkorange')
    ax2.tick_params(axis='y', labelcolor='darkorange')

    plt.xticks(range(len(df_plot)), df_plot['Algorithm'], rotation=45, ha='right')
    plt.title('Total NFE vs Total FLOPs per Algorithm\n(Lower = Better on Both Axes)')
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.92), ncol=2)
    plt.tight_layout()
    plt.savefig('nfe_vs_flops_comparison.png', dpi=200)
    plt.close()

    # 4. Horizontal Ranked Summary (Best for Paper Figure)
    plt.figure(figsize=(10, 8))
    y_pos = np.arange(len(df_plot))

    # Plot mid points with error bars
    plt.errorbar(mid_flops, y_pos, xerr=np.array(err_flops).T if any(err_flops) else None,
                 fmt='s', markersize=8, capsize=5, color='black', alpha=0.9)

    # Highlight top performers
    for i, alg in enumerate(df_plot['Algorithm']):
        if 'Opt.BFMS' in alg:
            plt.scatter(mid_flops[i], y_pos[i], s=200, color='gold', marker='*', edgecolors='black', zorder=5)
        elif 'Opt.TFMS' in alg:
            plt.scatter(mid_flops[i], y_pos[i], s=150, color='orange', marker='D', zorder=5)

    plt.yticks(y_pos, df_plot['Algorithm'])
    plt.xlabel('Estimated Total FLOPs (thousands) per Problem')
    plt.title('Ranked Total Computational Workload\n(Opt.BFMS = Lowest Workload)')
    plt.gca().invert_yaxis()
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('ranked_total_flops_horizontal.png', dpi=200)
    plt.close()

    print("Generated 4 advanced NFE/FLOPs plots:")
    print("   • total_nfe_per_algorithm.png")
    print("   • total_flops_per_algorithm.png")
    print("   • nfe_vs_flops_comparison.png")
    print("   • ranked_total_flops_horizontal.png (ideal for paper)")