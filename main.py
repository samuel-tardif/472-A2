#Comp 472 MP2
#Author : Samuel Tardif
import rushHour as rh
import searchAlgo as sa

#Reading from input file
filename = 'Sample/sample-input.txt'
filename2 = "randomproblems.txt"

#CHANGE FILENAME BELOW TO CHANGE WHAT PROBLEMS ARE SOLVED
lines = []
with open(filename2) as file:
    for line in file:
        if line.strip():
            lines.append(line.strip())

#Parsing through file for problems
problems = {}
for i, line in enumerate(lines):
    print(line)
    if not (line.startswith('#')):
        problems.update({lines[i-1]:line})


#UNCOMMENT TO RUN search algos
for name in problems:
    sa.searchUCS(name, problems[name])
    sa.searchGBFS(name, problems[name])
    sa.searchA(name, problems[name])

#Generating random problems
#UNCOMMENT TO GENERATE NEW PROBLEMS
#f = open("randomproblems.txt", "w")
#for i in range(0,50):
#    randomProblem = rh.generateRandomProblem()
#    name = str(i+1)
#    f.write("#"+name+"\n"+randomProblem+"\n\n")



