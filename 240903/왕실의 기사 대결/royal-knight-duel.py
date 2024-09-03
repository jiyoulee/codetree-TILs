from collections import deque

L, N, Q = map(int, input().split())

board = [[2] * (L + 2) for _ in range(L + 2)]
for i in range(1, L + 1):
    row = list(map(int, input().split()))
    for j in range(1, L + 1):
        board[i][j] = row[j - 1]

d4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
damages = [0] * (N + 1)
knights = [tuple()] * (N + 1)
boardN = [[0] * (L + 2) for _ in range(L + 2)]
for idx in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knights[idx] = (r, c, h, w, k)
    for i in range(r, r + h):
        for j in range(c, c + w):
            boardN[i][j] = idx


def in_range(R: int, C: int):
    global N
    return 1 <= R <= N and 1 <= C <= N


def get_trace(idx: int, d: int):
    global L, knights, boardN, board

    r, c, h, w, k = knights[idx]

    visited = [[False] * (L + 2) for _ in range(L + 2)]
    q = deque()
    trace = []

    visited[r][c] = True
    q.append((r, c))
    trace.append((r, c, boardN[r][c]))

    while q:
        curR, curC = q.popleft()

        for curD in range(4):
            nextR, nextC = curR + d4[curD][0], curC + d4[curD][1]

            if all([
                in_range(nextR, nextC) and not visited[nextR][nextC] and
                (boardN[nextR][nextC] == boardN[curR][curC] or (boardN[nextR][nextC] and curD == d))
            ]):
                visited[nextR][nextC] = True
                q.append((nextR, nextC))
                trace.append((nextR, nextC, boardN[nextR][nextC]))

    for t in range(len(trace)):
        curR, curC, _ = trace[t]
        nextR, nextC = curR + d4[d][0], curC + d4[d][1]

        if board[nextR][nextC] == 2:
            return []

    return sorted(trace, key=lambda x: x[2])


def main():
    global Q, knights, damages, L, boardN, board

    answer = 0

    for q in range(1, Q + 1):
        idx, d = map(int, input().split())
        r, c, h, w, k = knights[idx]

        if damages[idx] >= k:
            continue

        trace = get_trace(idx, d)
        if not trace:
            continue

        i = 0
        while i < len(trace):
            _, _, idxP = trace[i]
            rP, cP, hP, wP, kP = knights[idxP]

            while i < len(trace) and trace[i][2] == idxP:
                if idxP != idx:
                    rT, cT, _ = trace[i]
                    if board[rT + d4[d][0]][cT + d4[d][1]] == 1:
                        damages[idxP] += 1
                i += 1

            knights[idxP] = (rP + d4[d][0], cP + d4[d][1], hP, wP, kP)

        boardN = [[0] * (L + 2) for _ in range(L + 2)]
        for i in range(1, N + 1):
            if damages[i] < knights[i][4]:
                rP, cP, hP, wP, kP = knights[i]

                for R in range(rP, rP + hP):
                    for C in range(cP, cP + wP):
                        boardN[R][C] = i

    for idx in range(1, N + 1):
        if damages[idx] < knights[idx][4]:
            answer += damages[idx]

    print(answer)

if __name__ == "__main__":
    main()