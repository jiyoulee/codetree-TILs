# --- Packages

import heapq

# --- Variables

debug = False

N = 0

judges = []
judges_min_heap = []

domains = {}
waitlist = {}

# --- Functions


def initialize(n, u):
    global N, waitlist, judges, judges_min_heap, domains

    N = n
    judges = [["", -1] for _ in range(N + 1)]
    judges_min_heap = list(range(1, N + 1))

    did, tid = map(lambda x: int(x) if x.isdigit() else x, u.split('/'))
    domains[did] = [False, 0, 0]
    waitlist[did] = [(1, 0, tid)]

    if debug:
        print("100")
        print(judges)
        print(judges_min_heap)
        print(domains)
        print(waitlist)
        print("-" * 100)


def post(t, p, u):
    if debug:
        print("200")

    did, tid = map(lambda x: int(x) if x.isdigit() else x, u.split('/'))

    if did in waitlist:
        for (_, _, cur_tid) in waitlist[did]:
            if cur_tid == tid:
                if debug:
                    print("-" * 100)

                return

    if did not in domains:
        domains[did] = [False, 0, 0]
    if did not in waitlist:
        waitlist[did] = []
    heapq.heappush(waitlist[did], (p, t, tid))

    if debug:
        print(domains)
        print(waitlist)
        print("-" * 100)


def put300(t):
    global judges_min_heap, judges, domains, waitlist
    
    if debug:
        print("300")

    if not judges_min_heap:
        if debug:
            print("-" * 100)
        return

    ret_t, ret_p, ret_did, ret_tid = 1 << 30, 1 << 30, "", -1
    for cur_did in waitlist:
        if domains[cur_did][0]:
            continue

        start, gap = domains[cur_did][1:]
        if t < start + 3 * gap:
            continue

        if waitlist[cur_did]:
            cur_p, cur_t, cur_tid = waitlist[cur_did][0]
            if cur_p < ret_p or (cur_p == ret_p and cur_t < ret_t):
                ret_t, ret_p, ret_did, ret_tid = cur_t, cur_p, cur_did, cur_tid

    if ret_did:
        jid = heapq.heappop(judges_min_heap)
        judges[jid][0], judges[jid][1] = ret_did, ret_tid
        domains[ret_did][0], domains[ret_did][1] = True, t
        heapq.heappop(waitlist[ret_did])

    if debug:
        print(judges)
        print(judges_min_heap)
        print(domains)
        print(waitlist)
        print("-" * 100)
        
        
def put400(t, jid):
    global judges_min_heap, judges, domains

    if debug:
        print("400")

    if not judges[jid][0]:
        print("-" * 100)
        return

    did, tid = judges[jid]
    judges[jid][0], judges[jid][1] = "", -1
    heapq.heappush(judges_min_heap, jid)
    domains[did][0], domains[did][2] = False, t - domains[did][1]

    if debug:
        print(judges)
        print(judges_min_heap)
        print(domains)
        print("-" * 100)
        

def get():
    ret_val = 0

    for did in waitlist:
        ret_val += len(waitlist[did])

    return ret_val

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
        if debug:
            print("500")
        print(answer)
        if debug:
            print("-" * 100)