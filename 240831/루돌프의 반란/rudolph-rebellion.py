d8 = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

N, M, P, C, D = map(int, input().split())
board = [[0] * N for _ in range(N)]

rudolf = tuple(map(lambda x: x - 1, map(int, input().split())))
board[rudolf[0]][rudolf[1]] = -1

santas = [tuple()] * (P + 1)
for _ in range(P):
    n, r, c = map(int, input().split())
    santas[n] = tuple([r - 1, c - 1])
    board[santas[n][0]][santas[n][1]] = n
status = [1] * (P + 1)
answer = [0] * (P + 1)


def in_range(obj: tuple):
    return 0 <= obj[0] < N and 0 <= obj[1] < N


def get_distance(obj1: tuple, obj2: tuple):
    return (obj1[0] - obj2[0]) ** 2 + (obj1[1] - obj2[1]) ** 2


def recursively_move_santas(id: int, d: int):
    global board, santas

    santa = santas[id]

    if not in_range(santa):
        status[id] = 0
        return

    prev_id = board[santa[0]][santa[1]]
    board[santa[0]][santa[1]] = id

    if prev_id > 0:
        new_santa = tuple([santa[0] + d8[d][0], santa[1] + d8[d][1]])
        santas[prev_id] = new_santa
        recursively_move_santas(prev_id, d)


def move_rudolf(M: int):
    global board, rudolf, santas, status, C

    a = []
    for i in range(1, P + 1):
        if status[i]:
            a.append(santas[i] + tuple([get_distance(rudolf, santas[i])]))
    sorted_a = sorted(a, key=lambda x: (x[2], -x[0], -x[1]))
    min_santa = tuple([sorted_a[0][0], sorted_a[0][1]])

    a.clear()
    for d in range(8):
        new_rudolf = tuple([rudolf[0] + d8[d][0], rudolf[1] + d8[d][1]])
        a.append(new_rudolf + tuple([d, get_distance(new_rudolf, min_santa)]))
    sorted_a = sorted(a, key=lambda x: x[3])
    new_rudolf, d = tuple([sorted_a[0][0], sorted_a[0][1]]), sorted_a[0][2]

    board[rudolf[0]][rudolf[1]] = 0
    prev_id = board[new_rudolf[0]][new_rudolf[1]]
    rudolf = new_rudolf
    board[rudolf[0]][rudolf[1]] = -1

    if prev_id > 0:
        answer[prev_id] += C
        status[prev_id] = M + 2
        prev_santa = santas[prev_id]
        new_santa = tuple([prev_santa[0] + C * d8[d][0], prev_santa[1] + C * d8[d][1]])
        santas[prev_id] = new_santa
        recursively_move_santas(prev_id, d)


def move_santa(id: int, m: int):
    global santas, board, rudolf, answer, status, D

    a = []
    santa = santas[id]
    
    dist = get_distance(rudolf, santa)
    for d in range(4):
        new_santa = tuple([santa[0] + d8[d][0], santa[1] + d8[d][1]])
        new_dist = get_distance(rudolf, new_santa)
        if in_range(new_santa) and board[new_santa[0]][new_santa[1]] <= 0 and new_dist < dist:
            a.append(new_santa + tuple([d, new_dist]))
    sorted_a = sorted(a, key=lambda x: x[3])

    if not sorted_a:
        return

    board[santa[0]][santa[1]] = 0
    new_santa, d = tuple([sorted_a[0][0], sorted_a[0][1]]), sorted_a[0][2]
    prev_id = board[new_santa[0]][new_santa[1]]

    if prev_id == -1:
        answer[id] += D
        status[id] = m + 2
        new_santa = tuple([new_santa[0] + D * d8[(d + 2) % 4][0], new_santa[1] + D * d8[(d + 2) % 4][1]])
        santas[id] = new_santa
        recursively_move_santas(id, (d + 2) % 4)
    else:
        board[new_santa[0]][new_santa[1]] = id
        santas[id] = new_santa


def main():
    global M, P, status, answer, rudolf

    for m in range(1, M + 1):

        if not sum(status):
            break

        move_rudolf(m)

        for i in range(1, P + 1):
            if status[i] == m:
                move_santa(i, m)

        for i in range(1, P + 1):
            if status[i]:
                answer[i] += 1
            if status[i] == m:
                status[i] += 1

    for i in range(1, P + 1):
        print(answer[i], end=" ")


if __name__ == "__main__":
    main()