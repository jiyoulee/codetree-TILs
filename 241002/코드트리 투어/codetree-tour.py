# --- Libraries

import heapq

# --- Variables

debug = False

MAX_N, MAX_M, MAX_INT = 2000, 10000, 1 << 30

N, M = 0, 0
graph = [[] for _ in range(MAX_N)]
costs = [MAX_INT] * MAX_N
snode = 0

items = {}
min_heap = []

# --- Functions

def dijkstra():
    global costs

    costs = [MAX_INT] * MAX_N
    heap = []

    costs[snode] = 0
    heapq.heappush(heap, (0, snode))

    while heap:
        cost, u = heapq.heappop(heap)

        if cost > costs[u]:
            continue

        for (v, w) in graph[u]:
            if costs[v] > cost + w:
                costs[v] = cost + w
                heapq.heappush(heap, (costs[v], v))

    if debug:
        print(costs[:N])

def initialize_heap():
    global min_heap

    min_heap = []

    for id in items:
        revenue, dnode, is_valid = items[id]

        if is_valid and revenue >= costs[dnode]:
            heapq.heappush(min_heap, (-(revenue - costs[dnode]), id))

    if debug:
        for e in min_heap:
            print(e)

def initialize(n, m, edges):
    global N, M, graph

    N, M = n, m

    tmp = {}
    for (u, v, w) in [edges[i:i+3] for i in range(0, len(edges), 3)]:
        key = (min(u, v), max(u, v))
        if u != v and (key not in tmp or w < tmp[key][2]):
            tmp[key] = (u, v, w)
    filtered_edges = list(tmp.values())
    for (u, v, w) in filtered_edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    dijkstra()

    if debug:
        print(f"100")
        for i in range(N):
            print(graph[i])
        print("-" * 100)


def post(id, revenue, dnode):
    global items

    items[id] = [revenue, dnode, True]
    if revenue >= costs[dnode]:
        heapq.heappush(min_heap, (-(revenue - costs[dnode]), id))

    if debug:
        print(f"200")
        for id in items:
            print(id, items[id])
        for e in min_heap:
            print(e)
        print("-" * 100)


def delete(id):
    global items

    if id in items:
        items[id][2] = False

    if debug:
        print(f"300")
        for id in items:
            print(id, items[id])
        print("-" * 100)


def get():
    while min_heap:
        profit, id = heapq.heappop(min_heap)
        if items[id][2]:
            items[id][2] = False
            return id
    return -1


def put(node):
    global snode

    snode = node
    dijkstra()
    initialize_heap()

    if debug:
        print("500")
        print(snode)
        print("-" * 100)


# --- Main Logic

Q = int(input().split()[0])

for _ in range(Q):
    command, *rest = list(map(int, input().split()))

    if 100 == command:
        n, m, *edges = rest
        initialize(n, m, edges)
    elif 200 == command:
        id, revenue, node = rest
        post(id, revenue, node)
    elif 300 == command:
        id = rest[0]
        delete(id)
    elif 400 == command:
        answer = get()
        # print("400")
        print(answer)
        # print("-" * 100)
    elif 500 == command:
        node = rest[0]
        put(node)