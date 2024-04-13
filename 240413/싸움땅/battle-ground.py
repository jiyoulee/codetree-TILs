import sys
import heapq

# sys.stdin = open("input.txt", "r")

# 1. 정의
verbose = False
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

# 2. 입력
n, num_players, num_rounds = map(int, input().split())
guns_board = [[0] * (n + 1)] + [[[0]] + [[x] for x in list(map(lambda x: -x, map(int, input().split())))] for _ in range(n)]
for r in range(1, n + 1):
    for c in range(1, n + 1):
        if [0] == guns_board[r][c]:
            guns_board[r][c] = []
        else:
            heapq.heapify(guns_board[r][c])
players = [[0] * 5] + [list(map(int, input().split())) + [0] for _ in range(num_players)]
players_board = [[0] * (n + 1) for _ in range(n + 1)]
for index, player in enumerate(players):
    players_board[player[0]][player[1]] = index
answer = [0 for _ in range(num_players + 1)]


def in_range(x):
    return (0 < x[0] <= n) and (0 < x[1] <= n)


def max_heappush(heap, item):
    heapq.heappush(heap, -item)
    return


def max_heappop(heap):
    return -heapq.heappop(heap)


def max_heaptop(heap):
    return -heap[0]


for rid in range(1, num_rounds + 1):
    if verbose:
        print(f"Info: round #{rid}.")
        for row in guns_board:
            print(row)
        print(f"-")
        for row in players_board:
            print(row)
        print(f"-")

    for pid in range(1, num_players + 1):
        if verbose:
            print(f"Info: {pid}")

        # 1. 플레이어 이동
        d = players[pid][2]
        nr, nc = players[pid][0] + dr[d], players[pid][1] + dc[d]
        if not in_range([nr, nc]):
            d = ((d + 2) % 4)
            players[pid][2] = d
            nr, nc = players[pid][0] + dr[d], players[pid][1] + dc[d]
        players_board[players[pid][0]][players[pid][1]] = 0
        players[pid][0] += dr[d]
        players[pid][1] += dc[d]

        sr, sc = players[pid][:2]
        # 2-1. 플레이어 총기 갱신
        if not players_board[sr][sc]:
            players_board[sr][sc] = pid
            if guns_board[sr][sc] and max_heaptop(guns_board[sr][sc]) > players[pid][4]:
                max_heappush(guns_board[sr][sc], players[pid][4])
                players[pid][4] = max_heappop(guns_board[sr][sc])
        # 2-2. 플레이어 배틀
        else:
            npid = players_board[sr][sc]

            wpid, lpid = 0, 0
            if sum(players[pid][3:5]) > sum(players[npid][3:5]):
                wpid, lpid = pid, npid
            elif sum(players[pid][3:5]) == sum(players[npid][3:5]) and players[pid][3] > players[npid][3]:
                wpid, lpid = pid, npid
            else:
                wpid, lpid = npid, pid

            if verbose:
                print(wpid, lpid)

            # 2-2-1. 승자 상태 갱신 (1)
            answer[wpid] += abs(sum(players[pid][3:5]) - sum(players[npid][3:5]))
            players_board[sr][sc] = wpid

            # 2-2-2. 패자 상태 갱신
            if players[lpid][4]:
                max_heappush(guns_board[sr][sc], players[lpid][4])
                players[lpid][4] = 0

            d = players[lpid][2]
            for dd in range(4):
                npr, npc = players[lpid][0] + dr[(d + dd) % 4], players[lpid][1] + dc[(d + dd) % 4]
                if in_range([npr, npc]) and not players_board[npr][npc]:
                    players[lpid][0] = npr
                    players[lpid][1] = npc
                    players[lpid][2] = (d + dd) % 4
                    players_board[npr][npc] = lpid
                    if guns_board[npr][npc] and max_heaptop(guns_board[npr][npc]) > players[lpid][4]:
                        max_heappush(guns_board[npr][npc], players[lpid][4])
                        players[lpid][4] = max_heappop(guns_board[npr][npc])
                    break

            # 2-2-3. 승자 상태 갱신 (2)
            if guns_board[sr][sc] and max_heaptop(guns_board[sr][sc]) > players[wpid][4]:
                max_heappush(guns_board[sr][sc], players[wpid][4])
                players[wpid][4] = max_heappop(guns_board[sr][sc])

        if verbose:
            for row in guns_board:
                print(row)
            print(f"-")
            for row in players_board:
                print(row)
            print(f"-")
            for row in players:
                print(players)

if verbose:
    print(f"Info: final result.")
    for row in guns_board:
        print(row)
    print(f"-")
    for row in players_board:
        print(row)
    print(f"-")
    for row in players:
        print(players)

for score in answer[1:]:
    print(f"{score} ", end="")