import random
from typing import Any, Optional, List, Tuple


class HashTableChaining:
    """
    Hash table using chaining (each bucket holds a list of (key, value) pairs).

    Main idea:
    - Hash key -> bucket index
    - If collisions happen, store multiple items in the same bucket list

    Hash function (universal-hashing style):
      index = ((a * hash(key) + b) mod p) mod m
    where:
      m = number of buckets (table size)
      p = large prime
      a, b = random parameters chosen once (and again on resize)
    """

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.75, seed: int = 123):
        # Keep capacity at least 2
        if initial_capacity < 2:
            initial_capacity = 2

        # Using power-of-two capacity makes resizing simple
        self.m = self._next_power_of_two(initial_capacity)

        # Threshold after which we resize (keeps chains short)
        self.max_load_factor = max_load_factor

        # Number of stored key-value pairs
        self.n = 0

        # Table: list of buckets, each bucket is a list of (key, value)
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.m)]

        # Random seed for reproducible a,b selection
        random.seed(seed)

        # Large prime used in modulo step (helps distribute values)
        self.p = 2_147_483_647

        # Random parameters for universal-style hashing
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

    def _next_power_of_two(self, x: int) -> int:
        """Return smallest power of two >= x."""
        p = 1
        while p < x:
            p <<= 1
        return p

    def _index(self, key: Any) -> int:
        """
        Convert a key into a bucket index [0, m-1].
        We use Python's built-in hash() and then mix it with a,b.
        """
        hk = hash(key)

        # Make it non-negative to avoid negative modulo quirks across Python versions
        hk = hk & 0x7FFFFFFF

        return ((self.a * hk + self.b) % self.p) % self.m

    def load_factor(self) -> float:
        """
        Load factor α = n / m.
        - n = number of items
        - m = number of buckets
        Higher α => longer chains => slower operations.
        """
        return self.n / self.m

    def _resize(self, new_capacity: int) -> None:
        """
        Resize the table and rehash all items.
        This is how we keep load factor low.
        """
        # Collect existing items
        old_items = []
        for bucket in self.table:
            for k, v in bucket:
                old_items.append((k, v))

        # Create a new empty table
        self.m = self._next_power_of_two(new_capacity)
        self.table = [[] for _ in range(self.m)]
        self.n = 0

        # Pick new a,b to reduce clustering after resize
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

        # Reinsert everything into the new table
        for k, v in old_items:
            self.insert(k, v)

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert or update a (key, value) pair.

        Expected time: O(1 + α) under uniform hashing.
        """
        # If too full, grow the table (keeps α small)
        if self.load_factor() > self.max_load_factor:
            self._resize(self.m * 2)

        idx = self._index(key)
        bucket = self.table[idx]

        # If key exists, update it
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Otherwise, add new key-value pair
        bucket.append((key, value))
        self.n += 1

    def search(self, key: Any) -> Optional[Any]:
        """
        Find a key and return its value, or None if not found.

        Expected time: O(1 + α)
        """
        idx = self._index(key)
        bucket = self.table[idx]

        # Linear scan of the bucket chain
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        """
        Delete a key-value pair if present.
        Returns True if deleted, False otherwise.

        Expected time: O(1 + α)
        """
        idx = self._index(key)
        bucket = self.table[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.n -= 1

                # Optional: shrink when mostly empty (saves memory)
                if self.m > 8 and self.load_factor() < 0.20:
                    self._resize(self.m // 2)

                return True

        return False
