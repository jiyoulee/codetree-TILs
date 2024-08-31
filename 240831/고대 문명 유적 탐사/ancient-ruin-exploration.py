from collections import deque

N_large = 5
N_small = 3


class Board:
    def __init__(self):
        self.a = [[0] * N_large for _ in range(N_large)]


    def in_range(self, y, x):
        return 0 <= y < N_large and 0 <= x < N_large


    def rotate(self, sy, sx, cnt):
        result = Board()
        result.a = [row[:] for row in self.a]
        for _ in range(cnt):
            tmp = result.a[sy + 0][sx + 2]
            result.a[sy + 0][sx + 2] = result.a[sy + 0][sx + 0]
            result.a[sy + 0][sx + 0] = result.a[sy + 2][sx + 0]
            result.a[sy + 2][sx + 0] = result.a[sy + 2][sx + 2]
            result.a[sy + 2][sx + 2] = tmp

            tmp = result.a[sy + 1][sx + 2]
            result.a[sy + 1][sx + 2] = result.a[sy + 0][sx + 1]
            result.a[sy + 0][sx + 1] = result.a[sy + 1][sx + 0]
            result.a[sy + 1][sx + 0] = result.a[sy + 2][sx + 1]
            result.a[sy + 2][sx + 1] = tmp

        return result


    def cal_score(self):
        score = 0
        visit = [[False] * N_large for _ in range(N_large)]
        dy, dx = [0, 1, 0, -1], [1, 0, -1, 0]

        for i in range(N_large):
            for j in range(N_large):
                if not visit[i][j]:
                    q, trace = deque([(i, j)]), deque([(i, j)])
                    visit[i][j] = True

                    while q:
                        cur = q.popleft()

                        for k in range(4):
                            ny, nx = cur[0] + dy[k], cur[1] + dx[k]
                            if self.in_range(ny, nx) and self.a[ny][nx] == self.a[cur[0]][cur[1]] and not visit[ny][nx]:
                                q.append((ny, nx))
                                trace.append((ny, nx))
                                visit[ny][nx] = True

                    if len(trace) >= 3:
                        score += len(trace)

                        while trace:
                            t = trace.popleft()
                            self.a[t[0]][t[1]] = 0

        return score


    def fill(self, que):
        for j in range(N_large):
            for i in reversed(range(N_large)):
                if self.a[i][j] == 0:
                    self.a[i][j] = que.popleft()


def main():
    K, M = map(int, input().split())

    board = Board()
    for i in range(N_large):
        board.a[i] = list(map(int, input().split()))

    q = deque()
    for t in list(map(int, input().split())):
        q.append(t)

    for _ in range(K):
        maxScore = 0
        maxScoreBoard = None

        for cnt in range(1, 4):
            for sx in range(N_large - N_small + 1):
                for sy in range(N_large - N_small + 1):
                    rotated = board.rotate(sy, sx, cnt)
                    score = rotated.cal_score()

                    if maxScore < score:
                        maxScore = score
                        maxScoreBoard = rotated

        if maxScoreBoard is None:
            break

        board = maxScoreBoard

        while True:
            board.fill(q)
            newScore = board.cal_score()

            if newScore == 0:
                break

            maxScore += newScore

        print(maxScore, end=" ")


if __name__ == "__main__":
    main()