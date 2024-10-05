# --- Packages

import heapq

# --- Variables

debug = False

N = 0

judges = []
judges_min_heap = []

domains = {}

q = {}

# --- Functions


def initialize(n, u):
    global N, q, judges, judges_min_heap, domains

    N = n
    judges = [["", -1] for _ in range(N + 1)]
    judges_min_heap = list(range(1, N + 1))

    did, tid = map(lambda x: int(x) if x.isdigit() else x, u.split('/'))
    domains[did] = [False, 0, 0]
    q[(did, tid)] = (0, 1)


def post(t, p, u):
    did, tid = map(lambda x: int(x) if x.isdigit() else x, u.split('/'))

    if (did, tid) in q:
        return

    if did not in domains:
        domains[did] = [False, 0, 0]
    q[(did, tid)] = (t, p)


def put300(t):
    global judges_min_heap, judges, domains, q

    if not judges_min_heap:
        return

    ret_t, ret_p, ret_did, ret_tid = 1 << 30, 1 << 30, "", -1
    for (did, tid) in q:
        if domains[did][0]:
            continue

        start, gap = domains[did][1:]
        if t < start + 3 * gap:
            continue

        cur_t, cur_p = q[(did, tid)]
        if cur_p < ret_p or (cur_p == ret_p and cur_t < ret_t):
            ret_t, ret_p, ret_did, ret_tid = cur_t, cur_p, did, tid

    if ret_did:
        jid = heapq.heappop(judges_min_heap)
        judges[jid][0], judges[jid][1] = ret_did, ret_tid
        domains[ret_did][0], domains[ret_did][1] = True, t
        q.pop((ret_did, ret_tid))
        
        
def put400(t, jid):
    global judges_min_heap, judges, domains\

    if not judges[jid][0]:
        return

    did, tid = judges[jid]
    judges[jid][0], judges[jid][1] = "", -1
    heapq.heappush(judges_min_heap, jid)
    domains[did][0], domains[did][2] = False, t - domains[did][1]
        

def get():
    return len(q)

# --- Main Logic

Q = int(input().split()[0])

for _ in range(Q):
    command, *rest = map(lambda x: int(x) if x.isdigit() else x, input().split())

    if 100 == command:
        n, u = rest
        initialize(n, u)
    elif 200 == command:
        t, p, u = rest
        post(t, p, u)
    elif 300 == command:
        t = rest[0]
        put300(t)
    elif 400 == command:
        t, jid = rest
        put400(t, jid)
    elif 500 == command:
        answer = get()
        print(answer)