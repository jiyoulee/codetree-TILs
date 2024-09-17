from collections import deque

N = 5
K, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
wall = deque(map(int, input().split()))
deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def in_range(r, c):
    return 0 <= r < 5 and 0 <= c < 5


def get_rotated_board(r, c, d):
    result_board = [[board[i][j] for j in range(5)] for i in range(5)]
    submatrix = [[board[i][j] for j in range(c, c + 3)] for i in range(r, r + 3)]

    for _ in range(d):
        submatrix = [[submatrix[2 - j][i] for j in range(0, 3)] for i in range(0, 3)]

    for i in range(0, 3):
        for j in range(0, 3):
            result_board[i + r][j + c] = submatrix[i][j]

    return result_board


def get_submatrix_trace(r, c):
    result_trace = [(r + 1, c + 1)]

    for td in range(8):
        pos_r, pos_c = r + 1 + deltas[td][0], c + 1 + deltas[td][1]
        if in_range(pos_r, pos_c):
            result_trace.append((pos_r, pos_c))

    return result_trace


def get_pos_list(board, trace):
    result_trace = []

    visited = [[False] * 5 for _ in range(5)]
    q = deque()

    for r, c in trace:
            if not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
                tmp_trace = [(r, c)]

                while q:
                    cur_r, cur_c = q.popleft()
                    for d in range(4):
                        next_r, next_c = cur_r + deltas[d][0], cur_c + deltas[d][1]
                        if (in_range(next_r, next_c)
                                and not visited[next_r][next_c]
                                and board[next_r][next_c] == board[r][c]):
                            visited[next_r][next_c] = True
                            q.append((next_r, next_c))
                            tmp_trace.append((next_r, next_c))

                if 3 <= len(tmp_trace):
                    result_trace.extend(tmp_trace)

    return result_trace


def main():
    global board

    for k in range(1, K + 1):
        answer = 0

        submatrix_list = []

        for r in range(0, 3):
            for c in range(0, 3):
                for d in range(1, 4):
                    rotated_board = get_rotated_board(r, c, d)

                    trace = get_submatrix_trace(r, c)
                    new_trace = get_pos_list(rotated_board, trace)

                    value = len(new_trace)
                    submatrix_list.append((value, d, c, r))

        submatrix_list.sort(key=lambda x: (-x[0], x[1], x[2], x[3]))
        sub_value, sub_d, sub_c, sub_r = submatrix_list[0]

        if not sub_value:
            break

        board = get_rotated_board(sub_r, sub_c, sub_d)
        trace = get_submatrix_trace(sub_r, sub_c)

        while True:
            new_trace = get_pos_list(board, trace)

            if not new_trace:
                break

            answer += len(new_trace)

            new_trace.sort(key=lambda x: (x[1], -x[0]))
            for r, c in new_trace:
                board[r][c] = wall.popleft()

            trace = new_trace

        print(answer, end=" ")

if __name__ == "__main__":
    main()