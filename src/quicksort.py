import random
from typing import List, Callable, Tuple


def _partition_3way(arr: List[int], lo: int, hi: int, pivot_index: int) -> Tuple[int, int]:
    """
    3-way partition (Dutch National Flag) to handle duplicates well.

    After partition:
      arr[lo : lt]       < pivot
      arr[lt : gt + 1]   = pivot
      arr[gt + 1 : hi+1] > pivot

    Returns:
      (lt, gt) -> the start and end indices of the "= pivot" region.
    """
    pivot = arr[pivot_index]

    # Move pivot to the start to simplify the partition logic.
    arr[lo], arr[pivot_index] = arr[pivot_index], arr[lo]

    lt = lo          # boundary for "< pivot" region
    i = lo + 1       # current pointer scanning the array
    gt = hi          # boundary for "> pivot" region

    # Scan once and place elements into <, =, > regions.
    while i <= gt:
        if arr[i] < pivot:
            lt += 1
            arr[lt], arr[i] = arr[i], arr[lt]
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
            # Note: we do NOT increment i here because the swapped element at i is unprocessed.
        else:
            # Equal to pivot, just move ahead.
            i += 1

    # Place the pivot into its final position (first element of the "= pivot" region).
    arr[lo], arr[lt] = arr[lt], arr[lo]
    return lt, gt


def _quicksort(
    arr: List[int],
    lo: int,
    hi: int,
    choose_pivot_index: Callable[[int, int], int]
) -> None:
    """
    In-place quicksort helper.

    choose_pivot_index(lo, hi) decides which index to use as pivot.
    We use 3-way partitioning to reduce slowdowns on repeated elements.

    IMPORTANT FIX:
    - We always recurse on the smaller side first.
    - We handle the larger side using a loop.
    This prevents deep recursion and avoids RecursionError.
    """
    # Loop is used so we don't recurse on both sides every time.
    while lo < hi:
        # Choose pivot index using the provided strategy (random or first element).
        pivot_index = choose_pivot_index(lo, hi)

        # Partition into three parts: < pivot, = pivot, > pivot
        lt, gt = _partition_3way(arr, lo, hi, pivot_index)

        # Left side:  lo .. lt-1
        # Right side: gt+1 .. hi
        left_lo, left_hi = lo, lt - 1
        right_lo, right_hi = gt + 1, hi

        # Recurse on the smaller side to keep recursion depth small.
        if (left_hi - left_lo) < (right_hi - right_lo):
            # Left is smaller: recurse left, then loop on right
            if left_lo < left_hi:
                _quicksort(arr, left_lo, left_hi, choose_pivot_index)
            lo, hi = right_lo, right_hi
        else:
            # Right is smaller: recurse right, then loop on left
            if right_lo < right_hi:
                _quicksort(arr, right_lo, right_hi, choose_pivot_index)
            lo, hi = left_lo, left_hi


def randomized_quicksort(arr: List[int], seed: int | None = None) -> List[int]:
    """
    Randomized Quicksort:
    - Chooses pivot uniformly at random from the current subarray.
    - Returns a sorted COPY (does not modify the input list).

    Why random pivot?
    - Avoids worst-case patterns like sorted input causing O(n^2) behavior.
    """
    if seed is not None:
        random.seed(seed)

    a = list(arr)  # work on a copy so caller input stays unchanged

    def choose(lo: int, hi: int) -> int:
        # Uniformly random pivot within [lo, hi]
        return random.randint(lo, hi)

    if len(a) == 0:
        return a

    _quicksort(a, 0, len(a) - 1, choose)
    return a


def deterministic_quicksort_first_pivot(arr: List[int]) -> List[int]:
    """
    Deterministic Quicksort (first element pivot):
    - Always picks the first element as pivot.
    - Returns a sorted COPY.

    Note:
    - Can be very slow (O(n^2)) on already sorted or reverse-sorted arrays.
    """
    a = list(arr)

    def choose(lo: int, hi: int) -> int:
        # Always pick first element as pivot
        return lo

    if len(a) == 0:
        return a

    _quicksort(a, 0, len(a) - 1, choose)
    return a


def is_sorted(arr: List[int]) -> bool:
    """Small helper to verify sorting correctness."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
