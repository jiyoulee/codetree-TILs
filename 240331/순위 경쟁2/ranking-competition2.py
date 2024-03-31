# Preset.
input_list = []
student_type = ""
student_score = 0
answer = 0
score = [0] * 2
state = "AB"
new_state = ""

# Go.
T = int(input())

for test_case in range(1, T + 1):
    # Input
    input_list = input().split()
    student_type = input_list[0]
    student_score = int(input_list[1])

    # Compute
    if "A" == student_type:
        score[0] += student_score
    else:
        score[1] += student_score

    if score[0] > score[1]:
        new_state = "A"
    elif score[0] < score[1]:
        new_state = "B"
    else:
        new_state = "AB"

    if new_state != state:
        answer += 1
    
    # Reset.
    state = new_state

# Output.
print(answer)