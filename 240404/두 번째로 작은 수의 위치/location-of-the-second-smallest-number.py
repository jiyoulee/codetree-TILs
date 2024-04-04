# Define
answer = -2
n = int(input())
number_list = list(map(int, input().split()))
sorted_number_list = sorted(number_list)

# Compute
val = sorted_number_list[0]
for number in sorted_number_list:
    if number != val:
        val = number
        break

if sorted_number_list[0] != val and 1 == number_list.count(val):
    idx = -1
    for i in range(len(number_list)):
        if number_list[i] == val:
            answer = i
            break

# Output
print(answer + 1)