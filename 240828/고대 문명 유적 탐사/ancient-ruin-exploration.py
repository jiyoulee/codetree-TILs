from collections import deque

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

num_iters, num_spares = map(int, input().split())
g1 = [[x for x in map(int, input().split())] for _ in range(5)]
g2 = []
spares = [x for x in map(int, input().split())]
spares_idx = -1


def print_global_vars():
    print("g1")
    for r in range(5):
        print(g1[r])
    print("-" * 20)
    print("g2")
    for r in range(5):
        print(g2[r])
    print("-" * 20)
    print("spares")
    print(spares)
    print("-" * 20)


def set_position(r: int, c: int, d: int):
    """
    :param r: center x coordinate
    :param c: center y coordinate
    :param d: number of times to rotate
    :return:
    """
    global g1, g2

    g2 = [x[:] for x in g1]
    g3 = [[g1[i][j] for j in range(c - 1, c + 2)] for i in range(r - 1, r + 2)]

    for _ in range(d):
        g3 = [[g3[j][i] for j in range(3)] for i in range(3)]
        g3 = [g3[i][::-1] for i in range(3)]

    for cr in range(3):
        for cc in range(3):
            g2[r - 1 + cr][c - 1 + cc] = g3[cr][cc]


def get_valid_connections(r: int, c: int):
    """
    :param r: center x-coordinate
    :param c: center y-coordinate
    :return:
    """
    global g2

    connections = []
    visited = [[False] * 5 for _ in range(5)]

    for lr in range(r - 1, r + 2):
        for lc in range(c - 1, c + 2):
            if not visited[lr][lc]:  # if current square has not been visited
                val = g2[lr][lc]  # value of current square
                tmp_connections = []  # connections related to current square

                q = deque()

                visited[lr][lc] = True
                q.append((lr, lc))
                tmp_connections.append((lr, lc))

                while q:
                    cr, cc = q.pop()

                    for d in range(4):
                        nr = cr + dr[d]
                        nc = cc + dc[d]

                        if 0 <= nr < 5 and 0 <= nc < 5 and not visited[nr][nc] and g2[nr][nc] == val:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                            tmp_connections.append((nr, nc))

                if len(tmp_connections) >= 3:
                    connections.extend(tmp_connections)

    return connections


def search():
    """
    :return: optimum case
    """
    cases = []

    for r in range(1, 4):
        for c in range(1, 4):
            for d in range(1, 4):
                set_position(r, c, d)
                connections = get_valid_connections(r, c)
                cases.append((r, c, d, len(connections)))

    sorted_cases = sorted(cases, key=lambda x: (-x[3], x[2], x[1], x[0]))

    return sorted_cases[0]


def cleanse(r: int, c: int):
    global g2, spares, spares_idx

    val = 0

    while True:
        connections = get_valid_connections(r, c)
        if not connections:
            break

        val += len(connections)

        sorted_connections = sorted(connections, key=lambda x: (x[1], -x[0]))
        for connection in sorted_connections:
            cr, cc = connection
            spares_idx += 1
            g2[cr][cc] = spares[spares_idx]

    return val


def main():
    global g1, g2

    answer = ""

    for _ in range(num_iters):
        r, c, d, v = search()

        if not v:
            break

        set_position(r, c, d)

        val = cleanse(r, c)

        answer = "".join([answer, f"{str(val)} "])

        g1 = [x[:] for x in g2]

    print(answer)


if __name__ == "__main__":
    main()