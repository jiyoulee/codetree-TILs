# --- Packages

# --- Variables

debug = False

N, M = 0, 0

items = {}

heads = []
broken = []

# --- Functions


def printg():
    for pid in items:
        print(items[pid]["pid"], end=" ")
    print("")
    for hid in range(1, M + 1):
        print(hid, end=" ")
        if not broken[hid] and heads[hid]:
            cur = heads[hid]
            while cur["next"] != heads[hid]:
                print(f"cur: {cur['pid']}, prev: {cur['prev']['pid']}, next: {cur['next']['pid']}")
                cur = cur["next"]
            print(f"cur: {cur['pid']}, prev: {cur['prev']['pid']}, next: {cur['next']['pid']}")
        print(" ")


def initialize(n, m, rest):
    global N, M, items, heads, broken

    N, M = n, m

    heads = [None] * (M + 1)
    broken = [0] * (M + 1)

    rest = [tuple([rest[i], rest[i + n]]) for i in range(n)]
    for i in range(n):
        pid, weight = rest[i]
        hid = i * m // n + 1

        items[pid] = {
            "pid": pid,
            "weight": weight,
            "hid": hid,
            "prev": None,
            "next": None
        }

        if not heads[hid]:
            items[pid]["prev"] = items[pid]
            items[pid]["next"] = items[pid]
            heads[hid] = items[pid]
        else:
            cur = heads[hid]["prev"]
            cur["next"]["prev"] = items[pid]
            items[pid]["next"] = cur["next"]
            cur["next"] = items[pid]
            items[pid]["prev"] = cur

    if debug:
        print("> 100")
        printg()
        print("-" * 100)


def unload(max_weight):
    global items, heads

    answer = 0

    for hid in range(1, M + 1):
        if broken[hid] or not heads[hid]:
            continue

        cur = heads[hid]
        heads[hid] = None if cur == cur["next"] else heads[hid]["next"]

        if cur["weight"] <= max_weight:
            answer += cur["weight"]

            cur["prev"]["next"] = cur["next"]
            cur["next"]["prev"] = cur["prev"]
            cur["prev"] = None
            cur["next"] = None
            items.pop(cur["pid"])

    if debug:
        printg()

    return answer


def delete(pid):
    global items, heads

    answer = -1

    if pid in items:
        answer = pid

        cur = items[pid]
        hid = items[pid]["hid"]
        while broken[hid]:
            hid = broken[hid]
        if cur == heads[hid]:
            heads[hid] = None if cur == cur["next"] else heads[hid]["next"]

        cur["prev"]["next"] = cur["next"]
        cur["next"]["prev"] = cur["prev"]
        cur["prev"] = None
        cur["next"] = None
        items.pop(cur["pid"])

    if debug:
        printg()

    return answer


def get(pid):
    global items, heads

    answer = -1

    if pid in items:
        hid = items[pid]["hid"]
        while broken[hid]:
            hid = broken[hid]
        answer = hid
        heads[hid] = items[pid]

    if debug:
        printg()

    return answer


def crash(hid):
    global broken, heads

    answer = -1

    if not broken[hid]:
        answer = hid

        new_hid = 0
        for cur_bid in range(hid + 1, M + 1):
            if not broken[cur_bid]:
                new_hid = cur_bid
                break
        if not new_hid:
            for cur_bid in range(1, hid):
                if not broken[cur_bid]:
                    new_hid = cur_bid
                    break

        broken[hid] = new_hid

        cur = heads[hid]
        heads[hid] = None

        if not heads[new_hid]:
            heads[new_hid] = cur
        else:
            heads[new_hid]["prev"]["next"] = cur
            cur["prev"]["next"] = heads[new_hid]
            heads[new_hid]["prev"] = cur["prev"]
            cur["prev"] = heads[new_hid]["prev"]

    if debug:
        printg()

    return answer


# --- Main Logic

Q = int(input().split()[0])

for _ in range(Q):
    command, *rest = map(int, input().split())

    if 100 == command:
        n, m, *rest = rest
        initialize(n, m, rest)
    elif 200 == command:
        max_weight = rest[0]
        answer = unload(max_weight)
        if debug:
            print("> 200")
        print(answer)
        if debug:
            print("-" * 100)
    elif 300 == command:
        pid = rest[0]
        answer = delete(pid)
        if debug:
            print("> 300")
        print(answer)
        if debug:
            print("-" * 100)
    elif 400 == command:
        pid = rest[0]
        answer = get(pid)
        if debug:
            print("> 400")
        print(answer)
        if debug:
            print("-" * 100)
    elif 500 == command:
        hid = rest[0]
        answer = crash(hid)
        if debug:
            print("> 500")
        print(answer)
        if debug:
            print("-" * 100)