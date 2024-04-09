# 1. 변수 정의
answer = 0
verbose = False
WALL = -1
PERSON = -2
EXIT = -3

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
get_dist = lambda r1, c1, r2, c2: (abs(r1 - r2) + abs(c1 - c2))

# 2. 입력
n, persons_cnt, turns_cnt = list(map(int, input().split()))
is_valid_loc = lambda r1, c1: (1 <= r1 <= n and 1 <= c1 <= n)
board = [[-1 for _ in range(n + 2)] for _ in range(n + 2)]

# 1. 벽
for i in range(1, n + 1):
    board[i] = list(map(int, input().split()))
    board[i].insert(0, WALL)
    board[i].append(WALL)

# 2. 참가자
persons_loc = [[0 for _ in range(2)] for _ in range(persons_cnt + 1)]
persons_state = [1 for _ in range(persons_cnt + 1)]
persons_state[0] = 0
for pid in range(1, persons_cnt + 1):
    persons_loc[pid] = list(map(int, input().split()))
    board[persons_loc[pid][0]][persons_loc[pid][1]] = PERSON

# 3. 출구
exit_loc = list(map(int, input().split()))
board[exit_loc[0]][exit_loc[1]] = EXIT

if verbose:
    print(f"{'-' * 20}")
    for i in range(n + 2):
        for j in range(n + 2):
            print(f"{board[i][j]:3}", end='')
        print('')
    print(f"{'-' * 20}")

# 2. 계산
is_over = False
for turn_id in range(1, turns_cnt + 1):
    if verbose:
        print(f"Info: starting turn #{turn_id}.")
    er, ec = exit_loc

    # 1. 참가자 이동
    for pid in range(1, persons_cnt + 1):
        if persons_state[pid]:
            pr, pc = persons_loc[pid]

            cur_dist = get_dist(er, ec, pr, pc)
            persons_cand = [[pr + dr[i], pc + dc[i], get_dist(er, ec, pr + dr[i], pc + dc[i])] for i in range(4)]
            persons_cand = [cand for cand in persons_cand if cur_dist > cand[2]]
            persons_cand.sort(key=lambda x: x[2])

            for cand in persons_cand:
                if EXIT == board[cand[0]][cand[1]]:
                    board[persons_loc[pid][0]][persons_loc[pid][1]] = 0
                    persons_state[pid] = 0
                    answer += 1
                    if verbose:
                        print(f"Info: person #{pid} has left the maze. remaining persons are {[index for index, value in enumerate(persons_state) if 1 == value]}.")
                elif 0 == board[cand[0]][cand[1]]:
                    board[persons_loc[pid][0]][persons_loc[pid][1]] = 0
                    persons_loc[pid] = cand[:2]
                    board[persons_loc[pid][0]][persons_loc[pid][1]] = -2
                    answer += 1
                    if verbose:
                        print(f"Info: moving person #{pid} to ({persons_loc[pid][0]}, {persons_loc[pid][1]}).")

                    break

    # 2. 게임 종료 여부 갱신
    if 0 == sum(persons_state):
        if verbose:
            print(f"Info: game over. all persons have left the maze.")

        is_over = True
        print(answer)
        print(exit_loc)

        break

    # 3. 미로 회전
    persons_cand = [value for index, value in enumerate(persons_loc) if 1 == persons_state[index]]
    persons_cand.sort(key=lambda x: (get_dist(er, ec, x[0], x[1]), x[0], x[1]))
    sr, sc = persons_cand[0]

    square_len = max(abs(er - sr), abs(ec - sc))
    is_cand = False
    for i in range(er - square_len, er + 1):
        for j in range(ec - square_len, ec + 1):
            r1, c1, r2, c2 = i, j, i + square_len, j + square_len

            if is_valid_loc(r1, c1) and is_valid_loc(r2, c2) and r1 <= sr <= r2 and c1 <= sc <= c2:
                is_cand = True
                tr1, tc1, tr2, tc2 = r1, c1, r2, c2

                break

        if is_cand:
            break

    tmp_board = []
    for i in range(tr1, tr2 + 1):
        tmp_board.append(board[i][tc1:(tc2 + 1)])
    rotated_board = [[0 for _ in range(square_len + 1)] for _ in range(square_len + 1)]
    for i in range(square_len + 1):
        for j in range(square_len + 1):
            rotated_board[j][square_len - i] = tmp_board[i][j]
            if 0 < rotated_board[j][square_len - i]:
                rotated_board[j][square_len - i] -= 1

    if verbose:
        print(f"Info: square of length {square_len} with diagonal tip at ({tr1}, {tc1}), ({tr2}, {tc2}) and person at ({sr}, {sc}) in it.")
        for i in range(square_len + 1):
            for j in range(square_len + 1):
                print(f"{tmp_board[i][j]:3}", end="")
            print("")
        print(f"{'-' * 20}")
        for i in range(square_len + 1):
            for j in range(square_len + 1):
                print(f"{rotated_board[i][j]:3}", end="")
            print("")

    # 4. 미로 갱신
    for i in range(len(board)):
        for j in range(len(board[0])):
            if PERSON == board[i][j]:
                board[i][j] = 0

    for pid in range(1, persons_cnt + 1):
        if persons_state[pid]:
            if tr1 <= persons_loc[pid][0] <= tr2 and tc1 <= persons_loc[pid][1] <= tc2:
                persons_loc[pid] = [(persons_loc[pid][1] - tc1) + tr1, square_len - (persons_loc[pid][0] - tr1) + tc1]
            board[persons_loc[pid][0]][persons_loc[pid][1]] = -2

    for i in range(len(rotated_board)):
        for j in range(len(rotated_board[0])):
            board[i + tr1][j + tc1] = rotated_board[i][j]

    if tr1 <= exit_loc[0] <= tr2 and tc1 <= exit_loc[1] <= tc2:
        exit_loc = [(exit_loc[1] - tc1) + tr1, square_len - (exit_loc[0] - tr1) + tc1]

    if verbose:
        print(f"{'-' * 20}")
        for i in range(n + 2):
            for j in range(n + 2):
                print(f"{board[i][j]:3}", end='')
            print('')
        print(f"{'-' * 20}")
        print(persons_loc)
        print(exit_loc)

if not is_over:
    print(answer)
    print(f"{exit_loc[0]} {exit_loc[1]}")