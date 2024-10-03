# --- Libraries

import heapq

# --- Variables

debug = False

N, M, P = 0, 0, 0

dists = {}
base = 0
points = {}
min_heap = []

deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# --- Functions

def initialize(n, m, p, rabbits):
    global N, M, P, dists, min_heap

    N, M, P = n, m, p

    rabbits = [tuple(rabbits[i:i+2]) for i in range(0, len(rabbits), 2)]
    for (pid, dist) in rabbits:
        dists[pid] = dist
        points[pid] = 0
        heapq.heappush(min_heap, (0, 2, 1, 1, pid))

    if debug:
        print("100")
        print(N, M, P)
        for pid in dists:
            print(pid, dists[pid])
        for row in min_heap:
            print(row)
        print("-" * 100)


def post(k, s):
    global min_heap, base, points

    if debug: print("400")

    targets = []

    for _ in range(k):
        t, _, r, c, pid = heapq.heappop(min_heap)

        target_dist = []
        for d in range(4):
            dist, nr, nc = dists[pid], 0, 0

            if d < 2:
                m = N - 1
                dist += (r - 1) if 1 == d else -(r - 1)
                u, v = dist // m, dist % m
                (nr, nc) = (1 + v, c) if 0 == u % 2 else (N - v, c)
            else:
                n = M - 1
                dist += (c - 1) if 3 == d else -(c - 1)
                u, v = dist // n, dist % n
                (nr, nc) = (r, 1 + v) if 0 == u % 2 else (r, M - v)

            if debug: print(f"{d}: ({nr}, {nc})")
            target_dist.append((nr, nc))
        target_dist.sort(key=lambda x: (-(x[0] + x[1]), -x[0], -x[1]))

        (r, c) = target_dist[0]
        heapq.heappush(min_heap, (t + 1, r + c, r, c, pid))
        targets.append((r, c, pid))

        base += r + c
        points[pid] -= r + c

        if debug:
            for row in min_heap:
                print(row)

    targets.sort(key=lambda x: (-(x[0] + x[1]), -x[0], -x[1], -x[2]))
    points[targets[0][2]] += s

    if debug:
        print("-" * 100)


def put(pid, l):
    global dists

    dists[pid] *= l

    if debug:
        print("300")
        for pid in dists:
            print(pid, dists[pid])
        print("-" * 100)


def get():
    return base + max(points.values())

# --- Main Logic

Q = int(input().split()[0])

for _ in range(Q):
    command, *rest = map(int, input().split())

    if 100 == command:
        n, m, p, *rest = rest
        initialize(n, m, p, rest)
    elif 200 == command:
        k, s = rest
        post(k, s)
    elif 300 == command:
        pid, l = rest
        put(pid, l)
    elif 400 == command:
        answer = get()
        if debug:
            print("400")
        print(answer)
        if debug:
            print("-" * 100)