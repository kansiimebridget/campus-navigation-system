"""Task 4: BST, min-heap (own), top-k, heap sort."""


class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def insert(root, key):
    if root is None:
        return BSTNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root


def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = root.right
        while succ.left:
            succ = succ.left
        root.key = succ.key
        root.right = delete(root.right, succ.key)
    return root


def search(root, key):
    while root:
        if key == root.key:
            return True
        root = root.left if key < root.key else root.right
    return False


def inorder(r):
    return inorder(r.left) + [r.key] + inorder(r.right) if r else []


def preorder(r):
    return [r.key] + preorder(r.left) + preorder(r.right) if r else []


def postorder(r):
    return postorder(r.left) + postorder(r.right) + [r.key] if r else []


def height(r):
    return 0 if r is None else 1 + max(height(r.left), height(r.right))


def range_query(r, lo, hi):
    """All keys with lo <= key <= hi, in sorted order (a BST strength)."""
    if r is None:
        return []
    out = []
    if lo < r.key:
        out += range_query(r.left, lo, hi)
    if lo <= r.key <= hi:
        out.append(r.key)
    if r.key < hi:
        out += range_query(r.right, lo, hi)
    return out


class MinHeap:
    """Binary min-heap in a flat array. Items must support < (e.g. tuples)."""

    def __init__(self):
        self.a = []

    def __len__(self):
        return len(self.a)

    def peek(self):
        return self.a[0] if self.a else None

    def push(self, x):
        self.a.append(x)
        self._sift_up(len(self.a) - 1)

    def pop(self):
        """Remove and return the smallest item."""
        if not self.a:
            return None
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self._sift_down(0)
        return top

    def replace_root(self, x):
        """Pop the smallest and push x in one O(log n) step; returns old root."""
        old = self.a[0]
        self.a[0] = x
        self._sift_down(0)
        return old

    def _sift_up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.a[p] <= self.a[i]:
                break
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def _sift_down(self, i):
        n = len(self.a)
        while True:
            l, r, small = 2 * i + 1, 2 * i + 2, i
            if l < n and self.a[l] < self.a[small]:
                small = l
            if r < n and self.a[r] < self.a[small]:
                small = r
            if small == i:
                break
            self.a[i], self.a[small] = self.a[small], self.a[i]
            i = small


def top_k(pairs, k):
    """k largest (value, label) pairs using our own MinHeap, O(n log k)."""
    heap = MinHeap()
    for p in pairs:
        if len(heap) < k:
            heap.push(p)
        elif p > heap.peek():
            heap.replace_root(p)
    out = []
    while len(heap):
        out.append(heap.pop())
    return out[::-1]                      # busiest first


def sift_down_max(a, i, n):
    while True:
        left, right, largest = 2 * i + 1, 2 * i + 2, i
        if left < n and a[left] > a[largest]:
            largest = left
        if right < n and a[right] > a[largest]:
            largest = right
        if largest == i:
            break
        a[i], a[largest] = a[largest], a[i]
        i = largest


def heap_sort(a, trace=False):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down_max(a, i, n)
    if trace:
        print("max-heap built:", a)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down_max(a, 0, end)
        if trace:
            print(f"after extract (heap size {end}):", a[:end], "|", a[end:])
    return a


if __name__ == "__main__":
    root = None
    for code in ["LIB", "HST", "LEC1", "ADM", "GYM", "SPC", "CAF", "MED", "SCI", "LEC2"]:
        root = insert(root, code)
    print("height:", height(root))
    print("inorder  :", inorder(root))
    print("preorder :", preorder(root))
    print("postorder:", postorder(root))
    root = delete(root, "HST")
    print("after deleting HST, preorder:", preorder(root))
    print("range ADM..LIB:", range_query(root, "ADM", "LIB"))

    from data.campus_graph import FOOTFALL
    vals = list(FOOTFALL.values())[:8]
    h = MinHeap()
    print("min-heap build from footfall", vals)
    for v in vals:
        h.push(v)
        print(f"  insert {v:5d} -> {h.a}")
    print("top 3 busiest:", top_k([(f, c) for c, f in FOOTFALL.items()], 3))
    print("heap sort trace:")
    print(heap_sort([45, 12, 78, 33, 22, 90, 56], trace=True))
