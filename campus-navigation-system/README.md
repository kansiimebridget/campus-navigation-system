# Campus Navigation and Resource Management System

BCS 2105 Data Structures and Algorithms, Mountains of the Moon University (November 2026)

## Group members
| No. | Name | Registration number |
|-----|------|---------------------|
| 1 | Kansiime Bridget | 2025/U/MMU/BCS/01600 |
| 2 | Tabisa Azidah | 2025/U/MMU/BCS/01708 |
| 3 | Joseph Istivan | 2025/U/MMU/BCS/00065 |

## Requirements
Python 3.10 or newer. Standard library only (see `requirements.txt`).
The core structures (stack, queue, linked lists, heap, BST, hash table, graph) are our own classes.

## Layout
| File | Content |
|------|---------|
| `task1_analysis.py` | Nested-loop analysis, doubling dynamic array, lookup timing |
| `task2_stack_queue.py` | Bounded stack, queue, circular queue, infix to postfix |
| `task3_linked_list.py` | Singly, doubly and circular linked lists, Floyd cycle detection |
| `task4_trees_heaps.py` | BST, min-heap with pop and replace_root, top-k, heap sort |
| `task5_sort_search_hash.py` | Insertion, merge, quick sort, binary search, three hash tables |
| `task6_campus_system.py` | Graph, DFS, BFS, Dijkstra and the integrated menu program |
| `data/campus_graph.py` | Buildings, walking paths, footfall counts and rooms |
| `docs/` | Report (PDF) and signed contribution statement |

## How to run
Run every command from the repository folder.

```
python task1_analysis.py
python task2_stack_queue.py
python task3_linked_list.py
python task4_trees_heaps.py
python task5_sort_search_hash.py
python task6_campus_system.py          # interactive menu
python task6_campus_system.py --demo   # scripted sample output
```

## Sample menu walkthrough
```
Choice: 1
From: GATE
To: LT4
Route: GATE -> CAF -> LT3 -> LT4 (13 min)

Choice: 2
Room code: LT3-301
LT3-301 is in Lecture Theatre 3 (LT3)

Choice: 4
Top 3 busiest locations (min-heap of size 3):
  1. GATE  Main Gate and Shuttle Stop   1100 visitors/day
  2. LIB   Main Library                 910 visitors/day
  3. CAF   Cafeteria                    870 visitors/day
```

## Git workflow
Feature branches per member, pull requests into `main`, tag `v1.0-submission` for the final hand-in.
