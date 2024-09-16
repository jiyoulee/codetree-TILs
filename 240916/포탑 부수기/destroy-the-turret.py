from collections import deque

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

attack_time_list = [[0] * M for _ in range(N)]
d8 = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1)
]
FALSE = 21


def get_min_dist(src_pos, dst_pos):
    src_r, src_c = src_pos
    dst_r, dst_c = dst_pos

    q = deque()
    visited = [[FALSE] * M for _ in range(N)]

    visited[src_r][src_c] = 0
    q.append(src_pos)
    while q:
        cur_r, cur_c = q.popleft()

        for d in range(4):
            next_r, next_c = (cur_r + d8[d][0]) % N, (cur_c + d8[d][1]) % M
            if FALSE == visited[next_r][next_c] and board[next_r][next_c] > 0:
                visited[next_r][next_c] = visited[cur_r][cur_c] + 1
                q.append((next_r, next_c))

    return visited[dst_r][dst_c]


def go(cur_pos, dst_pos, history, history_list, visited, min_dist):
    if min_dist < len(history):
        return

    if cur_pos == dst_pos:
        history_list.append(history)
        return

    cur_r, cur_c = cur_pos
    for d in range(4):
        next_r, next_c = (cur_r + d8[d][0]) % N, (cur_c + d8[d][1]) % M

        if not visited[next_r][next_c] and board[next_r][next_c] > 0:
            visited[next_r][next_c] = True
            go((next_r, next_c), dst_pos, history + [d], history_list, visited, min_dist)
            visited[next_r][next_c] = False


def attack_with_lazer(src_pos, dst_pos, min_dist):
    pos_list = []

    history_list = []
    visited = [[False] * M for _ in range(N)]
    visited[src_pos[0]][src_pos[1]] = True
    go(src_pos, dst_pos, [], history_list, visited, min_dist)

    history_list.sort(key=lambda x: (len(x), x))
    if history_list:
        cur_r, cur_c = src_pos
        for d in history_list[0]:
            next_pos = ((cur_r + d8[d][0]) % N, (cur_c + d8[d][1]) % M)
            pos_list.append(next_pos)
            cur_r, cur_c = next_pos

    return pos_list


def attack_with_bomb(dst_pos):
    pos_list = [dst_pos]

    dst_r, dst_c = dst_pos
    for d in range(8):
        pos_list.append(((dst_r + d8[d][0]) % N, (dst_c + d8[d][1]) % M))

    return pos_list


def main():
    answer = 0

    for k in range(1, K + 1):
        turret_list = []
        for i in range(N):
            for j in range(M):
                if board[i][j] > 0:
                    turret_list.append(
                        (
                            i,
                            j,
                            board[i][j],
                            attack_time_list[i][j]
                        )
                    )

        if 1 >= len(turret_list):
            break

        src_turret = sorted(turret_list, key = lambda x: (x[2], -x[3], -(x[0] + x[1]), -x[1]))[0]
        dst_turret = sorted(turret_list, key = lambda x: (-x[2], x[3], x[0] + x[1], x[1]))[0]
        board[src_turret[0]][src_turret[1]] += N + M
        attack_time_list[src_turret[0]][src_turret[1]] = k

        src_pos = (src_turret[0], src_turret[1])
        dst_pos = (dst_turret[0], dst_turret[1])
        min_dist = get_min_dist(src_pos, dst_pos)
        target_pos_list = attack_with_bomb(dst_pos) if FALSE == min_dist else attack_with_lazer(src_pos, dst_pos, min_dist)

        for i in range(N):
            for j in range(M):
                cur_pos = (i, j)
                
                if cur_pos != src_pos:
                    if cur_pos ==    dst_pos:
                        board[i][j] -= board[src_pos[0]][src_pos[1]]
                    elif cur_pos in target_pos_list:
                        board[i][j] -= board[src_pos[0]][src_pos[1]] // 2
                    elif board[i][j] > 0:
                        board[i][j] += 1

    for i in range(N):
        for j in range(M):
            if board[i][j]:
                answer = max(answer, board[i][j])

    print(answer)

if __name__ == "__main__":
    main()