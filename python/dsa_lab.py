"""ICE-2202 style lab: data structures, sorting, searching, greedy, dynamic programming, backtracking."""
import os, time, random, heapq, bisect
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(__file__), "..", "results"); lines = []
def say(s=""): print(s); lines.append(s)

class Node:
    def __init__(self, v): self.v, self.next = v, None
class LinkedList:
    def __init__(self): self.head = None
    def push(self, v): n = Node(v); n.next = self.head; self.head = n
    def reverse(self):
        prev = None
        while self.head: nxt = self.head.next; self.head.next = prev; prev = self.head; self.head = nxt
        self.head = prev
    def items(self):
        out, c = [], self.head
        while c: out.append(c.v); c = c.next
        return out
class BST:
    def __init__(self): self.root = None
    def insert(self, v):
        def go(n):
            if not n: return [v, None, None]
            if v < n[0]: n[1] = go(n[1])
            else: n[2] = go(n[2])
            return n
        self.root = go(self.root)
    def inorder(self, n="x"):
        n = self.root if n == "x" else n
        return [] if not n else self.inorder(n[1]) + [n[0]] + self.inorder(n[2])
    def height(self, n="x"):
        n = self.root if n == "x" else n
        return 0 if not n else 1 + max(self.height(n[1]), self.height(n[2]))
def balanced(s):
    st, pair = [], {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in "([{": st.append(c)
        elif c in pair:
            if not st or st.pop() != pair[c]: return False
    return not st
def postfix(expr):
    st = []
    for t in expr.split():
        if t.lstrip("-").isdigit(): st.append(int(t))
        else: b, a = st.pop(), st.pop(); st.append({"+": a + b, "-": a - b, "*": a * b, "/": a // b}[t])
    return st[0]
say("== Linear and tree structures ==")
ll = LinkedList(); [ll.push(i) for i in range(1, 6)]; before = ll.items(); ll.reverse(); say("Linked list %s reversed -> %s" % (before, ll.items()))
bst = BST(); [bst.insert(v) for v in [50, 30, 70, 20, 40, 60, 80, 35]]; say("BST inorder: %s, height %d" % (bst.inorder(), bst.height()))
say("Balanced brackets: '{[()]}' -> %s, '{[(])}' -> %s" % (balanced("{[()]}"), balanced("{[(])}"))); say("Postfix '5 1 2 + 4 * + 3 -' = %d" % postfix("5 1 2 + 4 * + 3 -"))

def bubble(a):
    a = a[:]
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]
    return a
def insertion(a):
    a = a[:]
    for i in range(1, len(a)):
        k, j = a[i], i - 1
        while j >= 0 and a[j] > k: a[j + 1] = a[j]; j -= 1
        a[j + 1] = k
    return a
def merge_sort(a):
    if len(a) < 2: return a
    l, r = merge_sort(a[:len(a)//2]), merge_sort(a[len(a)//2:]); out = []
    while l and r: out.append(l.pop(0) if l[0] <= r[0] else r.pop(0))
    return out + l + r
def quick(a):
    if len(a) < 2: return a
    p = a[len(a)//2]; return quick([x for x in a if x < p]) + [x for x in a if x == p] + quick([x for x in a if x > p])
def heap_sort(a): h = a[:]; heapq.heapify(h); return [heapq.heappop(h) for _ in range(len(h))]
def binary_search(a, t):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if a[m] == t: return m
        lo, hi = (m + 1, hi) if a[m] < t else (lo, m - 1)
    return -1
random.seed(7); data = random.sample(range(1000), 20)
say("\n== Sorting and searching ==")
for name, fn in [("bubble", bubble), ("insertion", insertion), ("merge", merge_sort), ("quick", quick), ("heap", heap_sort)]: say("%-10s correct: %s" % (name, fn(data) == sorted(data)))
sd = sorted(data); say("Binary search for %d in sorted list: index %d (bisect says %d)" % (sd[7], binary_search(sd, sd[7]), bisect.bisect_left(sd, sd[7])))
sizes = [200, 400, 800, 1600]; times = {k: [] for k in ["bubble", "insertion", "merge", "quick", "heap"]}
for n in sizes:
    arr = random.sample(range(10 * n), n)
    for name, fn in [("bubble", bubble), ("insertion", insertion), ("merge", merge_sort), ("quick", quick), ("heap", heap_sort)]:
        t0 = time.perf_counter(); fn(arr); times[name].append(time.perf_counter() - t0)
say("Time (ms) at n=1600: " + ", ".join("%s %.1f" % (k, v[-1] * 1000) for k, v in times.items()))
plt.figure(figsize=(7, 4.5))
for k, v in times.items(): plt.plot(sizes, [x * 1000 for x in v], "o-", label=k)
plt.xlabel("n"); plt.ylabel("time (ms)"); plt.title("Sorting running time"); plt.legend(); plt.grid(alpha=.4); plt.tight_layout(); plt.savefig(os.path.join(OUT, "sorting_times.png"), dpi=150)

say("\n== Greedy, dynamic programming, backtracking ==")
acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]; sel, end = [], 0
for s, e in sorted(acts, key=lambda x: x[1]):
    if s >= end: sel.append((s, e)); end = e
say("Activity selection picks %d activities: %s" % (len(sel), sel))
items = [(60, 10), (100, 20), (120, 30)]; cap = 50; val = 0
for v, w in sorted(items, key=lambda x: -x[0] / x[1]):
    take = min(w, cap); val += v * take / w; cap -= take
say("Fractional knapsack (capacity 50) = %.1f" % val)
def knap(items, W):
    dp = [0] * (W + 1)
    for v, w in items:
        for c in range(W, w - 1, -1): dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]
say("0/1 knapsack (capacity 50) = %d" % knap(items, 50))
def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)): dp[i+1][j+1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j+1], dp[i+1][j])
    return dp[-1][-1]
say("LCS('AGGTAB','GXTXAYB') = %d" % lcs("AGGTAB", "GXTXAYB"))
def edit(a, b):
    dp = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, len(b) + 1): prev, dp[j] = dp[j], min(dp[j] + 1, dp[j-1] + 1, prev + (a[i-1] != b[j-1]))
    return dp[-1]
say("Edit distance('kitten','sitting') = %d" % edit("kitten", "sitting"))
def queens(n, row=0, cols=()):
    if row == n: return 1
    return sum(queens(n, row + 1, cols + (c,)) for c in range(n) if all(c != k and abs(c - k) != row - r for r, k in enumerate(cols)))
say("N-Queens solutions: " + ", ".join("n=%d: %d" % (n, queens(n)) for n in range(4, 9)))
open(os.path.join(OUT, "dsa_output.txt"), "w").write("\n".join(lines) + "\n")
