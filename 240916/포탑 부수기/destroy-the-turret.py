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


def in_range(r: int, c: int):
    return 0 <= r < N and 0 <= c < M


def go(cur_pos, dst_pos, history, history_list, visited):
    if cur_pos == dst_pos:
        history_list.append(history)
        return

    cur_r, cur_c = cur_pos

    for d in range(4):
        next_r, next_c = (cur_r + d8[d][0], cur_c + d8[d][1])

        if in_range(next_r, next_c) and len(history) + 1 < visited[next_r][next_c] and board[next_r][next_c]:
            tmp = visited[next_r][next_c]
            visited[next_r][next_c] = len(history) + 1
            go((next_r, next_c), dst_pos, history + [d], history_list, visited)
            visited[next_r][next_c] = tmp


def attack_with_lazer(src_pos, dst_pos):
    pos_list = []

    history_list = []
    visited = [[987654321] * M for _ in range(N)]
    visited[src_pos[0]][src_pos[1]] = 0

    go(src_pos, dst_pos, [], history_list, visited)

    history_list.sort(key=lambda x: (len(x), x))
    if history_list:
        cur_pos = src_pos
        for d in history_list[0]:
            next_pos = (cur_pos[0] + d8[d][0], cur_pos[1] + d8[d][1])
            pos_list.append(next_pos)
            cur_pos = next_pos

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
                if board[i][j]:
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

        src_turret = sorted(turret_list, key = lambda x: (x[2], -x[3], -(x[0] + x[1]), -x[0]))[0]
        dst_turret = sorted(turret_list, key = lambda x: (-x[2], x[3], x[0] + x[1], x[0]))[0]
        board[src_turret[0]][src_turret[1]] += N + M
        attack_time_list[src_turret[0]][src_turret[1]] = k

        src_pos = (src_turret[0], src_turret[1])
        dst_pos = (dst_turret[0], dst_turret[1])
        target_pos_list = attack_with_lazer(src_pos, dst_pos)
        if not target_pos_list:
            target_pos_list = attack_with_bomb(dst_pos)

        for i in range(N):
            for j in range(M):
                cur_pos = (i, j)
                
                if board[i][j] and cur_pos != src_pos:
                    if cur_pos == dst_pos:
                        board[i][j] -= board[src_pos[0]][src_pos[1]]
                    elif cur_pos in target_pos_list:
                        board[i][j] -= board[src_pos[0]][src_pos[1]] // 2
                    else:
                        board[i][j] += 1

    for i in range(N):
        for j in range(M):
            if board[i][j]:
                answer = max(answer, board[i][j])

    print(answer)

if __name__ == "__main__":
    main()