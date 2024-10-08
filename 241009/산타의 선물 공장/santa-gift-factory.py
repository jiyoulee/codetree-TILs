# --- Packages

# --- Variables

debug = False

N, M = 0, 0

items = {}

belts = []
broken = []

# --- Functions


def initialize(n, m, rest):
    global N, M, items, belts, broken

    N, M = n, m

    belts = [None] * (M + 1)
    broken = [0] * (M + 1)

    rest = [tuple([rest[i], rest[i + n]]) for i in range(n)]
    for i in range(n):
        pid, weight = rest[i]
        bid = i * m // n + 1

        items[pid] = {
            "pid": pid,
            "weight": weight,
            "bid": bid,
            "prev": None,
            "next": None
        }

        if not belts[bid]:
            items[pid]["prev"] = items[pid]
            items[pid]["next"] = items[pid]
            belts[bid] = items[pid]
            continue

        cur = belts[bid]["prev"]
        
        cur["next"]["prev"] = items[pid]
        items[pid]["next"] = cur["next"]
        cur["next"] = items[pid]
        items[pid]["prev"] = cur

    if debug:
        print("> 100")
        for pid in items:
            print(items[pid]["pid"], end= " ")
        print("")
        for bid in range(1, M + 1):
            cur = belts[bid]
            print(bid, end=" ")
            while cur["next"] != belts[bid]:
                print(cur["pid"], end=" ")
                cur = cur["next"]
            print(cur["pid"], end=" ")
            print(" ")
        print("-" * 100)


def unload(max_weight):
    global items

    answer = 0

    for bid in range(1, M + 1):
        if broken[bid]:
            continue

        cur = belts[bid]
        belts[bid] = belts[bid]["next"]

        if cur["weight"] <= max_weight:
            answer += cur["weight"]

            cur["prev"]["next"] = cur["next"]
            cur["next"]["prev"] = cur["prev"]
            cur["prev"] = None
            cur["next"] = None
            items.pop(cur["pid"])

    if debug:
        for pid in items:
            print(items[pid]["pid"], end=" ")
        print("")
        for bid in range(1, M + 1):
            cur = belts[bid]
            print(bid, end=" ")
            if cur:
                while cur["next"] != belts[bid]:
                    print(cur["pid"], end=" ")
                    cur = cur["next"]
                print(cur["pid"], end=" ")
            print(" ")

    return answer


def delete(pid):
    global items

    answer = -1

    if pid in items:
        answer = pid

        cur = items[pid]
        cur["prev"]["next"] = cur["next"]
        cur["next"]["prev"] = cur["prev"]
        cur["prev"] = None
        cur["next"] = None
        items.pop(cur["pid"])

    if debug:
        for pid in items:
            print(items[pid]["pid"], end=" ")
        print("")
        for bid in range(1, M + 1):
            cur = belts[bid]
            print(bid, end=" ")
            if cur:
                while cur["next"] != belts[bid]:
                    print(cur["pid"], end=" ")
                    cur = cur["next"]
                print(cur["pid"], end=" ")
            print(" ")

    return answer


def get(pid):
    global items

    answer = -1

    if pid in items:
        bid = items[pid]["bid"]
        while broken[bid]:
            bid = broken[bid]
        answer = bid
        belts[bid] = items[pid]

    if debug:
        for pid in items:
            print(items[pid]["pid"], end=" ")
        print("")
        for bid in range(1, M + 1):
            cur = belts[bid]
            print(bid, end=" ")
            if cur:
                while cur["next"] != belts[bid]:
                    print(cur["pid"], end=" ")
                    cur = cur["next"]
                print(cur["pid"], end=" ")
            print(" ")

    return answer


def crash(bid):
    global broken

    answer = -1

    if not broken[bid]:
        answer = bid

        new_bid = 0
        for cur_bid in range(bid + 1, M + 1):
            if not broken[cur_bid]:
                new_bid = cur_bid
                break
        if not new_bid:
            for cur_bid in range(1, bid):
                if not broken[cur_bid]:
                    new_bid = cur_bid
                    break

        broken[bid] = new_bid

        cur = belts[bid]
        belts[bid] = None

        belts[new_bid]["prev"]["next"] = cur
        cur["prev"]["next"] = belts[new_bid]
        belts[new_bid]["prev"] = cur["prev"]
        cur["prev"] = belts[new_bid]["prev"]

    if debug:
        for pid in items:
            print(items[pid]["pid"], end=" ")
        print("")
        for bid in range(1, M + 1):
            cur = belts[bid]
            print(bid, end=" ")
            if cur:
                while cur["next"] != belts[bid]:
                    print(cur["pid"], end=" ")
                    cur = cur["next"]
                print(cur["pid"], end=" ")
            print(" ")

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
        bid = rest[0]
        answer = crash(bid)
        if debug:
            print("> 500")
        print(answer)
        if debug:
            print("-" * 100)