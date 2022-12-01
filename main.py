#Comp 472 MP2
#Author : Samuel Tardif
import rushHour as rh

#Reading from input file
filename = 'Sample/sample-input.txt'
lines = []
with open(filename) as file:
    for line in file:
        if line.strip():
            lines.append(line.strip())

#Parsing through file for problems
problems = {}
for i, line in enumerate(lines):
    print(line)
    if not (line.startswith('#')):
        problems.update({lines[i-1]:line})

#Checking problems to solve
print(problems)

#File output
with open('problems.txt', 'w') as f:
    f.write(str(problems))

state = "..A"
newState = rh.valet(state)
print(state)
print(newState)