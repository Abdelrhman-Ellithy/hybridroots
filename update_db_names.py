import sqlite3
import os

def update_method_names(db_path='Results.db'):
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        return

    # The mapping of Old Name -> New Name
    name_mapping = {
   #     "09-Optimized_Trisection-FalsePosition-Modified Secant": "Opt.TFMS",
    #    "07-Optimized-Bisection-FalsePosition-Modified Secant": "Opt.BFMS",
     #   "08-Optimized-Trisection-FalsePosition": "Opt.TF",
      #  "04-Badr-2021-A Comparative Study among New Hybrid Root Finding Algorithms-Hybrid-Blend-Trisection-Falseposition": "HybridBlendTF",
       # "12-Quadratic-Interval-Refinement": "QIR",
     #   "06-Optimized-Bisection-FalsePosition": "Opt.BF",
     #   "HybridBlendBF": "HybridBlendBF",
     #   "Brent(SciPy)": "Brent (SciPy)",
     #   "Bisection": "Bisection",
     #   "Trisection": "Trisection",
     #   "FalsePosition": "False Position",
        "Brent(Impl.)": "Brent (Impl.)"
    }

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"--- Updating Method Names in {db_path} ---")
        
        total_changes = 0
        
        for old_name, new_name in name_mapping.items():
            # SQL Update Query
            query = "UPDATE results SET method_name = ? WHERE method_name = ?"
            cursor.execute(query, (new_name, old_name))
            
            rows_affected = cursor.rowcount
            if rows_affected > 0:
                print(f"Updated {rows_affected:>5} rows: '{old_name}' -> '{new_name}'")
                total_changes += rows_affected
        
        conn.commit()
        conn.close()
        
        print("-" * 60)
        print(f"Success! Total rows updated: {total_changes}")
        
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

if __name__ == "__main__":
    update_method_names()