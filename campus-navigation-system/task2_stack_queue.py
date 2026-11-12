"""Task 2: stacks and queues (own implementations, no collections.deque)."""


class Stack:
    """Navigation history that remembers only the last `limit` buildings."""

    def __init__(self, limit=10):
        self.items = []
        self.limit = limit

    def push(self, x):
        if len(self.items) == self.limit:
            self.items.pop(0)            # drop oldest visit, O(n) but limit is 10
        self.items.append(x)

    def pop(self):
        return self.items.pop() if self.items else None

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


class Queue:
    """Shuttle queue: list plus head index so dequeue is O(1)."""

    def __init__(self):
        self.items = []
        self.head = 0

    def enqueue(self, x):
        self.items.append(x)

    def dequeue(self):
        if self.is_empty():
            return None
        x = self.items[self.head]
        self.items[self.head] = None     # release the reference
        self.head += 1
        return x

    def front(self):
        return None if self.is_empty() else self.items[self.head]

    def is_empty(self):
        return self.head == len(self.items)

    def to_list(self):
        return self.items[self.head:]

    def __len__(self):
        return len(self.items) - self.head


PREC = {'+': 1, '-': 1, '*': 2, '/': 2}


def infix_to_postfix(tokens, trace=False):
    out, stack = [], []
    for t in tokens:
        if t in PREC:
            while stack and PREC[stack[-1]] >= PREC[t]:   # >= : left associative
                out.append(stack.pop())
            stack.append(t)
        else:
            out.append(t)
        if trace:
            print(f"{t:>3} | stack {stack} | output {out}")
    while stack:
        out.append(stack.pop())
    if trace:
        print(f"end | stack {stack} | output {out}")
    return out


class CircularQueue:
    """Fixed-capacity queue that reuses freed slots with modulo arithmetic."""

    def __init__(self, capacity):
        self.data = [None] * capacity
        self.cap = capacity
        self.front = 0
        self.size = 0

    def enqueue(self, x):
        if self.size == self.cap:
            return False
        self.data[(self.front + self.size) % self.cap] = x
        self.size += 1
        return True

    def dequeue(self):
        if self.size == 0:
            return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.cap
        self.size -= 1
        return x


if __name__ == "__main__":
    h = Stack(3)
    for b in ["GATE", "LIB", "CAF", "LT1"]:
        h.push(b)
    print("history (limit 3):", h.items, "| back ->", h.pop(), "| now on", h.peek())
    q = Queue()
    for s in ["Asha", "Brian", "Cathy"]:
        q.enqueue(s)
    print("shuttle queue:", q.to_list(), "| boards:", q.dequeue(), "| waiting:", q.to_list())
    print("A + B * C - D / E ->", " ".join(infix_to_postfix("A + B * C - D / E".split(), trace=True)))
    c = CircularQueue(3)
    print([c.enqueue(x) for x in "abcd"], c.dequeue(), c.enqueue("d"), c.data)
