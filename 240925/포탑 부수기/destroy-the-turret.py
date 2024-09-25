# ----- Packages

from collections import deque

# ----- Global Variables

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

timing = [[0] * M for _ in range(N)]
deltas = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1)
]

# ----- Functions

# ----- Main

for k in range(1, K + 1):
    cnt = 0
    for i in range(N):
        for j in range(M):
            if 0 < board[i][j]:
                cnt += 1

    if 1 >= cnt:
        break

    targets = []
    for i in range(N):
        for j in range(M):
            if 0 < board[i][j]:
                targets.append((i, j, board[i][j], timing[i][j]))
    targets.sort(key=lambda x: (x[2], -x[3], -(x[0] + x[1]), -x[1]))

    r1, c1 = targets[0][:2]
    board[r1][c1] += N + M
    timing[r1][c1] = k

    r2, c2 = targets[-1][:2]

    dir_trace = []
    visited = [[False] * M for _ in range(N)]
    visited[r1][c1] = True
    q = deque()
    q.append((r1, c1, []))
    while q:
        cur_r, cur_c, cur_dir_trace = q.popleft()

        if cur_r == r2 and cur_c == c2:
            dir_trace = cur_dir_trace
            break

        for d in range(4):
            next_r, next_c = (cur_r + deltas[d][0]) % N, (cur_c + deltas[d][1]) % M

            if 0 < board[next_r][next_c] and not visited[next_r][next_c]:
                visited[next_r][next_c] = True
                q.append((next_r, next_c, cur_dir_trace + [d]))

    processed = [[False] * M for _ in range(N)]
    if dir_trace:
        processed[r1][c1] = True
        cur_r, cur_c = r1, c1
        for d in dir_trace:
            next_r, next_c = (cur_r + deltas[d][0]) % N, (cur_c + deltas[d][1]) % M
            processed[next_r][next_c] = True
            board[next_r][next_c] -= board[r1][c1] if (next_r == r2 and next_c == c2) else (board[r1][c1] // 2)
            cur_r, cur_c = next_r, next_c
    else:
        processed[r1][c1] = True
        processed[r2][c2] = True
        board[r2][c2] -= board[r1][c1]
        for d in range(8):
            cur_r, cur_c = (r2 + deltas[d][0]) % N, (c2 + deltas[d][1]) % M
            if cur_r != r1 and cur_c != c1:
                processed[cur_r][cur_c] = True
                board[cur_r][cur_c] -= board[r1][c1] // 2

    for i in range(N):
        for j in range(M):
            if 0 < board[i][j] and not processed[i][j]:
                board[i][j] += 1

answer = 1
for i in range(N):
    for j in range(M):
        if answer < board[i][j]:
            answer = board[i][j]
print(answer)