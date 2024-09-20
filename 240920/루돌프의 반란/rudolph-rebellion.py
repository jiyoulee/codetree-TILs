N, M, P, C, D = map(int, input().split())
rudolf_pos = tuple(map(int, input().split()))
santa_pos_list = [()] * (P + 1)
for _ in range(P):
    sid, r, c = map(int, input().split())
    santa_pos_list[sid] = (r, c)

board = [[0] * (N + 1) for _ in range(N + 1)]
board[rudolf_pos[0]][rudolf_pos[1]] = -1
for sid in range(1, P + 1):
    board[santa_pos_list[sid][0]][santa_pos_list[sid][1]] = sid
santa_stunned = [0] * (P + 1)
santa_dropped = [False] * (P + 1)
deltas = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def in_range(r, c):
    return 1 <= r <= N and 1 <= c <= N


def get_distance(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


def get_new_rudolf(rudolf_pos):
    cur_r, cur_c = rudolf_pos

    target_santa_pos_list = []
    for sid in range(1, P + 1):
        if not santa_dropped[sid]:
            santa_pos = santa_pos_list[sid]
            target_santa_pos_list.append(
                (
                    get_distance(rudolf_pos, santa_pos),
                    santa_pos
                )
            )
    target_santa_pos_list.sort(key=lambda x: (x[0], -x[1][0], -x[1][1]))
    result_santa_pos = target_santa_pos_list[0][1]

    target_rudolf_pos_list = []
    for d in range(8):
        next_rudolf_pos = (cur_r + deltas[d][0], cur_c + deltas[d][1])
        if in_range(next_rudolf_pos[0], next_rudolf_pos[1]):
            target_rudolf_pos_list.append(
                (
                    get_distance(next_rudolf_pos, result_santa_pos),
                    next_rudolf_pos,
                    d
                )
            )
    target_rudolf_pos_list.sort(key=lambda x: x[0])
    result_rudolf_pos, result_d = target_rudolf_pos_list[0][1], target_rudolf_pos_list[0][2]

    return result_rudolf_pos, result_d


def get_new_santa(santa_pos):
    result_santa, result_d = (-1, -1), -1

    (cur_r, cur_c), cur_d = santa_pos, get_distance(rudolf_pos, santa_pos)

    target_santa_pos_list = []
    for td in range(4):
        next_r, next_c = cur_r + deltas[td][0], cur_c + deltas[td][1]

        if in_range(next_r, next_c) and 0 >= board[next_r][next_c]:
            next_d = get_distance(rudolf_pos, (next_r, next_c))
            if next_d < cur_d:
                target_santa_pos_list.append(((next_r, next_c), next_d, td))
    target_santa_pos_list.sort(key=lambda x: (x[1], x[2]))

    if target_santa_pos_list:
        result_santa, result_d = target_santa_pos_list[0][0], target_santa_pos_list[0][2]

    return result_santa, result_d


def create_santa_chain_reaction(init_sid, strength, d):
    global board

    cur_sid = init_sid
    cur_r = santa_pos_list[init_sid][0] + strength * deltas[d][0]
    cur_c = santa_pos_list[init_sid][1] + strength * deltas[d][1]

    while True:
        if not in_range(cur_r, cur_c):
            santa_dropped[cur_sid] = True
            break

        if not board[cur_r][cur_c]:
            santa_pos_list[cur_sid] = (cur_r, cur_c)
            board[cur_r][cur_c] = cur_sid
            break

        next_sid = board[cur_r][cur_c]

        santa_pos_list[cur_sid] = (cur_r, cur_c)
        board[cur_r][cur_c] = cur_sid

        cur_sid = next_sid
        cur_r = santa_pos_list[next_sid][0] + deltas[d][0]
        cur_c = santa_pos_list[next_sid][1] + deltas[d][1]


def main():
    global rudolf_pos, santa_pos_list, santa_stunned, santa_dropped

    answer = [0] * (P + 1)

    for m in range(1, M + 1):
        if P == sum(santa_dropped):
            break

        board[rudolf_pos[0]][rudolf_pos[1]] = 0
        rudolf_pos, d = get_new_rudolf(rudolf_pos)

        init_sid = board[rudolf_pos[0]][rudolf_pos[1]]
        if init_sid:
            answer[init_sid] += C
            santa_stunned[init_sid] = m + 1
            create_santa_chain_reaction(init_sid, C, d)

        board[rudolf_pos[0]][rudolf_pos[1]] = -1

        for sid in range(1, P + 1):
            if not santa_dropped[sid] and m > santa_stunned[sid]:
                santa_pos = santa_pos_list[sid]
                new_santa_pos, d = get_new_santa(santa_pos)

                if -1 == d:
                    continue

                board[santa_pos[0]][santa_pos[1]] = 0
                santa_pos_list[sid] = new_santa_pos
                santa_pos = santa_pos_list[sid]

                init_sid = board[santa_pos[0]][santa_pos[1]]
                if -1 == init_sid:
                    answer[sid] += D
                    santa_stunned[sid] = m + 1
                    d = (d + 2) % 4
                    create_santa_chain_reaction(sid, D, d)
                else:
                    board[santa_pos[0]][santa_pos[1]] = sid

        for sid in range(1, P + 1):
            if not santa_dropped[sid]:
                answer[sid] += 1

    for i in range(1, P + 1):
        print(answer[i], end=" ")


if __name__ == "__main__":
    main()