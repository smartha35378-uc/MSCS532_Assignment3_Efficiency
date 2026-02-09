This repository contains implementations and empirical evaluations for:

- Randomized and deterministic Quicksort (`src/quicksort.py`) 
- A chaining hash table (`src/chaining_hash_table.py`) 
- Evaluation scripts for measurements (`evaluations/evaluations_quicksort.py`, `evaluations/evaluations_hash_table.py`)

## Requirements

- Python 3.8+ (tested with macOS)

## How to run

1. From the repository root, run unit / evaluation scripts with Python. Example for quicksort evaluations:

```bash
python3 evaluations/evaluations_quicksort.py
```

2. For hashing evaluations:

```bash
python3 evaluations/evaluations_hash_table.py
```

3. Review printed output in the terminal for median runtimes and correctness checks. Data tables and figures are produced by the evaluation scripts (if enabled in the script).

## Project structure

- `src/` — algorithm implementations (`quicksort.py`, `chaining_hash_table.py`)
- `evaluations/` — scripts to run timing and correctness experiments
- `report/` — Markdown report summarizing methods and results

## Summary of findings

- Randomized Quicksort: Expected time is $O(n\\log n)$ and empirically resists adversarial input orders (sorted and reverse-sorted), showing far better runtimes than deterministic first-pivot Quicksort on those inputs.
- Deterministic Quicksort: Using the first element as pivot can degrade to $O(n^2)$ on sorted or reverse-sorted inputs; occasionally faster on small random inputs due to lower overhead.
- Hashing with chaining: With a low load factor (e.g., $\\alpha=0.5$) operations perform near-constant time $O(1+\\alpha)$; dynamic resizing and good hash functions are important to maintain performance.

## Notes

- If evaluation scripts fail, verify Python path and that you run from repository root.
- To reproduce graphs/tables, ensure any plotting dependencies (e.g., `matplotlib`) are installed and enabled in the evaluation scripts.
