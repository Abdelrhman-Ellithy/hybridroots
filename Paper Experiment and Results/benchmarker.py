import time
import json
import os
import gc
import sympy as sp
import math
import sqlite3
import statistics

class ScientificBenchmark:
    """
    A precision benchmarking tool implementing the 'Single-Loop' strategy 
    with per-call GC control and JIT warm-up.
    Measures time in MICROSECONDS (us).
    """

    def __init__(self, config_file='config.json'):
        self.total_iterations = self._load_config(config_file)

    def _load_config(self, filepath):
        total_iterations = 1000
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_iterations = int(data.get('iterations', 1000))
                    print(f"[Benchmark] Loaded config: Total Reps={total_iterations}")
            except Exception as e:
                print(f"[Benchmark] Config error ({e}). Using defaults.")
        else:
            print("[Benchmark] Config file not found. Using defaults.")
        return total_iterations

    # --- Static Utility Methods ---

    @staticmethod
    def rest_data(db_path='Results.db'):
        """Initialize database with 'iterations' column."""
        con = sqlite3.connect(db_path)
        cursor = con.cursor()
        cursor.execute(""" 
                create table IF NOT EXISTS results(
                id Integer PRIMARY KEY not null,
                problemId Integer problemId not null,
                method_name text,
                CPU_Time REAL,
                iterations Integer
                )""")
        con.commit()
        con.close()

    @staticmethod
    def load_dataset(source='dataset.json'):
        """Load and parse the dataset."""
        if isinstance(source, list):
            return source

        file_path = source
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file '{file_path}' not found.")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dataset = []
        for item in data:
            expr = sp.sympify(item['expression'])
            a = float(item['a'])
            b = float(item['b'])
            dataset.append((expr, a, b))
        return dataset

    @staticmethod
    def record_speeds(records, db_path='Results.db'):
        """Batch insert records into the database."""
        try:
            with sqlite3.connect(db_path) as con:
                cursor = con.cursor()
                cursor.executemany(
                    "INSERT INTO results (problemId, method_name, CPU_Time, iterations) VALUES (?, ?, ?, ?)", 
                    records
                )
                con.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    # --- Core Run Method ---

    def run(self, algorithm_func, method_name, dataset=None, tol=1e-14, **algo_kwargs):
        """
        Executes the benchmark using a single loop with per-call timing.
        Appends EVERY individual run (in Microseconds) to the records list.
        """
        records = []
        
        # --- SMART DATASET LOADING ---
        if dataset is None:
            print("[Benchmark] No dataset provided. Auto-loading 'dataset.json'...")
            try:
                dataset = self.load_dataset('dataset.json')
            except Exception as e:
                print(f"[Error] Could not auto-load dataset: {e}")
                return []
        elif isinstance(dataset, str):
             print(f"[Benchmark] Loading dataset from '{dataset}'...")
             dataset = self.load_dataset(dataset)
        # -----------------------------

        print(f"\n--- Benchmarking: {method_name} ---")
        print(f"Strategy: Single Loop over {self.total_iterations} repetitions")
        print(f"Storage: Appending RAW results (Total: {len(dataset) * self.total_iterations} records)")
        if algo_kwargs:
            print(f"Params: {algo_kwargs}")
        print("-" * 90)
        print(f"{'ProbID':<8} {'Status':<10} {'Iter':<6} {'Root':<15} {'Avg Time (us)':<20}")
        print("-" * 90)

        # 1. PRE-COMPILATION PHASE
        prepared_data = []
        for item in dataset:
            func_expr, a, b = item
            f_lambda = sp.lambdify('x', func_expr, 'numpy')
            prepared_data.append((f_lambda, a, b))

        # 2. BENCHMARKING PHASE
        for i, (f, a, b) in enumerate(prepared_data):
            
            # A. WARMUP
            try:
                algorithm_func(f, a, b, tol, **algo_kwargs)
            except Exception:
                pass 

            times_us = []
            final_result = None
            
            # B. SINGLE LOOP EXECUTION
            for _ in range(self.total_iterations):
                
                # C. GC CONTROL & TIMING
                gc.disable()
                try:
                    t1 = time.perf_counter_ns()
                    res = algorithm_func(f, a, b, tol, **algo_kwargs)
                    t2 = time.perf_counter_ns()
                    
                    gc.enable() # Re-enable immediately
                    
                    # CONVERT TO MICROSECONDS (us)
                    duration_us = (t2 - t1) / 1000.0
                    
                    times_us.append(duration_us)
                    final_result = res
                    
                except Exception:
                    gc.enable()
                    final_result = None
                    break

            # F. RESULT PARSING
            status = "Error"
            root_str = "---"
            iters = 0
            
            if final_result:
                try:
                    if isinstance(final_result, tuple) and len(final_result) >= 2:
                        n, x_val = final_result[0], final_result[1]
                        iters = n if n is not None else 0
                        status = "Success" if n else "Failed"
                        root_str = f"{x_val:.8f}" if x_val is not None else "None"
                    else:
                        status = "Done"
                        root_str = str(final_result)[:10]
                except Exception:
                    pass

            # --- APPEND RAW DATA (in Microseconds) ---
            for raw_time in times_us:
                records.append((i + 1, method_name, raw_time, iters))

            # For Console Display ONLY: Calculate summary average
            if times_us:
                avg_us_display = statistics.mean(times_us)
                time_str = f"{avg_us_display:,.2f}"
            else:
                time_str = "NaN"

            print(f"{i+1:<8} {status:<10} {iters:<6} {root_str:<15} {time_str}")

        return records