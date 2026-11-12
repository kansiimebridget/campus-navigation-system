"""Task 3: singly, doubly and circular linked lists; Floyd cycle detection."""


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class StopList:
    """Singly linked list of shuttle stops."""

    def __init__(self):
        self.head = None

    def insert_head(self, val):
        n = Node(val)
        n.next = self.head
        self.head = n

    def insert_tail(self, val):
        n = Node(val)
        if self.head is None:
            self.head = n
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = n

    def delete(self, val):
        if self.head is None:
            return
        if self.head.val == val:
            self.head = self.head.next
            return
        cur = self.head
        while cur.next and cur.next.val != val:
            cur = cur.next
        if cur.next:
            cur.next = cur.next.next

    def traverse(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.val)
            cur = cur.next
        return out


class DNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


def unlink(node):
    """Remove a node we already hold in O(1)."""
    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev
    node.prev = node.next = None


def has_cycle(head):
    """Floyd's tortoise and hare, O(n) time, O(1) space."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


class CircularStopList:
    """Bonus 3(e): circular singly linked list for a looping shuttle route.
    Only a tail pointer is kept; tail.next is the head, so insert at both ends is O(1)."""

    def __init__(self):
        self.tail = None

    def insert_tail(self, val):
        n = Node(val)
        if self.tail is None:
            n.next = n
        else:
            n.next = self.tail.next
            self.tail.next = n
        self.tail = n

    def delete(self, val):
        if self.tail is None:
            return
        prev, cur = self.tail, self.tail.next
        while True:
            if cur.val == val:
                if cur is prev:               # only one node
                    self.tail = None
                else:
                    prev.next = cur.next
                    if cur is self.tail:
                        self.tail = prev
                return
            if cur is self.tail:
                return
            prev, cur = cur, cur.next

    def laps(self, steps):
        """Walk `steps` stops round the loop, starting at the head."""
        out = []
        if self.tail is None:
            return out
        cur = self.tail.next
        for _ in range(steps):
            out.append(cur.val)
            cur = cur.next
        return out


if __name__ == "__main__":
    s = StopList()
    for stop in ["GATE", "LIB", "CAF"]:
        s.insert_tail(stop)
    s.insert_head("ADM")
    print("stops:", s.traverse())
    s.delete("LIB")
    print("after delete LIB:", s.traverse())
    print("cycle in plain list?", has_cycle(s.head))
    last = s.head
    while last.next:
        last = last.next
    last.next = s.head.next
    print("cycle after linking last to second?", has_cycle(s.head))
    c = CircularStopList()
    for stop in ["GATE", "LIB", "CAF", "HST1"]:
        c.insert_tail(stop)
    print("loop, 6 steps:", c.laps(6))
    c.delete("CAF")
    print("after delete CAF, 5 steps:", c.laps(5))
