from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
de = [
        [(0, -2), (-1, -1), (-2, 0), (-1, 1), (0, 2)],
        [(-2, 0), (-1, 1), (0, 2), (1, 1), (2, 0)],
        [(0, -2), (1, -1), (2, 0), (1, 1), (0, 2)],
        [(-2, 0), (-1, -1), (0, -2), (1, -1), (2, 0)]
     ]

num_rows, num_cols, num_turns = map(int, input().split())
board = [[0] * (num_cols + 2) for _ in range(num_rows + 3)]

def print_global_vars():
    print("board")
    for i in range(num_rows + 3):
        str = ""
        for j in range(num_cols + 2):
            str = " ".join([str, f"{board[i][j]:10}"])
        print(str)
    print("-" * 20)


def get_golem_position(ar: int, ac: int, ad: int):
    global num_rows, num_cols, board

    r, c, d = ar, ac, ad

    while True:
        print(r, c, d)
        # 1. move south
        if (
                num_rows + 2 >= (r + 2) and
                1 <= (c - 1) and
                num_cols >= (c + 1) and
                not board[r + 1][c - 1] and
                not board[r + 2][c] and
                not board[r + 1][c + 1]
        ):
                r += 1
        # 2. move west
        elif (
                num_rows + 2 >= (r + 2) and
                1 <= (c - 2) and
                not board[r - 1][c - 1] and
                not board[r][c - 2] and
                not board[r + 1][c - 1] and
                not board[r + 1][c - 2] and
                not board[r + 2][c - 1]
        ):
                r += 1
                c -= 1
                d = (d + 3) % 4
        # 3. move east
        elif (
                num_rows + 2 >= (r + 2) and
                num_cols >= (c + 2) and
                not board[r - 1][c + 1] and
                not board[r][c + 2] and
                not board[r + 1][c + 1] and
                not board[r + 1][c + 2] and
                not board[r + 2][c + 1]
        ):
                r += 1
                c += 1
                d = (d + 1) % 4
        # 4. stop
        else:
            print("stop")
            break

    return r, c, d


def set_golem_position(ar: int, ac: int, ad: int, at: int):
    global num_rows, num_cols, board

    flag = True

    r, c, d, t = ar, ac, ad, at

    if 3 <= (r - 1) and num_rows + 2 >= (r + 1) and 1 <= (c - 1) and num_cols >= (c + 1):
        board[r][c] = t

        for dd in range(4):
            cr, cc = r + dr[dd], c + dc[dd]

            if dd == d:
                board[cr][cc] = -t
            else:
                board[cr][cc] = t
    else:
        flag = False

        for i in range(num_rows + 3):
            for j in range(num_cols + 2):
                board[i][j] = 0

    return flag


def get_fairy_position(ar: int, ac: int):
    global num_rows, num_cols, board

    r, c = ar, ac

    q = deque()
    visited = [[False] * (num_cols + 2) for _ in range(num_rows + 3)]

    q.append((r, c))
    visited[r][c] = True
    val = r

    while q:
        cr, cc = q.pop()

        # 1. get exit coordinates
        er, ec, ed = 0, 0, 0

        for dd in range(4):
            nr, nc = cr + dr[dd], cc + dc[dd]

            if 3 <= nr <= num_rows + 2 and 1 <= nc <= num_cols and 0 > board[nr][nc]:
                er, ec, ed = nr, nc, dd
                break

        # 2. get next golem coordinates
        for dd in range(5):
            nr, nc = er + de[ed][dd][0], ec + de[ed][dd][1]

            if 3 <= nr <= num_rows + 2 and 1 <= nc <= num_cols and not visited[nr][nc] and board[nr][nc]:
                flag = True

                for ddd in range(4):
                    nnr, nnc = nr + dr[ddd], nc + dc[ddd]

                    if 3 <= nnr <= num_rows + 2 and 1 <= nnc <= num_cols and abs(board[nnr][nnc]) == board[nr][nc]:
                        continue
                    else:
                        flag = False
                        break

                if flag:
                    print (f"-- {nr} {nc} {board[nr][nc]}")
                    visited[nr][nc] = True
                    val = max(val, nr)
                    q.append((nr, nc))

    return val - 1


answer = 0

for t in range(1, num_turns + 1):
    r = 1
    c, d = map(int, input().split())

    r, c, d = get_golem_position(r, c, d)

    if set_golem_position(r, c, d, t):
        answer += get_fairy_position(r, c)

print(answer)