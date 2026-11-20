# ICE-2202: Data Structure and Algorithm Sessional

Lab program built from the course syllabus: linear and non-linear data structures, sorting and searching, greedy algorithms, dynamic programming and backtracking.

These are written from the syllabus topics. They are not my original lab questions, which I no longer have.

## Contents

`python/dsa_lab.py` covers:

- Linked list with reversal, binary search tree with inorder traversal and height
- Bracket matching and postfix evaluation with a stack
- Bubble, insertion, merge, quick and heap sort, checked against `sorted`, plus a timing comparison
- Binary search
- Activity selection and fractional knapsack (greedy)
- 0/1 knapsack, longest common subsequence, edit distance (dynamic programming)
- N-Queens (backtracking): 2, 10, 4, 40, 92 solutions for n = 4 to 8

Outputs: `results/dsa_output.txt` and `results/sorting_times.png`.

## Run

```bash
pip install matplotlib
python python/dsa_lab.py
```

## Notes and limitations

- Timings depend on the machine. The ordering (bubble slowest, heap and quick fastest) is what matters, not the exact milliseconds.
- Heap sort here uses Python's `heapq`, so it is faster than a hand-written one would be.
