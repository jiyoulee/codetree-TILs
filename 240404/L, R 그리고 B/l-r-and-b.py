# Define
answer = 0
num_rows = 10
num_cols = 10
grid = [list(input().split()) for _ in range(num_rows)]
lr = 0
lc = 0
rr = 0
rc = 0
br = 0
bc = 0
verbose = False

# Compute
for i in range(num_rows):
    for j in range(num_cols):
        if "L" == grid[i][0][j]:
            lr = i
            lc = j
        if "R" == grid[i][0][j]:
            rr = i
            rc = j
        if "B" == grid[i][0][j]:
            br = i
            bc = j

if lr != br and lc != bc:
    answer = abs(lr - br) + abs(lc - bc) - 1
elif lr == br:
    answer = abs(lc - bc) - 1
    if (lc < rc and bc > rc) or (bc < rc and lc > rc):
        answer += 2
elif lc == bc:
    if verbose:
        print(lc, rc, bc)
    answer = abs(lr - br) - 1
    if (lr < rr and br > rr) or (br < rr and lr > rr):
        answer += 2

# Output
print(answer)