from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

num_rows, num_cols, num_turns = map(int, input().split())
board = [[0] * (num_cols + 2) for _ in range(num_rows + 2)]

def print_global_vars():
    print("board")
    for i in range(num_rows + 2):
        print(board[i])
    print("-" * 20)


def get_golem_position(r: int, c: int, d: int):
    global num_rows, num_cols, board

    locr, locc, locd = r, c, d

    while True:
        # 1. move south
        if (
                (num_rows + 2) > (locr + 2) and
                1 <= (locc - 1) and
                num_cols >= (locc + 1) and
                not board[locr + 1][locc - 1] and
                not board[locr + 2][locc] and
                not board[locr + 1][locc + 1]
        ):
                locr += 1
        # 2. move west
        elif (
                (num_rows + 2) > (locr + 2) and
                1 <= (locc - 2) and
                num_cols >= (locc - 1) and
                not board[locr - 1][locc - 1] and
                not board[locr][locc - 2] and
                not board[locr + 1][locc - 1] and
                not board[locr + 1][locc - 2] and
                not board[locr + 2][locc - 1]
        ):
                locr += 1
                locc -= 1
                locd = (locd + 3) % 4
        # 3. move east
        elif (
                (num_rows + 2) > (locr + 2) and
                1 <= (locc + 1) and
                num_cols >= (locc + 2) and
                not board[locr - 1][locc + 1] and
                not board[locr][locc + 2] and
                not board[locr + 1][locc + 1] and
                not board[locr + 1][locc + 2] and
                not board[locr + 2][locc + 1]
        ):
                locr += 1
                locc += 1
                locd = (locd + 1) % 4
        # 4. stop
        else:
            break

    return locr, locc, locd


def set_golem_position(r: int, c: int, d: int, t: int):
    global num_rows, num_cols, board

    flag = True

    locr, locc, locd, loct = r, c, d, t
    
    if 2 <= (locr - 1) and (num_rows + 2) > (locr + 1) and 1 <= (locc - 1) and num_cols >= (locc + 1):
        board[locr][locc] = loct

        for di in range(4):
            curr, curc = locr + dr[di], locc + dc[di]
            
            if di == locd:
                board[curr][curc] = -loct
            else:
                board[curr][curc] = loct
    else:
        flag = False

        for i in range(num_rows + 2):
            for j in range(num_cols + 2):
                board[i][j] = 0
    
    return flag


def get_fairy_position(r: int, c: int):
    global num_rows, num_cols, board

    locr, locc = r, c

    q = deque()
    visited = [[False] * (num_cols + 2) for _ in range(num_rows + 3)]

    q.append((locr, locc))
    visited[locr][locc] = True
    val = locr

    while q:
        curr, curc = q.pop()
        curt = board[curr][curc]

        for di in range(4):
            nextr, nextc = curr + dr[di], curc + dc[di]

            if 0 < nextr < (num_rows + 2) and 0 < nextc < (num_cols + 2) and not visited[nextr][nextc]:
                if 0 < curt:
                    if abs(board[nextr][nextc]) == curt:
                        visited[nextr][nextc] = True
                        val = max(val, nextr)
                        q.append((nextr, nextc))
                elif 0 > curt:
                    if board[nextr][nextc]:
                        visited[nextr][nextc] = True
                        val = max(val, nextr)
                        q.append((nextr, nextc))

    return val - 1


answer = 0

for t in range(1, num_turns + 1):
    r = 1
    c, d = map(int, input().split())

    r, c, d = get_golem_position(r, c, d)

    set_golem_position(r, c, d, t)

    if set_golem_position(r, c, d, t):
        answer += get_fairy_position(r, c)

print(answer)