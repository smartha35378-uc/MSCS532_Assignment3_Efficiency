import time
import random
from statistics import median
from typing import List, Callable, Dict

from src.quicksort import randomized_quicksort, deterministic_quicksort_first_pivot, is_sorted


# ---------- Edge Case Tests (Correctness Only) ----------

def edge_case_tests() -> None:
    """
    Correctness-only tests to explicitly show that edge cases
    required by the assignment are handled correctly.
    These are NOT performance benchmarks.
    """
    print("=== Edge Case Tests (Correctness Only) ===")

    tests = {
        "empty array": [],
        "single element": [7],
        "already sorted": [1, 2, 3, 4, 5],
        "reverse sorted": [5, 4, 3, 2, 1],
        "repeated elements": [3, 3, 3, 3, 3],
    }

    for name, arr in tests.items():
        r = randomized_quicksort(arr, seed=1)
        d = deterministic_quicksort_first_pivot(arr)

        # Print True/False so it is clear that correctness was verified
        print(
            f"{name:18} | randomized sorted={is_sorted(r)} "
            f"| deterministic sorted={is_sorted(d)}"
        )

    print()  # blank line after edge-case section


# ---------- Input generators (different distributions) ----------

def make_random_array(n: int, low: int = 0, high: int = 10**6) -> List[int]:
    """Random integers across a wide range."""
    return [random.randint(low, high) for _ in range(n)]


def make_sorted_array(n: int) -> List[int]:
    """Already sorted (common worst-case for first-pivot quicksort)."""
    return list(range(n))


def make_reverse_sorted_array(n: int) -> List[int]:
    """Reverse sorted (also bad for first-pivot quicksort)."""
    return list(range(n, 0, -1))


def make_repeated_array(n: int, distinct: int = 5) -> List[int]:
    """Many duplicates (only 'distinct' unique values)."""
    return [random.randint(0, distinct - 1) for _ in range(n)]


# ---------- Timing helper ----------

def time_fn(fn: Callable[[List[int]], List[int]], arr: List[int], repeats: int = 5) -> float:
    """
    Measure runtime of a sorting function.
    - Uses median to reduce noise.
    - Checks correctness (must be sorted).
    """
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        out = fn(arr)
        end = time.perf_counter()

        # Always validate correctness so we don't time a broken algorithm.
        assert is_sorted(out), "Output is not sorted"

        times.append(end - start)

    return median(times)


def run() -> None:
    # Fixed seed so results are reproducible
    random.seed(42)

    # 1) Run edge-case correctness tests first (includes empty array)
    edge_case_tests()

    # Input sizes to test (increase if your machine can handle more)
    sizes = [1_000, 2_000, 5_000, 10_000, 20_000]

    # Different distributions to see behavior under different patterns
    distributions = {
        "random": make_random_array,
        "sorted": make_sorted_array,
        "reverse_sorted": make_reverse_sorted_array,
        "repeated": make_repeated_array,
    }

    # Algorithms to compare
    algos: Dict[str, Callable[[List[int]], List[int]]] = {
        # Seed inside randomized_quicksort so comparisons are consistent across runs
        "randomized_quicksort": lambda a: randomized_quicksort(a, seed=123),
        "deterministic_first_pivot": deterministic_quicksort_first_pivot,
    }

    print("Median runtime (milliseconds) over repeats\n")

    for dist_name, dist_fn in distributions.items():
        print(f"=== Distribution: {dist_name} ===")

        for n in sizes:
            # Build the base input array
            if dist_name == "random":
                base = dist_fn(n, 0, 10**6)
            elif dist_name == "repeated":
                base = dist_fn(n, distinct=5)
            else:
                base = dist_fn(n)

            # Time each algorithm on the same input
            row = [f"n={n:>6}"]
            for algo_name, algo_fn in algos.items():
                t_seconds = time_fn(algo_fn, base, repeats=5)
                row.append(f"{algo_name}: {t_seconds * 1000:.3f} ms")

            print(" | ".join(row))

        print()  # blank line after each distribution


if __name__ == "__main__":
    run()
