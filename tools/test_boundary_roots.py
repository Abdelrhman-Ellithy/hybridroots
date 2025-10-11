import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'dataset.json'

def load_problems(indices):
    with open(DATASET, 'r') as f:
        data = json.load(f)
    # indices are 1-based
    return [(i+1, item) for i, item in enumerate(data) if (i+1) in indices]

def run_script(script, prob_index, item):
    # Run the script but override dataset to a temporary small file
    tmp = ROOT / 'tools' / f'tmp_problem_{prob_index}.json'
    with open(tmp, 'w') as f:
        json.dump([item], f)
    cmd = [sys.executable, str(ROOT / script)]
    # set env to let script read tmp file by passing a small hack: it uses default dataset.json
    # so replace dataset.json temporarily
    orig = ROOT / 'dataset.json'
    backup = ROOT / 'dataset.json.bak'
    orig.replace(backup)
    tmp.replace(orig)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        out = p.stdout
    except Exception as e:
        out = f'ERROR: {e}'
    finally:
        # restore
        (ROOT / 'dataset.json').replace(tmp)
        backup.replace(orig)
    return out

def extract_result(output):
    # find the line that starts with 'problem1|' in the output
    for line in output.splitlines():
        if line.strip().startswith('problem1|'):
            return line.strip()
    return output.splitlines()[-1] if output.splitlines() else ''

def main():
    problems = load_problems([26, 40])
    scripts = [
        '06-Optimized-Bisection-FalsePosition.py',
        '07-Optimized_Bisection-FalsePosition-Modified-Secant.py',
        '08-Optimized-Trisection-FalsePosition.py',
        '09-Optimized-Trisection-FalsePosition-Modified-Secant.py'
    ]
    for idx, item in problems:
        print(f'=== Problem {idx} ===')
        for s in scripts:
            out = run_script(s, idx, item)
            res = extract_result(out)
            print(f'{s}: {res}')

if __name__ == '__main__':
    main()
