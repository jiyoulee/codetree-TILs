N, M, P, C, D = map(int, input().split())
board = [[0] * (N + 1) for _ in range(N + 1)]

rudolf = tuple(map(int, input().split()))
board[rudolf[0]][rudolf[1]] = -1

santas = [(0, 0)] * (P + 1)
for _ in range(P):
    idx, r, c = map(int, input().split())
    santas[idx] = (r, c)
    board[r][c] = idx
santa_stunned = [0] * (P + 1)
santa_dropped = [False] * (P + 1)

deltas = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def in_range(r, c):
    return 1 <= r <= N and 1 <= c <= N


def get_distance(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


def get_next_rudolf(cur_rudolf):
    cur_r, cur_c = cur_rudolf

    targets = []
    for idx in range(1, P + 1):
        if not santa_dropped[idx]:
            santa_r, santa_c = santas[idx]
            targets.append((get_distance(rudolf, (santa_r, santa_c)), santa_r, santa_c))
    targets.sort(key=lambda x: (x[0], -x[1], -x[2]))
    target_santa = (targets[0][1], targets[0][2])

    targets = []
    for next_d in range(8):
        next_r, next_c = cur_r + deltas[next_d][0], cur_c + deltas[next_d][1]
        if in_range(next_r, next_c):
            targets.append((get_distance((next_r, next_c), target_santa), next_r, next_c, next_d))
    targets.sort(key=lambda x: x[0])
    result_rudolf, result_d = (targets[0][1], targets[0][2]), targets[0][3]

    return result_rudolf, result_d


def get_new_santa(cur_santa):
    result_santa, result_d = (-1, -1), -1

    (cur_r, cur_c), cur_dist = cur_santa, get_distance(rudolf, cur_santa)

    targets = []
    for next_d in range(4):
        next_r, next_c = cur_r + deltas[next_d][0], cur_c + deltas[next_d][1]
        if in_range(next_r, next_c) and 0 >= board[next_r][next_c]:
            next_dist = get_distance(rudolf, (next_r, next_c))
            if next_dist < cur_dist:
                targets.append(((next_r, next_c), next_dist, next_d))
    if targets:
        targets.sort(key=lambda x: (x[1], x[2]))
        result_santa, result_d = targets[0][0], targets[0][2]

    return result_santa, result_d


def main():
    global rudolf, santas, santa_stunned, santa_dropped

    answer = [0] * (P + 1)

    for m in range(1, M + 1):
        if P == sum(santa_dropped):
            break
        
        board[rudolf[0]][rudolf[1]] = 0
        new_rudolf, d = get_next_rudolf(rudolf)

        if board[new_rudolf[0]][new_rudolf[1]]:
            collide_idx = board[new_rudolf[0]][new_rudolf[1]]
            answer[collide_idx] += C
            santa_stunned[collide_idx] = m + 1
            new_santa = (santas[collide_idx][0] + C * deltas[d][0], santas[collide_idx][1] + C * deltas[d][1])

            if not in_range(new_santa[0], new_santa[1]):
                santa_dropped[collide_idx] = True
            else:
                targets = []
                cur_r, cur_c = new_santa[0], new_santa[1]
                while in_range(cur_r, cur_c) and 0 < board[cur_r][cur_c]:
                    targets.append((cur_r, cur_c))
                    cur_r += deltas[d][0]
                    cur_c += deltas[d][1]

                for (cur_r, cur_c) in targets[::-1]:
                    cur_idx = board[cur_r][cur_c]
                    new_r, new_c = cur_r + deltas[d][0], cur_c + deltas[d][1]

                    if not in_range(new_r, new_c):
                        santa_dropped[cur_idx] = True
                        continue

                    santas[cur_idx] = (new_r, new_c)
                    board[new_r][new_c] = cur_idx

                santas[collide_idx] = new_santa
                board[santas[collide_idx][0]][santas[collide_idx][1]] = collide_idx

        rudolf = new_rudolf
        board[new_rudolf[0]][new_rudolf[1]] = -1

        for idx in range(1, P + 1):
            if not santa_dropped[idx] and m > santa_stunned[idx]:
                new_santa_1, d = get_new_santa(santas[idx])

                if -1 == d:
                    continue

                board[santas[idx][0]][santas[idx][1]] = 0

                if -1 == board[new_santa_1[0]][new_santa_1[1]]:
                    answer[idx] += D
                    santa_stunned[idx] = m + 1
                    d = (d + 2) % 4
                    new_santa_2 = (new_santa_1[0] + D * deltas[d][0], new_santa_1[1] + D * deltas[d][1])

                    if not in_range(new_santa_2[0], new_santa_2[1]):
                        santa_dropped[idx] = True
                    else:
                        targets = []
                        cur_r, cur_c = new_santa_2[0], new_santa_2[1]
                        while in_range(cur_r, cur_c) and 0 < board[cur_r][cur_c]:
                            targets.append((cur_r, cur_c))
                            cur_r += deltas[d][0]
                            cur_c += deltas[d][1]

                        for (cur_r, cur_c) in targets[::-1]:
                            cur_idx = board[cur_r][cur_c]
                            new_r, new_c = cur_r + deltas[d][0], cur_c + deltas[d][1]

                            if not in_range(new_r, new_c):
                                santa_dropped[cur_idx] = True
                                continue

                            santas[cur_idx] = (new_r, new_c)
                            board[new_r][new_c] = cur_idx

                        santas[idx] = new_santa_2
                        board[new_santa_2[0]][new_santa_2[1]] = idx
                else:
                    santas[idx] = new_santa_1
                    board[new_santa_1[0]][new_santa_1[1]] = idx

        for idx in range(1, P + 1):
            if not santa_dropped[idx]:
                answer[idx] += 1

    for i in range(1, P + 1):
        print(answer[i], end=" ")


if __name__ == "__main__":
    main()