from collections import deque

R, C, K = map(int, input().split())
board = [[0] * (1 + C) for _ in range(3 + R)]
golem_list = [(-1, -1)] + [tuple(map(int, input().split())) for _ in range(K)]
deltas = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]


def in_range(r):
    return 4 <= r <= R + 1


def move_kth_golem(r, c, d, k):
    result_board = [[board[i][j] for j in range(1 + C)] for i in range(3 + R)]

    result_r, result_c, result_d = r, c, d

    while result_r <= R:
        if (
                not board[result_r + 1][result_c - 1]
                and not board[result_r + 2][result_c]
                and not board[result_r + 1][result_c + 1]
        ):
            result_r += 1
        elif (
                3 <= result_c
                and not board[result_r - 1][result_c -1]
                and not board[result_r][result_c - 2]
                and not board[result_r + 1][result_c - 1]
                and not board[result_r + 1][result_c - 2]
                and not board[result_r + 2][result_c - 1]
        ):
            result_r += 1
            result_c -= 1
            result_d = (result_d + 3) % 4
        elif (
                C - 2 >= result_c
                and not board[result_r - 1][result_c + 1]
                and not board[result_r][result_c + 2]
                and not board[result_r + 1][result_c + 1]
                and not board[result_r + 1][result_c + 2]
                and not board[result_r + 2][result_c + 1]
        ):
            result_r += 1
            result_c += 1
            result_d = (result_d + 1) % 4
        else:
            break

    if in_range(result_r):
        for rd in range(5):
            result_board[result_r + deltas[rd][0]][result_c + deltas[rd][1]] = -k if rd == result_d else k
    else:
        for i in range(3 + R):
            for j in range(1 + C):
                result_board[i][j] = 0

    return result_r, result_c, result_board


def move_kth_fairy(r, c):
    result_r = -1

    visited = [[False] * (C + 1) for _ in range(R + 3)]
    q = deque()

    visited[r][c] = True
    q.append((r, c))

    while q:
        cur_r, cur_c = q.popleft()

        result_r = max(result_r, cur_r)

        for d in range(4):
            next_r, next_c = cur_r + deltas[d][0], cur_c + deltas[d][1]

            if 3 <= next_r <= R + 2 and 1 <= next_c <= C and not visited[next_r][next_c]:
                visited[next_r][next_c] = True

                if (
                        (board[cur_r][cur_c] > 0 and abs(board[next_r][next_c]) == board[cur_r][cur_c])
                        or (board[cur_r][cur_c] < 0 and board[next_r][next_c] != 0)
                ):
                    q.append((next_r, next_c))

    return result_r - 2

def main():
    global board

    answer = 0

    for k in range(1, K + 1):
        init_r, init_c, init_d = 1, golem_list[k][0], golem_list[k][1]

        r, c, board = move_kth_golem(init_r, init_c, init_d, k)

        if in_range(r):
            answer += move_kth_fairy(r, c)

    print(answer)

if __name__ == "__main__":
    main()