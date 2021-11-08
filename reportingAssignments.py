#!/user/bin/python

import json
import sys

stack = []
data = []
arguments = []

arguments = sys.argv
file = arguments[1]
output = arguments[2]

while True:
    try:
        f = open(file,'r',encoding='ISO-8859-1')
        break
    except IOError:
        input("Error in file opening, please type correct filename\n")
        print(file)
        sys.exit()
lineDict = {}
highestIndentation = 0
for line in f:
    x = 0
    while(x < len(line)):
        #function call in a new stack
        if(line[x] == '-' and x+1 < len(line) and
        line[x+1] == '>'):
            y = x+1
            string = ""
            while(y<len(line) and line[y] != '('):
                string = string + line[y]
                y = y + 1
            if(x > highestIndentation):
                highestIndentation = x
                stack.append(string)
            else:
                highestIndentation = x
                # print("before we pop at function call")
                # counter = 0
                # while(counter < len(stack)):
                #     print(stack[counter])
                #     counter = counter + 1
                stack.pop()
                stack.append(string)
                # print("after we pop and add at function call")
                # counter = 0
                # while(counter < len(stack)):
                #     print(stack[counter])
                #     counter = counter + 1
            break
        if(line[x] == '>' and x < highestIndentation):
            highestIndentation = x - 1
            stack.pop()
            break
        if(line[x] == '=' and x+1 < len(line) and x > 0 and line[x-1] != '>' 
        and line[x+1]== '>' and "alert(" in line):
            y = x + 4
            variableName = ""
            while(line[y] != ' '):
                variableName = variableName + line[y]
                y = y + 1
            while(line[y] != "="):
                y = y + 1
            y = y + 2
            newString = ""
            while(y < len(line)):
                newString = newString + line[y]
                y = y + 1
            # print("this is new String: " + newString)
            splitString = newString.split("/var/www/html/")
            # print("this is splitString: " + splitString[0])
            myDictionary = {}
            myDictionary['function_name'] = stack[-1][2:]
            myDictionary['variable_name'] = variableName
            myDictionary['value'] = splitString[0]
            myDictionary['file_name'] = "/var/www/html/" + (splitString[1][:len(splitString[1]) - 1])
            data.append(myDictionary)
            # print("The function: " + stack[-1] + " line: " + line)
            break
        if(line[x] == '=' or line[x] == '-' or line[x] == '>'):
            break
        x = x + 1
with open(output+'.json', 'w') as file:
    file.write(json.dumps(data))
# print('Finished')
f.close()
