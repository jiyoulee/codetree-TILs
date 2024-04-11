from collections import deque

# 1. 정의
answer = 0
verbose = False
dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

# 2. 입력
num_rows, num_persons = list(map(int, input().split()))
is_valid_loc = lambda x: (0 <= x[0] < num_rows and 0 <= x[1] < num_rows)
board = [list(map(int, input().split())) for _ in range(num_rows)]
persons = [(-1, -1) for _ in range(num_persons)]
stores = [tuple(map(lambda x: (x - 1), map(int, input().split()))) for _ in range(num_persons)]

for tid in range(10):
    if verbose:
        print(f"Info: {tid} seconds.")

    # 1. 사람 이동
    for pid in range(min(tid, num_persons)):
        if stores[pid] != persons[pid]:
            deq = deque()
            visited = [[False] * num_rows for _ in range(num_rows)]

            shortest_path = []
            deq.append([pid, persons[pid], []])
            visited[persons[pid][0]][persons[pid][1]] = True
            while deq:
                cur_pid, cur_ploc, cur_path = deq.popleft()

                if stores[cur_pid] == cur_ploc:
                    shortest_path = cur_path
                    break

                next_plocs = [(cur_ploc[0] + dr[d], cur_ploc[1] + dc[d]) for d in range(4)]
                for next_ploc in next_plocs:
                    if is_valid_loc(next_ploc) and not visited[next_ploc[0]][next_ploc[1]] and 2 != board[next_ploc[0]][next_ploc[1]]:
                        visited[next_ploc[0]][next_ploc[1]] = True
                        deq.append([pid, next_ploc, [*cur_path, next_ploc]])

            if shortest_path:
                persons[pid] = shortest_path[0]

    # 2. 종료 조건 갱신 (O)
    if persons == stores:
        answer = tid + 1
        break

    # 3. 편의점 정지 (o)
    for i in range(num_persons):
        if persons[i] == stores[i]:
            board[stores[i][0]][stores[i][1]] = 2

    # 4. t번 사람 이동
    if num_persons > tid:
        deq = deque()
        visited = [[False] * num_rows for _ in range(num_rows)]

        basecamp_cand = []
        deq.append([stores[tid], []])
        visited[stores[tid][0]][stores[tid][1]] = True
        while deq:
            cur_loc, cur_path = deq.popleft()

            if 1 == board[cur_loc[0]][cur_loc[1]]:
                basecamp_cand.append([cur_loc, len(cur_path)])

            next_locs = [(cur_loc[0] + dr[d], cur_loc[1] + dc[d]) for d in range(4)]
            for next_loc in next_locs:
                if is_valid_loc(next_loc) and not visited[next_loc[0]][next_loc[1]] and 2 != board[next_loc[0]][next_loc[1]]:
                    visited[next_loc[0]][next_loc[1]] = True
                    deq.append([next_loc, [*cur_path, next_loc]])

        basecamp_cand.sort(key=lambda x: (x[1], x[0][0], x[0][1]))
        persons[tid] = basecamp_cand[0][0]
        board[persons[tid][0]][persons[tid][1]] = 2

    if verbose:
        verbose_board = copy.deepcopy(board)
        for pid, ploc in enumerate(persons):
            if 0 <= persons[pid][0]:
                verbose_board[ploc[0]][ploc[1]] = -(pid + 1)
        for r in range(num_rows):
            for c in range(num_rows):
                print(f"{verbose_board[r][c]:5}", end="")
            print("")

print(answer)