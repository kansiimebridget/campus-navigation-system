"""Task 5: sorting, binary search, hash tables (own classes)."""
import random


def insertion_sort(a, trace=False):
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
        if trace:
            print(a)
    return a


def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def quick_sort(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        p = random.randint(lo, hi)
        a[p], a[hi] = a[hi], a[p]
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        quick_sort(a, lo, i - 1)
        quick_sort(a, i + 1, hi)
    return a


def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


class LinearProbeTable:
    def __init__(self, size=11):
        self.size = size
        self.slots = [None] * size

    def insert(self, key):
        i = key % self.size
        probes = 1
        while self.slots[i] is not None:
            i = (i + 1) % self.size
            probes += 1
            if probes > self.size:
                raise OverflowError("table full")
        self.slots[i] = key
        return i, probes


class ChainedTable:
    """Integer-key chaining table used for the Task 5(e) trace."""

    def __init__(self, size=11):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def insert(self, key):
        self.buckets[key % self.size].append(key)

    def search(self, key):
        steps = 0
        for k in self.buckets[key % self.size]:
            steps += 1
            if k == key:
                return steps
        return None


class DoubleHashTable:
    def __init__(self, size=11):
        self.size = size
        self.slots = [None] * size

    def h2(self, key):
        return 7 - (key % 7)

    def insert(self, key):
        i, step = key % self.size, self.h2(key)
        for _ in range(self.size):
            if self.slots[i] is None:
                self.slots[i] = key
                return i
            i = (i + step) % self.size
        raise OverflowError("table full")


class ChainedHashTable:
    """String-key hash table (separate chaining), our own class.
    Used by the campus system for room and building lookup. No Python dict."""

    def __init__(self, size=17):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        h = 0
        for ch in key:                       # polynomial rolling hash, base 31
            h = (h * 31 + ord(ch)) % self.size
        return h

    def put(self, key, value):
        chain = self.buckets[self._hash(key)]
        for pair in chain:
            if pair[0] == key:
                pair[1] = value              # update existing key
                return
        chain.append([key, value])
        self.count += 1
        if self.count > 2 * self.size:       # keep chains short
            self._grow()

    def get(self, key, default=None):
        for k, v in self.buckets[self._hash(key)]:
            if k == key:
                return v
        return default

    def contains(self, key):
        for k, _ in self.buckets[self._hash(key)]:
            if k == key:
                return True
        return False

    def keys(self):
        return [k for chain in self.buckets for k, _ in chain]

    def _grow(self):
        old = self.buckets
        self.size = self.size * 2 + 1
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        for chain in old:
            for k, v in chain:
                self.put(k, v)


if __name__ == "__main__":
    print("insertion sort trace:")
    insertion_sort([12, 11, 13, 5, 6], trace=True)
    print("merge sort:", merge_sort([12, 11, 13, 5, 6]))
    print("quick sort:", quick_sort([12, 11, 13, 5, 6]))
    print("binary search 12 in [5,6,11,12,13]:", binary_search([5, 6, 11, 12, 13], 12))
    keys = [22, 41, 53, 46, 30, 13, 1, 67]
    lp, ch, dh = LinearProbeTable(), ChainedTable(), DoubleHashTable()
    total = 0
    for k in keys:
        slot, p = lp.insert(k)
        total += p
        ch.insert(k)
        print(f"key {k:3d}: home {k % 11:2d} slot {slot:2d} probes {p}")
        dh.insert(k)
    print("linear table:", lp.slots, "total probes", total)
    print("chains:", [(i, b) for i, b in enumerate(ch.buckets) if b])
    print("search 67: linear probes 4, chaining steps", ch.search(67))
    print("double hashing table:", dh.slots)
    t = ChainedHashTable()
    t.put("LIB-G1", "LIB")
    print("string table lookup:", t.get("LIB-G1"), t.get("XXX"))
