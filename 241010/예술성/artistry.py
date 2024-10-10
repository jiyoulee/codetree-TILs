# --- Packages

from collections import deque, defaultdict

# --- Variables

debug = False

N = int(input())

grid = [list(map(int, input().split())) for _ in range(N)]
grid_idx = [[0] * N for _ in range(N)]

if debug:
    for row in grid:
        print(row)
    print("-" * 100)

group_id = []
group_cnt = []
edges_cnt = []

deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

answer = 0

# --- Functions

def in_range(r: int, c: int):
    return 0 <= r < N and 0 <= c < N

# --- Main Logic

for t in range(4):
    group_id = [0]
    group_cnt = [1]
    edges_cnt = [defaultdict(int)]
    
    grid_idx = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if not grid_idx[r][c]:
                init_r, init_c, init_id, gidx = r, c, grid[r][c], len(group_id)
                group_id.append(init_id)
                group_cnt.append(1)
                edges_cnt.append(defaultdict(int))

                q = deque()
                
                grid_idx[init_r][init_c] = gidx
                q.append((init_r, init_c))
                
                while q:
                    cur_r, cur_c = q.pop()
                    
                    for (dr, dc) in deltas:
                        next_r, next_c = cur_r + dr, cur_c + dc
                        if in_range(next_r, next_c) and not grid_idx[next_r][next_c] and init_id == grid[next_r][next_c]:
                            grid_idx[next_r][next_c] = gidx
                            q.append((next_r, next_c))

    visited = [[False] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if not visited[r][c]:
                init_r, init_c, init_idx = r, c, grid_idx[r][c]

                q = deque()

                visited[init_r][init_c] = True
                q.append((init_r, init_c))

                while q:
                    cur_r, cur_c = q.pop()

                    for (dr, dc) in deltas:
                        next_r, next_c = cur_r + dr, cur_c + dc
                        if in_range(next_r, next_c):
                            next_idx = grid_idx[next_r][next_c]
                            if not visited[next_r][next_c] and init_idx == next_idx:
                                group_cnt[init_idx] += 1
                                visited[next_r][next_c] = True
                                q.append((next_r, next_c))
                            elif init_idx != next_idx:
                                edges_cnt[init_idx][next_idx] += 1

    if debug:
        for row in grid_idx:
            print(row)
        print(group_id)
        print(group_cnt)
        for dict in edges_cnt:
            print(dict)

    for aidx in range(len(group_id)):
        for bidx in range(aidx + 1, len(group_id)):
            answer += (group_cnt[aidx] + group_cnt[bidx]) * group_id[aidx] * group_id[bidx] * edges_cnt[aidx][bidx]

    mid = (N - 1) // 2
    grid_copy = [[grid[r][c] for c in range(N)] for r in range(N)]
    for x in range(N):
        grid[mid][x] = grid_copy[x][N - 1 - mid]
        grid[x][mid] = grid_copy[mid][N - 1 - x]
    for (init_r, init_c) in [(0, 0), (0, (N + 1) // 2), ((N + 1) // 2, 0), ((N + 1) // 2, (N + 1) // 2)]:
        submatrix = [[grid[r][c] for c in range(init_c, init_c + mid)] for r in range(init_r, init_r + mid)]
        rotated = [[submatrix[mid - 1 - c][r] for c in range(mid)] for r in range(mid)]
        for r in range(mid):
            for c in range(mid):
                grid[r + init_r][c + init_c] = rotated[r][c]

    if debug:
        for row in grid:
            print(row)
        print("-" * 100)

                
print(answer)