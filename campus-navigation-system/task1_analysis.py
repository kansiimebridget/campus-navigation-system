"""Task 1: algorithm analysis, nested loop, amortised dynamic array, timing."""
import time

from task5_sort_search_hash import ChainedHashTable


def count_equal_pairs(A):
    count = 0
    n = len(A)
    for i in range(n):            # runs n times
        for j in range(n):        # runs n times per i -> n*n comparisons
            if A[i] == A[j]:
                count += 1
    return count


def count_equal_pairs_fast(A):
    """O(n) average alternative. Uses Python dict for illustration only;
    it is NOT part of the campus system."""
    freq = {}
    for x in A:
        freq[x] = freq.get(x, 0) + 1
    return sum(f * f for f in freq.values())


class DynArray:
    """Doubling dynamic array that counts the elements it copies."""

    def __init__(self):
        self.cap = 1
        self.n = 0
        self.data = [None] * self.cap
        self.copies = 0

    def append(self, x):
        if self.n == self.cap:
            self.cap *= 2
            new = [None] * self.cap
            for i in range(self.n):
                new[i] = self.data[i]
                self.copies += 1
            self.data = new
        self.data[self.n] = x
        self.n += 1


def time_it(fn, repeats=100000):
    t0 = time.perf_counter()
    for _ in range(repeats):
        fn()
    return (time.perf_counter() - t0) / repeats * 1e6   # microseconds per call


def lookup_timing(codes=None, repeats=100000):
    """List scan versus our own hash table on the campus building codes."""
    if codes is None:
        from data.campus_graph import BUILDINGS
        codes = list(BUILDINGS)
    table = ChainedHashTable(size=17)
    for c in codes:
        table.put(c, True)
    target = codes[-1]                       # worst case for the scan

    def scan():
        for c in codes:
            if c == target:
                return True

    return time_it(scan, repeats), time_it(lambda: table.get(target), repeats)


if __name__ == "__main__":
    A = [1, 2, 1, 3, 2, 1]
    print("pairs (n^2 loop):", count_equal_pairs(A), " pairs (fast):", count_equal_pairs_fast(A))
    d = DynArray()
    print("append | capacity-after | running copies")
    for k in range(1, 9):
        d.append(k)
        print(f"{k:6d} | {d.cap:14d} | {d.copies}")
    print("operations for 8 appends:", d.copies + 8, "(bound 3n =", 24, ")")
    scan_us, hash_us = lookup_timing()
    print(f"worst-case list scan: {scan_us:.3f} us   own hash table: {hash_us:.3f} us  (13 buildings)")
