# Input
answer = -1
n = int(input())
number_list = sorted(list(map(int, input().split())))

# Compute
idx = -1
for i in range(len(number_list)):
    if number_list[0] != number_list[i]:
        idx = i
        break

if -1 != idx:
    if len(number_list) - 1 == idx:
        answer = idx
    elif number_list[idx + 1] != number_list[idx]:
        answer = idx

print(answer + 1)