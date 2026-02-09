from src.chaining_hash_table import HashTableChaining


def run() -> None:
    print("=== Hash Table with Chaining (Demo Tests) ===")

    ht = HashTableChaining(initial_capacity=4, seed=42)

    # Insert: Add key-value pairs
    print("\nInsert operations:")
    ht.insert("apple", 10)
    ht.insert("banana", 20)
    ht.insert("orange", 30)
    print("Inserted: apple=10, banana=20, orange=30")

    # Insert update: same key, new value
    ht.insert("banana", 99)
    print("Updated: banana=99")

    # Search: Retrieve values
    print("\nSearch operations:")
    print("search('apple')  ->", ht.search("apple"))
    print("search('banana') ->", ht.search("banana"))
    print("search('grape')  ->", ht.search("grape"))  # not present

    # Delete: Remove key-value pairs
    print("\nDelete operations:")
    print("delete('orange') ->", ht.delete("orange"))
    print("search('orange') ->", ht.search("orange"))

    # Show load factor (helps explain performance)
    print("\nStats:")
    print("items (n)        ->", ht.n)
    print("buckets (m)      ->", ht.m)
    print("load factor (α)  ->", round(ht.load_factor(), 3))


if __name__ == "__main__":
    run()
