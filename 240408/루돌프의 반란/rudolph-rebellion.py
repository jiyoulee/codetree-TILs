# 1. 변수 정의 및 입력
answer = ""
verbose = False
WALL = 0
RUDOLF = -1
get_distance = lambda r1, c1, r2, c2: ((r1 - r2) ** 2 + (c1 - c2) ** 2)
dr = [-1, 0, 1, 0, -1, 1, -1, 1]
dc = [0, 1, 0, -1, -1, -1, 1, 1]
rdr = [1, 0, -1, 0, 1, -1, 1, -1]
rdc = [0, -1, 0, 1, 1, 1, -1, -1]

n, turn_cnt, santas_cnt, rudolf_strength, santa_strength = list(map(int, input().split()))
is_valid_loc = lambda r1, c1: (r1 and (n >= r1) and c1 and (n >= c1))
board = [[0 for _ in range(n + 2)] for _ in range(n + 2)]

# 1. 루돌프
r, c = list(map(int, input().split()))
rudolf_loc = [r, c]
board[r][c] = RUDOLF

# 2. 산타
santas_loc = [[0 for _ in range(2)] for _ in range(santas_cnt + 1)]
santas_state = [-1 for _ in range(santas_cnt + 1)]
santas_state[0] = 0
santas_score = [0 for _ in range(santas_cnt + 1)]
for _ in range(santas_cnt):
    santa_id, r, c = list(map(int, input().split()))
    santas_loc[santa_id][0] = r
    santas_loc[santa_id][1] = c
    board[r][c] = santa_id

if verbose:
    print("Info: board initialized.")
    print(f"{'-' * 20}")
    for row in board:
        print(row)
    print(f"{'-' * 20}")

# 2. 계산
for turn_id in range(1, turn_cnt + 1):
    if verbose:
        print(f"{'*' * 20}")
        print(f"Info: starting turn #{turn_id}.")
        print(f"{'*' * 20}")

    # 1 산타 부활
    for santa_id in range(1, santas_cnt + 1):
        if turn_id == santas_state[santa_id]:
            santas_state[santa_id] = -1

    if verbose:
        print(f"Info: alive santas are {[index for index, state in enumerate(santas_state) if 0 > state]}.")

    # 2. 루돌프 이동
    rr, rc = rudolf_loc

    # 1. 최소 거리 산타 탐색
    santas_cand = [loc for loc, state in zip(santas_loc, santas_state) if state]
    santas_cand.sort(key=lambda x: (-get_distance(rr, rc, x[0], x[1]), x[0], x[1]), reverse=True)
    min_sr, min_sc = santas_cand[0]

    # 2. 루돌프 이동 방향 및 위치 탐색
    rudolf_cand = [[0 for _ in range(3)] for _ in range(8)]
    for d in range(8):
        rudolf_cand[d][0] = d
        rudolf_cand[d][1] = rr + dr[d]
        rudolf_cand[d][2] = rc + dc[d]
    rudolf_cand.sort(key=lambda x: get_distance(min_sr, min_sc, x[1], x[2]))
    min_d, min_rr, min_rc = rudolf_cand[0]

    # 3. 루돌프 위치 갱신
    if verbose:
        print(f"Info: moving rudolf to ({min_rr}, {min_rc}).")

    board[rr][rc] = 0
    rudolf_loc[0] = min_rr
    rudolf_loc[1] = min_rc
    rr, rc = rudolf_loc

    # 4. 루돌프 이동
    if not board[rr][rc]:
        board[rr][rc] = RUDOLF
    else:
        santa_id = board[rr][rc]
        sr = santas_loc[santa_id][0]
        sc = santas_loc[santa_id][1]

        board[rr][rc] = RUDOLF

        # 1. 산타 점수 부여
        santas_score[santa_id] += rudolf_strength

        # 2. 산타 위치 갱신
        santas_loc[santa_id][0] += rudolf_strength * dr[min_d]
        santas_loc[santa_id][1] += rudolf_strength * dc[min_d]
        sr, sc = santas_loc[santa_id]

        if verbose:
            print(f"Info: moving santa #{santa_id} to ({sr}, {sc}).")

        # 3. 산타 상태 갱신
        if not is_valid_loc(santas_loc[santa_id][0], santas_loc[santa_id][1]):
            santas_state[santa_id] = 0
        else:
            santas_state[santa_id] = turn_id + 2

        # 4. 산타 연쇄 이동
        while is_valid_loc(sr, sc) and board[sr][sc]:
            new_santa_id = board[sr][sc]
            board[sr][sc] = santa_id

            santas_loc[new_santa_id][0] += dr[min_d]
            santas_loc[new_santa_id][1] += dc[min_d]

            if not is_valid_loc(santas_loc[new_santa_id][0], santas_loc[new_santa_id][1]):
                santas_state[new_santa_id] = 0

            sr = santas_loc[new_santa_id][0]
            sc = santas_loc[new_santa_id][1]
            santa_id = new_santa_id
        if is_valid_loc(sr, sc):
            board[sr][sc] = santa_id

    if verbose:
        print(f"{'-' * 20}")
        for row in board:
            print(row)
        print(f"{'-' * 20}")

    # 4. 산타 이동
    rr, rc = rudolf_loc

    for santa_id in range(1, santas_cnt + 1):
        if -1 == santas_state[santa_id]:
            sr, sc = santas_loc[santa_id]

            # 1. 산타 이동 방향 및 위치 탐색
            cur_dist = get_distance(rr, rc, sr, sc)
            santa_cand = [[0 for _ in range(4)] for _ in range(4)]
            for d in range(4):
                santa_cand[d][0] = d
                santa_cand[d][1] = sr + dr[d]
                santa_cand[d][2] = sc + dc[d]
                santa_cand[d][3] = get_distance(rr, rc, sr + dr[d], sc + dc[d])
            santa_cand = [santa for santa in santa_cand if cur_dist > santa[3]]
            santa_cand.sort(key=lambda x: (x[3], x[0]))
            if verbose:
                print(santa_cand)
            is_cand = False
            for cand in santa_cand:
                d, r, c, _ = cand

                if 0 >= board[r][c]:
                    is_cand = True
                    min_d = d
                    min_sr = r
                    min_sc = c
                    break

            # 2. 산타 좌표 갱신
            if is_cand:
                if verbose:
                    print(f"Info: moving santa #{santa_id} to ({min_sr}, {min_sc})")

                board[sr][sc] = 0
                santas_loc[santa_id][0] = min_sr
                santas_loc[santa_id][1] = min_sc
                sr, sc = santas_loc[santa_id]

                # 3. 산타 -> 루돌프 충돌
                if RUDOLF == board[min_sr][min_sc]:
                    # 1. 산타 점수 갱신
                    santas_score[santa_id] += santa_strength

                    # 2. 산타 위치 갱신
                    santas_loc[santa_id][0] += santa_strength * rdr[min_d]
                    santas_loc[santa_id][1] += santa_strength * rdc[min_d]
                    sr, sc = santas_loc[santa_id]

                    # 3. 산타 상태 갱신
                    if not is_valid_loc(sr, sc):
                        santas_state[santa_id] = 0
                    else:
                        santas_state[santa_id] = turn_id + 2

                # 3. 산타 연쇄 이동
                while is_valid_loc(sr, sc) and board[sr][sc]:
                    new_santa_id = board[sr][sc]
                    board[sr][sc] = santa_id

                    santas_loc[new_santa_id][0] += rdr[min_d]
                    santas_loc[new_santa_id][1] += rdc[min_d]

                    if not is_valid_loc(santas_loc[new_santa_id][0], santas_loc[new_santa_id][1]):
                        santas_state[new_santa_id] = 0

                    sr = santas_loc[new_santa_id][0]
                    sc = santas_loc[new_santa_id][1]
                    santa_id = new_santa_id
                if is_valid_loc(sr, sc):
                    board[sr][sc] = santa_id

                if verbose:
                    print(f"{'-' * 20}")
                    for row in board:
                        print(row)
                    print(f"{'-' * 20}")

    # n. 산타 추가 점수 부여
    for santa_id in range(1, santas_cnt + 1):
        if santas_state[santa_id]:
            santas_score[santa_id] += 1

    # n + 1. 턴 종료
    if 0 == sum(santas_state):
        if verbose:
            print("Info: game over due to lack of santas.")

        break

# 3. 출력
for score in santas_score[1:]:
    answer = "".join([answer, f"{score} "])

print(answer.strip())