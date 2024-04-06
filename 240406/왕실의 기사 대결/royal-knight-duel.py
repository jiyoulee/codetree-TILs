from collections import deque

# Read from file.
# import sys
# sys.stdin = open("input.txt", "r")

# 1. Define
answer = 0
verbose = False
TRAP = 1
WALL = 2

l, n, q = list(map(int, input().split()))

# 1. 전쟁터 정보
traps_board = [[WALL for _ in range(l + 2)] for _ in range(l + 2)]
for i in range(1, l + 1):
    input_list = list(map(int, input().split()))
    for j in range(1, l + 1):
        traps_board[i][j] = input_list[j - 1]

# 2. 기사 정보
knights_board = [[0 for _ in range(l + 2)] for _ in range(l + 2)]
knights_location = [[0 for _ in range(4)] for _ in range(n + 1)]
knights_stamina = [0 for _ in range(n + 1)]
knights_damage = [0 for _ in range(n + 1)]
for knight_id in range(1, n + 1):
    r, c, h, w, k = list(map(int, input().split()))
    knights_stamina[knight_id] = k
    knights_location[knight_id][0] = r
    knights_location[knight_id][1] = c
    knights_location[knight_id][2] = h
    knights_location[knight_id][3] = w
    for row in range(r, r + h):
        for col in range(c, c + w):
            knights_board[row][col] = knight_id

if verbose:
    print(f"initial:")
    for row in traps_board:
        print(row)
    print(f"{'-' * 20}")
    for row in knights_board:
        print(row)
    print(f"{'-' * 20}")

# 2. Compute
for _ in range(q):
    start_knight, d = list(map(int, input().split()))
    if verbose:
        print(f"Info: processing order with ({start_knight}, {d}).")

    if knights_stamina[start_knight] <= knights_damage[start_knight]:
        continue

    knights_id = []
    deq = deque()
    visited = [False for _ in range(n + 1)]
    is_valid = True

    # 1. 기사 이동
    deq.append(start_knight)
    knights_id.append(start_knight)
    while is_valid and deq:
        cur_knight = deq.popleft()
        if verbose:
            print(f"cur_knight: {cur_knight}")

        r, c, h, w = knights_location[cur_knight]
        if 0 == d:
            if verbose:
                print(f"Info: going up.")

            for col in range(c, c + w):
                if verbose:
                    print(f"checking square: ({r - 1}, {col})")

                if WALL == traps_board[r - 1][col]:
                    is_valid = False
                    break
                else:
                    next_knight = knights_board[r - 1][col]

                    if next_knight and not visited[next_knight]:
                        visited[next_knight] = True
                        deq.append(next_knight)
                        knights_id.append(next_knight)
        elif 1 == d:
            if verbose:
                print(f"Info: going right.")

            for row in range(r, r + h):
                if verbose:
                    print(f"checking square: ({row}, {c + w})")

                if WALL == traps_board[row][c + w]:
                    is_valid = False
                    break
                else:
                    next_knight = knights_board[row][c + w]

                    if next_knight and not visited[next_knight]:
                        visited[next_knight] = True
                        deq.append(next_knight)
                        knights_id.append(next_knight)
        elif 2 == d:
            if verbose:
                print(f"Info: going down.")

            for col in range(c, c + w):
                if verbose:
                    print(f"checking square: ({r + h}, {col})")

                if WALL == traps_board[r + h][col]:
                    is_valid = False
                    break
                else:
                    next_knight = knights_board[r + h][col]

                    if next_knight and not visited[next_knight]:
                        visited[next_knight] = True
                        deq.append(next_knight)
                        knights_id.append(next_knight)
        elif 3 == d:
            if verbose:
                print(f"Info: going left.")

            for row in range(r, r + h):
                if verbose:
                    print(f"checking square: ({row}, {c - 1})")

                if WALL == traps_board[row][c - 1]:
                    is_valid = False
                    break
                else:
                    next_knight = knights_board[row][c - 1]

                    if next_knight and not visited[next_knight]:
                        visited[next_knight] = True
                        deq.append(next_knight)
                        knights_id.append(next_knight)

    # 2. 대결 대미지
    if is_valid and knights_id:
        if verbose:
            print(f"Info: wall check has passed. tracked knights are {knights_id}.")

        # 1. 기사 갱신
        if 0 == d:
            for knight in knights_id[1:]:
                r, c, h, w = knights_location[knight]

                # 1. 위치 갱신
                knights_location[knight][0] -= 1

                # 2. 대결 대미지 갱신
                for row in range(r - 1, r + h - 1):
                    for col in range(c, c + w):
                        if TRAP == traps_board[row][col]:
                            knights_damage[knight] += 1

            knights_location[knights_id[0]][0] -= 1
        if 1 == d:
            for knight in knights_id[1:]:
                r, c, h, w = knights_location[knight]

                # 1. 위치 갱신
                knights_location[knight][1] += 1

                # 2. 대결 대미지 갱신
                for row in range(r, r + h):
                    for col in range(c + 1, c + w + 1):
                        if TRAP == traps_board[row][col]:
                            knights_damage[knight] += 1

            knights_location[knights_id[0]][1] += 1
        if 2 == d:
            for knight in knights_id[1:]:
                r, c, h, w = knights_location[knight]

                # 1. 위치 갱신
                knights_location[knight][0] += 1

                # 2. 대결 대미지 갱신
                for row in range(r + 1, r + h + 1):
                    for col in range(c, c + w):
                        if TRAP == traps_board[row][col]:
                            knights_damage[knight] += 1

            knights_location[knights_id[0]][0] += 1
        if 3 == d:
            for knight in knights_id[1:]:
                r, c, h, w = knights_location[knight]

                # 1. 위치 갱신
                knights_location[knight][1] -= 1

                # 2. 대결 대미지 갱신
                for row in range(r, r + h):
                    for col in range(c - 1, c + w - 1):
                        if TRAP == traps_board[row][col]:
                            knights_damage[knight] += 1

            knights_location[knights_id[0]][1] -= 1

        # 2. 기사 보드 갱신
        knights_board = [[0 for _ in range(l + 2)] for _ in range(l + 2)]
        for knight in range(1, n + 1):
            if knights_stamina[knight] > knights_damage[knight]:
                r, c, h, w = knights_location[knight]
                for row in range(r, r + h):
                    for col in range(c, c + w):
                        knights_board[row][col] = knight
    else:
        if verbose:
            print("Exception: knight cannot move due to wall.")

    if verbose:
        print(f"{'-' * 20}")
        for row in traps_board:
            print(row)
        print(f"{'-' * 20}")
        for row in knights_board:
            print(row)
        print(f"{'-' * 20}")

# Output
for i in range(1, n + 1):
    if knights_stamina[i] > knights_damage[i]:
        answer += knights_damage[i]

print(answer)