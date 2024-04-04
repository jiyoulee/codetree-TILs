# Define
answer = 0
num_rows = 10
num_cols = 10
grid = [list(input().split()) for _ in range(num_rows)]
lr = 0
lc = 0
br = 0
bc = 0

# Compute
for i in range(num_rows):
    for j in range(num_cols):
        if "L" == grid[i][0][j]:
            lr = i
            lc = j
        if "B" == grid[i][0][j]:
            br = i
            bc = j

if lr != br and lc != bc:
    answer = abs(lr - br) + abs(lc - bc) - 1
elif lr == br:
    answer = abs(lc - bc) - 1
elif lc == bc:
    answer = abs(lr - br) - 1

# Output
print(answer)