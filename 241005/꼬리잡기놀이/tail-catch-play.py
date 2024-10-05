# --- Packages

# --- Variables

N, M, K = map(int, input().split())

grid = [list(map(int, input().split())) for _ in range(N)]
teams = [[] for _ in range(M)]
answers = [0] * M

deltas = [(0, 1), (-1, 0), (0, -1), (1, 0)]

# --- Functions

def in_range(r: int, c: int):
    return 0 <= r < N and 0 <= c < N


def update_team(ball_r, ball_c):
    global answers, teams
    
    flag = False
    for idx in range(M):
        for i in range(len(teams[idx])):
            cur_r, cur_c = teams[idx][i]

            if ball_r != cur_r:
                continue
            if ball_c != cur_c:
                continue

            answers[idx] += (i + 1) ** 2
            teams[idx] = teams[idx][::-1]
            flag = True
            break

        if flag:
            break


# --- Main Logic

idx = 0
for i in range(N):
    for j in range(N):
        if 1 == grid[i][j]:
            cur_r, cur_c = i, j

            grid[cur_r][cur_c] = 5
            teams[idx].append((cur_r, cur_c))

            while True:
                updated = False

                for d in range(4):
                    next_r, next_c = cur_r + deltas[d][0], cur_c + deltas[d][1]
                    if in_range(next_r, next_c) and 2 == grid[next_r][next_c]:
                        grid[next_r][next_c] = 5
                        teams[idx].append((next_r, next_c))
                        cur_r, cur_c = next_r, next_c
                        updated = True
                        break

                if not updated:
                    break

            for d in range(4):
                next_r, next_c = cur_r + deltas[d][0], cur_c + deltas[d][1]
                if 3 == grid[next_r][next_c]:
                    grid[next_r][next_c] = 5
                    teams[idx].append((next_r, next_c))
                    break

            idx += 1

for k in range(K):
    for idx in range(M):
        (tail_r, tail_c) = teams[idx][-1]
        grid[tail_r][tail_c] = 4

        (top_r, top_c) = teams[idx][0]
        for d in range(4):
            new_r, new_c = top_r + deltas[d][0], top_c + deltas[d][1]
            if in_range(new_r, new_c) and 4 == grid[new_r][new_c]:
                grid[new_r][new_c] = 5
                break

        teams[idx] = [(new_r, new_c)] + teams[idx][:-1]

    remainder = k % (4 * N)
    if N > remainder:
        ball_r = remainder
        for ball_c in range(N):
            if 5 == grid[ball_r][ball_c]:
                update_team(ball_r, ball_c)
                break
    elif 2 * N > remainder:
        ball_c = remainder - N
        for ball_r in range(N - 1, -1, -1):
            if 5 == grid[ball_r][ball_c]:
                update_team(ball_r, ball_c)
                break
    elif 3 * N > remainder:
        ball_r = -remainder + 3 * N - 1
        for ball_c in range(N - 1, -1, -1):
            if 5 == grid[ball_r][ball_c]:
                update_team(ball_r, ball_c)
                break
    else:
        ball_c = -remainder + 4 * N - 1
        for ball_r in range(N):
            if 5 == grid[ball_r][ball_c]:
                update_team(ball_r, ball_c)
                break

print(sum(answers))