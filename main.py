#Comp 472 MP2
#Author : Samuel Tardif
import rushHour as rh
import searchAlgo as sa

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



for name in problems:
#   sa.searchUCS(name, problems[name])
#   sa.searchGBFS(name, problems[name])
    sa.searchA(name, problems[name])


