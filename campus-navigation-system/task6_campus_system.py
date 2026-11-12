"""Task 6: graph algorithms and the integrated Campus Navigation System.

Run:  python task6_campus_system.py          (menu)
      python task6_campus_system.py --demo   (scripted sample output)
Uses only our own structures (Stack, Queue, MinHeap, BST, ChainedHashTable).
"""
import sys

from data.campus_graph import BUILDINGS, EDGES, FOOTFALL, ROOMS
from task2_stack_queue import Stack, Queue
from task4_trees_heaps import MinHeap, insert, inorder, range_query, top_k
from task5_sort_search_hash import ChainedHashTable

INF = float("inf")


# ---------- 6(a) graph representations ----------
def build_adjacency_list(codes, edges):
    """Adjacency list: list of (neighbour index, minutes) per vertex."""
    index = ChainedHashTable()
    for i, c in enumerate(codes):
        index.put(c, i)
    adj = [[] for _ in codes]
    for a, b, w in edges:
        i, j = index.get(a), index.get(b)
        adj[i].append((j, w))
        adj[j].append((i, w))             # undirected: both directions
    return adj, index


def build_adjacency_matrix(n, adj):
    m = [[0] * n for _ in range(n)]       # 0 means no direct path
    for u in range(n):
        for v, w in adj[u]:
            m[u][v] = w
    return m


# ---------- 6(b) traversals and Dijkstra ----------
def dfs(adj, start, seen=None, order=None):
    seen = seen if seen is not None else [False] * len(adj)
    order = order if order is not None else []
    seen[start] = True
    order.append(start)
    for v, _ in adj[start]:
        if not seen[v]:
            dfs(adj, v, seen, order)
    return order


def bfs(adj, start):
    seen = [False] * len(adj)
    seen[start] = True
    order, q = [], Queue()                # our own Queue, not collections.deque
    q.enqueue(start)
    while not q.is_empty():
        u = q.dequeue()
        order.append(u)
        for v, _ in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.enqueue(v)
    return order


def dijkstra(adj, src, dst):
    n = len(adj)
    dist = [INF] * n
    prev = [None] * n
    dist[src] = 0
    pq = MinHeap()                        # our own heap of (distance, vertex)
    pq.push((0, src))
    while len(pq):
        d, u = pq.pop()
        if d > dist[u]:
            continue                      # stale entry
        if u == dst:
            break
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                pq.push((dist[v], v))
    if dist[dst] == INF:
        return [], INF
    path, node = [], dst
    while node is not None:
        path.append(node)
        node = prev[node]
    return path[::-1], dist[dst]


# ---------- 6(c) integrated system ----------
class CampusSystem:
    def __init__(self):
        self.codes = list(BUILDINGS)
        self.adj, self.index = build_adjacency_list(self.codes, EDGES)
        self.matrix = build_adjacency_matrix(len(self.codes), self.adj)
        self.rooms = ChainedHashTable()               # room code -> building code
        for room, b in ROOMS.items():
            self.rooms.put(room, b)
        self.bst = None                               # sorted building codes
        for c in self.codes:
            self.bst = insert(self.bst, c)
        self.history = Stack(10)
        self.shuttle = Queue()

    # helpers
    def name(self, code):
        return BUILDINGS[code][0]

    def resolve(self, text):
        """Accept a building code or a room code; return a building code or None."""
        text = text.strip().upper()
        if self.index.contains(text):
            return text
        return self.rooms.get(text)

    def route(self, a, b):
        i, j = self.index.get(a), self.index.get(b)
        path, mins = dijkstra(self.adj, i, j)
        return [self.codes[k] for k in path], mins

    # menu actions
    def do_route(self, a, b):
        s, t = self.resolve(a), self.resolve(b)
        if not s or not t:
            print("Unknown building or room.")
            return
        path, mins = self.route(s, t)
        if not path:
            print("No route found.")
            return
        print("Route:", " -> ".join(path), f"({mins} min)")
        self.history.push(t)

    def do_lookup(self, room):
        b = self.resolve(room)
        print(f"{room.upper()} is in {self.name(b)} ({b})" if b else "Not found.")

    def do_list_sorted(self):
        print("Buildings (BST inorder):", ", ".join(inorder(self.bst)))

    def do_range(self, lo, hi):
        print(f"Codes between {lo.upper()} and {hi.upper()}:",
              ", ".join(range_query(self.bst, lo.upper(), hi.upper())))

    def do_top(self, k=3):
        print(f"Top {k} busiest locations (min-heap of size {k}):")
        for rank, (f, c) in enumerate(top_k([(FOOTFALL[c], c) for c in self.codes], k), 1):
            print(f"  {rank}. {c:5s} {self.name(c):28s} {f} visitors/day")

    def do_back(self):
        gone = self.history.pop()
        if gone is None:
            print("History is empty.")
        else:
            print(f"Back from {gone}; now at {self.history.peek() or 'start'}")

    def do_history(self):
        print("History (oldest to newest):", self.history.items)

    def do_join(self, who):
        self.shuttle.enqueue(who)
        print(f"{who} joined the shuttle queue. Waiting: {self.shuttle.to_list()}")

    def do_board(self):
        who = self.shuttle.dequeue()
        print(f"{who} boards. Waiting: {self.shuttle.to_list()}" if who else "Queue is empty.")

    def show_graph(self):
        print("Adjacency list (neighbour, minutes):")
        for i, c in enumerate(self.codes):
            print(f"  {c:5s} -> ", ", ".join(f"({self.codes[v]}, {w})" for v, w in self.adj[i]))
        print("Adjacency matrix (minutes, 0 = no direct path):")
        print("      " + " ".join(f"{c:>4s}" for c in self.codes))
        for i, row in enumerate(self.matrix):
            print(f"  {self.codes[i]:4s}" + " ".join(f"{x:4d}" for x in row))

    def do_traverse(self, start):
        s = self.resolve(start)
        if not s:
            print("Unknown building.")
            return
        i = self.index.get(s)
        print("DFS:", " ".join(self.codes[k] for k in dfs(self.adj, i)))
        print("BFS:", " ".join(self.codes[k] for k in bfs(self.adj, i)))


MENU = """
===== Mountains of the Moon University: Campus Navigation =====
 1 Find shortest route        6 Back (pop history)
 2 Look up a room (hash)      7 Join shuttle queue
 3 List buildings (BST)       8 Board shuttle (dequeue)
 4 Top 3 busiest (heap)       9 Show graph (list + matrix)
 5 Show history              10 DFS / BFS from a building
 0 Exit
"""


def run_menu(cs):
    while True:
        print(MENU)
        ch = input("Choice: ").strip()
        if ch == "1":
            cs.do_route(input("From: "), input("To: "))
        elif ch == "2":
            cs.do_lookup(input("Room code: "))
        elif ch == "3":
            cs.do_list_sorted()
            if input("Range query? (y/n): ").lower() == "y":
                cs.do_range(input("From code: "), input("To code: "))
        elif ch == "4":
            cs.do_top(3)
        elif ch == "5":
            cs.do_history()
        elif ch == "6":
            cs.do_back()
        elif ch == "7":
            cs.do_join(input("Passenger name: "))
        elif ch == "8":
            cs.do_board()
        elif ch == "9":
            cs.show_graph()
        elif ch == "10":
            cs.do_traverse(input("Start: "))
        elif ch == "0":
            print("Goodbye.")
            return
        else:
            print("Invalid choice.")


def run_demo(cs):
    print(">> 9 Show graph"); cs.show_graph()
    print("\n>> 10 DFS / BFS from GATE"); cs.do_traverse("GATE")
    print("\n>> 1 Route GATE -> HST3"); cs.do_route("GATE", "HST3")
    print(">> 1 Route GATE -> LT4"); cs.do_route("GATE", "LT4")
    print(">> 1 Route LT4 -> SPC"); cs.do_route("LT4", "SPC")
    print("\n>> 2 Look up LT3-301 / ANX-S1 / XYZ-9")
    for r in ("LT3-301", "ANX-S1", "XYZ-9"):
        cs.do_lookup(r)
    print("\n>> 3 BST listing and range"); cs.do_list_sorted(); cs.do_range("ANX", "HST3")
    print("\n>> 4 Top 3 busiest"); cs.do_top(3)
    print("\n>> 5 History, then Back x2"); cs.do_history(); cs.do_back(); cs.do_back()
    print("\n>> Shuttle queue")
    for p in ("Asha", "Brian", "Cathy"):
        cs.do_join(p)
    cs.do_board(); cs.do_board()


if __name__ == "__main__":
    system = CampusSystem()
    run_demo(system) if "--demo" in sys.argv else run_menu(system)
