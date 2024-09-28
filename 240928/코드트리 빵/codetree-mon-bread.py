# --- Libraries

from collections import deque

# --- Variables

N, M = map(int, input().split())

persons = [(-1, -1)] * (M + 1)
arrived = [False] * (M + 1)

board = [list(map(int, input().split())) for _ in range(N)]
valid = [[True] * N for _ in range(N)]

stores = [(0, 0)] + [tuple(map(lambda x: int(x) - 1, input().split())) for _ in range(M)]

deltas = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1)
]

# --- Functions

def in_range(r: int, c: int):
    return 0 <= r < N and 0 <= c < N

# --- main()
answer = 0

while True:
    answer += 1

    # 1. Move persons.
    for idx in range(1, M + 1):
        if answer > idx and not arrived[idx]:
            r, c = persons[idx]

            next_d = -1
            
            visited = [[False] * N for _ in range(N)]
            q = deque()
            
            # Initialize.
            visited[r][c] = True
            for d in range(4):
                next_r, next_c = r + deltas[d][0], c + deltas[d][1]
                
                if in_range(next_r, next_c) and valid[next_r][next_c]:
                    visited[next_r][next_c] = True
                    q.append((next_r, next_c, d))
            
            # Search.
            while q:
                cur_r, cur_c, cur_d = q.popleft()
                
                if stores[idx] == (cur_r, cur_c):
                    next_d = cur_d
                    break
                    
                for d in range(4):
                    next_r, next_c = cur_r + deltas[d][0], cur_c + deltas[d][1]
                    
                    if in_range(next_r, next_c) and not visited[next_r][next_c] and valid[next_r][next_c]:
                        visited[next_r][next_c] = True
                        q.append((next_r, next_c, cur_d))
            
            # Update (coordinates).
            persons[idx] = (r + deltas[next_d][0], c + deltas[next_d][1])

    # 2. Handle arrivals.
    for idx in range(1, M + 1):
        if answer > idx and not arrived[idx] and persons[idx] == stores[idx]:
            arrived[idx] = True
            valid[stores[idx][0]][stores[idx][1]] = False

    # 3. Exit game.
    if M < answer and M == sum(arrived):
        break

    # 4. Move t-th person.
    if M >= answer:
        r, c = stores[answer]

        targets = []

        visited = [[0] * N for _ in range(N)]
        q = deque()

        visited[r][c] = 1
        q.append((r, c))

        while q:
            cur_r, cur_c = q.popleft()

            if board[cur_r][cur_c]:
                targets.append((cur_r, cur_c, visited[cur_r][cur_c]))

            for d in range(4):
                next_r, next_c = cur_r + deltas[d][0], cur_c + deltas[d][1]

                if in_range(next_r, next_c) and not visited[next_r][next_c] and valid[next_r][next_c]:
                    visited[next_r][next_c] = visited[cur_r][cur_c] + 1
                    q.append((next_r, next_c))

        targets.sort(key=lambda x: (x[2], x[0], x[1]))

        persons[answer] = (targets[0][0], targets[0][1])
        valid[persons[answer][0]][persons[answer][1]] = False

print(answer)