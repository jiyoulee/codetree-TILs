# --- Libraries

# --- Variables

N, M, K, C = map(int, input().split())

board = [[-1] * (N + 2) for _ in range(N + 2)]
for i in range(1, N + 1):
    row = list(map(int, input().split()))
    for j in range(1, N + 1):
        board[i][j] = row[j - 1]

pesticides = [[0] * (N + 1) for _ in range(N + 1)]

deltas1 = [(-1, 0), (1,0), (0, -1), (0, 1)]
deltas2 = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

# --- Functions

def in_range(r: int, c: int):
    return 1 <= r <= N and 1 <= c <= N

# --- Main Logic

answer = 0

for m in range(1, M + 1):
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if board[i][j] > 0:
                for d in range(4):
                    if board[i + deltas1[d][0]][j + deltas1[d][1]] > 0:
                        board[i][j] += 1

    growth = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if board[i][j] > 0:
                cnt = 0
                for d in range(4):
                    ni, nj = i + deltas1[d][0], j + deltas1[d][1]
                    if board[ni][nj] == 0 and pesticides[ni][nj] < m:
                        cnt += 1

                for d in range(4):
                    ni, nj = i + deltas1[d][0], j + deltas1[d][1]
                    if board[ni][nj] == 0 and pesticides[ni][nj] < m:
                        growth[ni][nj] += board[i][j] // cnt
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            board[i][j] += growth[i][j]

    max_points, r, c = -1, 0, 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if board[i][j] >= 0:
                points = board[i][j]
                if board[i][j] > 0:
                    for d in range(4):
                        for k in range(1, K + 1):
                            ni, nj = i + k * deltas2[d][0], j + k * deltas2[d][1]
                            if board[ni][nj] <= 0:
                                break
                            points += board[ni][nj]

                if max_points < points:
                    max_points, r, c = points, i, j

    answer += max_points

    if board[r][c] > 0:
        for d in range(4):
            for k in range(1, K + 1):
                ni, nj = r + k * deltas2[d][0], c + k * deltas2[d][1]
                if board[ni][nj] < 0:
                    break
                pesticides[ni][nj] = m + C
                if board[ni][nj] == 0:
                    break
                board[ni][nj] = 0
    pesticides[r][c] = m + C
    board[r][c] = 0

print(answer)