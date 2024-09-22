from collections import deque

L, N, Q = map(int, input().split())

status_board = [[0] * (L + 1) for _ in range(L + 1)]
for i in range(1, L + 1):
    row = list(map(int, input().split()))
    for j in range(1, L + 1):
        status_board[i][j] = row[j - 1]

knights = [(0, 0, 0, 0, 0)] * (N + 1)
knight_board = [[0] * (L + 1) for _ in range(L + 1)]
for idx in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knights[idx] = (r, c, h, w, k)
    for i in range(r, r + h):
        for j in range(c, c + w):
            knight_board[i][j] = idx
knight_damages = [0] * (N + 1)
knight_alive = [True] * (N + 1)

deltas = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]


def in_range(r, c):
    return 1 <= r <= L and 1 <= c <= L


def is_movable(idx, d):
    visited = [[False] * (L + 1) for _ in range(L + 1)]
    q = deque()
    trace = set()

    r, c, h, w, _ = knights[idx]
    visited[r][c] = True
    q.append((r, c))
    trace.add(idx)

    while q:
        cur_r, cur_c = q.popleft()

        if not in_range(cur_r + deltas[d][0], cur_c + deltas[d][1]) or 2 == status_board[cur_r + deltas[d][0]][cur_c + deltas[d][1]]:
            return False, trace

        for qd in range(4):
            next_r, next_c = cur_r + deltas[qd][0], cur_c + deltas[qd][1]

            if in_range(next_r, next_c) and not visited[next_r][next_c] and 2 > status_board[next_r][next_c]:
                if (
                        knight_board[next_r][next_c] == knight_board[cur_r][cur_c]
                        or (0 < knight_board[next_r][next_c] and qd == d)
                ):
                    visited[next_r][next_c] = True
                    q.append((next_r, next_c))
                    trace.add(knight_board[next_r][next_c])

    return True, trace

for q in range(1, Q + 1):
    idx, d = map(int, input().split())

    if not knight_alive[idx]:
        continue

    flag, trace = is_movable(idx, d)

    if not flag:
        continue

    for tidx in trace:
        r, c, h, w, k = knights[tidx]

        knights[tidx] = (r + deltas[d][0], c + deltas[d][1], h, w, k)
        r, c, _, _, _ = knights[tidx]

        if tidx != idx:
            for i in range(r, r + h):
                for j in range(c, c + w):
                    if 1 == status_board[i][j]:
                        knight_damages[tidx] += 1

            if k <= knight_damages[tidx]:
                knight_alive[tidx] = False

    knight_board = [[0] * (L + 1) for _ in range(L + 1)]
    for idx in range(1, N + 1):
        r, c, h, w, _ = knights[idx]

        if knight_alive[idx]:
            for i in range(r, r + h):
                for j in range(c, c + w):
                    knight_board[i][j] = idx

answer = 0
for idx in range(1, N + 1):
    if knight_alive[idx]:
        answer += knight_damages[idx]
print(answer)