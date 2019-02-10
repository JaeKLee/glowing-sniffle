# Author: Jae Kyoung Lee (LJ)
import re
# Importing list of our grammar regex from regex.py
import regex

# Opening as read mode to read the test files
open_file = open("test_alan.txt", "r")

listFile = open_file.read().split(" ")
# print(listFile)

lineNumber = 1
programNumber = 1
# for line in listFile: 
#   print(line)
#   if re.compile(regex.leftParen).match(line):
#     print("Found token left paren:    " , line , " in line " , lineNumber)
print(listFile)


for line in listFile:
  # print("Program ", programNumber)
  # for character in line: 
    # print(character)
  if re.search(regex.leftParen, line):
    print("In line " , lineNumber, "found token left paren:    " , line)
  elif re.search(regex.rightParen, line):
    print("Found token right paren:   " , line , " in line " , lineNumber)
  elif re.search(regex.character, line):
    print("character: ", line , " in line " , lineNumber)
  elif re.compile(regex.typeInt).findall(line):
    print("Found token type Integer:  " , line , " in line " , lineNumber)
  elif re.search(regex.typeString, line):
    print("Found token type String:   " , line , " in line " , lineNumber)
  elif re.search(regex.typeboolean, line):
    print("Found token type Boolean:  " , line , " in line " , lineNumber)
  elif re.search(regex.equal, line):
    print("Found token equal:         " , line , " in line " , lineNumber)
  elif re.search(regex.notEqual, line):
    print("Found token not Equal:     " , line , " in line " , lineNumber)
  elif re.search(regex.boolFalse, line):
    print("Found token boolean false: " , line , " in line " , lineNumber)
  elif re.search(regex.boolTrue, line):
    print("Found token boolean True:  " , line , " in line " , lineNumber)
  elif re.search(regex.assign, line):
    print("Found token assignment:    " , line , " in line " , lineNumber)
  # elif re.compile(regex.eop).match(line):
  #   print("End of Program detected:  ", line, "\n")  
  #   programNumber+=1
  lineNumber+=1

