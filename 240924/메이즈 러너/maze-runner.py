N, M, K = map(int, input().split())

board = [[0] * (N + 1) for _ in range(N + 1)]
for i in range(1, N + 1):
    row = list(map(int, input().split()))
    for j in range(1, N + 1):
        board[i][j] = row[j - 1]

pos = [tuple(map(int, input().split())) for _ in range(M)]
escaped = [False] * M

door = tuple(map(int, input().split()))

deltas = [
    (-1, 0), (1, 0),
    (0, -1), (0, 1)
]


def in_range(r, c):
    return 1 <= r <= N and 1 <= c <= N


def get_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def main():
    global board, pos, door

    answer = 0

    for k in range(1, K + 1):
        for idx in range(M):
            if not escaped[idx]:
                cur_r, cur_c = pos[idx]

                for d in range(4):
                    next_r, next_c = cur_r + deltas[d][0], cur_c + deltas[d][1]

                    if in_range(next_r, next_c) and board[next_r][next_c] <= 0:
                        if (next_r, next_c) == door:
                            answer += 1
                            escaped[idx] = True
                            break

                        cur_dist = get_dist(door, (cur_r, cur_c))
                        next_dist = get_dist(door, (next_r, next_c))
                        if next_dist < cur_dist:
                            answer += 1
                            pos[idx] = (next_r, next_c)
                            break

        if sum(escaped) == M:
            break

        r1, c1 = door
        targets = []
        for idx in range(M):
            if not escaped[idx]:
                r2, c2 = pos[idx]

                l = max(abs(r1 - r2), abs(c1 - c2))
                r = max(1, max(r1, r2) - l)
                c = max(1, max(c1, c2) - l)

                targets.append((r, c, l))
        targets.sort(key=lambda x: (x[2], x[0], x[1]))
        r, c, l = targets[0]

        submatrix = [[board[i + r][j + c] for j in range (0, l + 1)] for i in range(0, l + 1)]
        submatrix = [[submatrix[l - j][i] for j in range (0, l + 1)] for i in range(0, l + 1)]
        for i in range(0, l + 1):
            for j in range(0, l + 1):
                board[i + r][j + c] = submatrix[i][j] - 1

        for idx in range(M):
            if not escaped[idx]:
                cur_r, cur_c = pos[idx]
                if r <= cur_r <= r + l and c <= cur_c <= c + l:
                    pos[idx] = (cur_c + r - c, -cur_r + r + c + l)

        door = (door[1] + r - c, -door[0] + r + c + l)

    print(answer)
    print(door)


if __name__ == "__main__":
    main()