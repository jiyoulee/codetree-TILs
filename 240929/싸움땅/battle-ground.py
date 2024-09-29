# --- Libraries

import heapq

# --- Variables

N, M, K = map(int, input().split())

guns = [[[] for _ in range(N + 1)] for _ in range(N + 1)]
for i in range(1, N + 1):
    row = [0] + list(map(int, input().split()))
    for j in range(1, N + 1):
        if row[j]:
            heapq.heappush(guns[i][j], -row[j])

persons = [[0, 0, 0, 0, 0]]
grid = [[0] * (N + 1) for _ in range(N + 1)]
for idx1 in range(1, M + 1):
    r, c, d, s = map(int, input().split())

    persons.append([r, c, d, s, 0])
    grid[r][c] = idx1

deltas = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]

# --- Functions

# for i in range(1, N + 1):
#     for j in range(1, N + 1):
#         print(f"{0:5}" if not guns[i][j] else f"{guns[i][j][0]:5}", end=" ")
#     print("")

def in_range(r: int, c: int):
    return 1 <= r <= N and 1 <= c <= N

# --- Main Logic

answer = [0] * (M + 1)

for k in range(1, K + 1):
    for idx in range(1, M + 1):
        idx1 = idx
        r1, c1, d1, s1, g1 = persons[idx1]
        
        grid[r1][c1] = 0
        
        r, c = r1 + deltas[d1][0], c1 + deltas[d1][1]
        if not in_range(r, c):
            d1 = (d1 + 2) % 4
            r, c, = r1 + deltas[d1][0], c1 + deltas[d1][1]
        r1, c1 = r, c
        
        persons[idx1][0], persons[idx1][1], persons[idx1][2] = r1, c1, d1
        
        if not grid[r1][c1]:
            grid[r1][c1] = idx1
            
            if g1:
                heapq.heappush(guns[r1][c1], -g1)
            if guns[r1][c1]:
                persons[idx1][4] = -heapq.heappop(guns[r1][c1])
            
            continue

        idx2 = grid[r1][c1]
        r2, c2, d2, s2, g2 = persons[idx2]

        (winner, loser) = (idx1, idx2) if (
            (s1 + g1 > s2 + g2)
            or (s1 + g1 == s2+ g2 and s1 > s2)
        ) else (idx2, idx1)

        idx1, idx2 = winner, loser
        r1, c1, d1, s1, g1 = persons[winner]
        r2, c2, d2, s2, g2 = persons[loser]

        answer[idx1] += s1 + g1 - s2 - g2

        if g2:
            heapq.heappush(guns[r2][c2], -g2)
            persons[idx2][4] = 0

        for d in range(4):
            next_d2 = (d2 + d) % 4
            r, c = r2 + deltas[next_d2][0], c2 + deltas[next_d2][1]

            if in_range(r, c) and not grid[r][c]:
                r2, c2, d2 = r, c, next_d2
                break
        persons[idx2][0], persons[idx2][1], persons[idx2][2] = r2, c2, d2
        grid[r2][c2] = idx2

        if guns[r2][c2]:
            persons[idx2][4] = -heapq.heappop(guns[r2][c2])

        grid[r1][c1] = idx1

        if g1 > 0:
            heapq.heappush(guns[r1][c1], -g1)
        if guns[r1][c1]:
            persons[idx1][4] = -heapq.heappop(guns[r1][c1])

for point in answer[1:]:
    print(point, end=" ")