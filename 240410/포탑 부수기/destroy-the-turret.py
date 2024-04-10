from collections import deque

# 1. 정의
answer = 0
verbose = False
dr = [0, 1, 0, -1, -1, -1, 1, 1]
dc = [1, 0, -1, 0, -1, 1, -1, 1]

# 2. 입력
num_rows, num_cols, num_turns = list(map(int, input().split()))
turret_strength = [list(map(int, input().split())) for _ in range(num_rows)]
turret_state = [[0] * num_cols for _ in range(num_rows)]

# 3. 계산
for turn_id in range(1, num_turns + 1):
    if verbose:
        print(f"Info: turn {turn_id}.")
        print(f"{'-' * 20}")
        for i in range(num_rows):
            for j in range(num_cols):
                print(f"{turret_strength[i][j]:5}", end="")
            print("")
        print(f"{'-' * 20}")

    # 1. 공격자 선정
    attacker = [0, 0]
    for r in range(num_rows):
        for c in range(num_cols):
            if 0 < turret_strength[r][c]:
                attacker = [r, c]
                break
        if 0 < turret_strength[r][c]:
            break
    defender = [0, 0]

    for r in range(num_rows):
        for c in range(num_cols):
            if 0 < turret_strength[r][c]:
                # 1. 공격지
                if turret_strength[r][c] < turret_strength[attacker[0]][attacker[1]]:
                    attacker = [r, c]
                elif turret_strength[r][c] == turret_strength[attacker[0]][attacker[1]]:
                    if turret_state[r][c] > turret_state[attacker[0]][attacker[1]]:
                        attacker = [r, c]
                    elif turret_state[r][c] == turret_state[attacker[0]][attacker[1]]:
                        if r + c > attacker[0] + attacker[1]:
                            attacker = [r, c]
                        elif r + c == attacker[0] + attacker[1]:
                            if c > attacker[1]:
                                attacker = [r, c]

                # 2. 공격 대상
                if turret_strength[r][c] > turret_strength[defender[0]][defender[1]]:
                    defender = [r, c]
                elif turret_strength[r][c] == turret_strength[defender[0]][defender[1]]:
                    if turret_state[r][c] < turret_state[defender[0]][defender[1]]:
                        defender = [r, c]
                    elif turret_state[r][c] == turret_state[defender[0]][defender[1]]:
                        if r + c < defender[0] + defender[1]:
                            defender = [r, c]
                        elif r + c == defender[0] + defender[1]:
                            if c < defender[1]:
                                defender = [r, c]

    turret_state[attacker[0]][attacker[1]] = turn_id
    turret_strength[attacker[0]][attacker[1]] += num_rows + num_cols

    if verbose:
        print(f"Info: attacker at ({attacker[0]}, {attacker[1]}), defender at ({defender[0]}, {defender[1]}).")

    # 2. 공격자의 공격
    turrets = []
    visited = [[False] * num_cols for _ in range(num_rows)]
    deq = deque()

    deq.append([attacker, [attacker]])
    visited[attacker[0]][attacker[1]] = True
    while deq:
        cur_turret, path = deq.popleft()

        if defender == cur_turret:
            turrets = path
            break

        for d in range(4):
            next_turret = [(cur_turret[0] + dr[d]) % num_rows, (cur_turret[1] + dc[d]) % num_cols]

            if 0 < turret_strength[next_turret[0]][next_turret[1]] and not visited[next_turret[0]][next_turret[1]]:
                visited[next_turret[0]][next_turret[1]] = True
                deq.append([next_turret, [*path + [next_turret]]]) # <- REVIEW!

    if not turrets:
        turrets = [[(defender[0] + dr[d]) % num_rows, (defender[1] + dc[d]) % num_cols] for d in range(8)] + [attacker, defender]

    if verbose:
        print(f"Info: effected turrets are {turrets}.")

    # 3. 포탑 부서짐
    attack_strength = turret_strength[attacker[0]][attacker[1]]
    turret_strength[defender[0]][defender[1]] -= attack_strength
    for turret in turrets:
        if turret not in [attacker, defender]:
            turret_strength[turret[0]][turret[1]] -= attack_strength // 2

    # 4. 포탑 정비 및 종료 여부 갱신
    num_turrets = 0
    for r in range(num_rows):
        for c in range(num_cols):
            if 0 < turret_strength[r][c]:
                num_turrets += 1
                if [r, c] not in turrets:
                    turret_strength[r][c] += 1

    if 1 >= num_turrets:
        break

# 4. 출력
if verbose:
    print(f"Info: turn {turn_id}.")
    print(f"{'-' * 20}")
    for i in range(num_rows):
        for j in range(num_cols):
            print(f"{turret_strength[i][j]:5}", end="")
        print("")
    print(f"{'-' * 20}")

for r in range(num_rows):
    for c in range(num_cols):
        if turret_strength[r][c] > answer:
            answer = turret_strength[r][c]

print(answer)