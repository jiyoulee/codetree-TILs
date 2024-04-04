# Define
answer = 0
verbose = True
n = int(input())
prev_state = "ABC"
cur_state = ""
a_score = 0
b_score = 0
c_score = 0

# Compute
for _ in range(n):
    c, s = input().split()
    s = int(s)

    if "A" == c:
        a_score += s
    elif "B" == c:
        b_score += s
    elif "C" == c:
        c_score += s

    if a_score > b_score and a_score > c_score:
        cur_state = "A"
    elif b_score > a_score and b_score > c_score:
        cur_state = "B"
    elif c_score > a_score and c_score > b_score:
        cur_state = "C"
    elif a_score == b_score and a_score > c_score:
        cur_state = "AB"
    elif a_score == c_score and a_score > b_score:
        cur_state = "AC"
    elif b_score == c_score and b_score > a_score:
        cur_state = "BC"
    else:
        cur_state = "ABC"

    if prev_state != cur_state:
        answer += 1

    prev_state = cur_state

# Output
print(answer)