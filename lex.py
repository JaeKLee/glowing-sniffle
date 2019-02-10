# Author: Jae Kyoung Lee (LJ)
import re
import regex

# Opening as read mode because all I need is to read for now
open_file = open("test_alan.txt", "r")

# testArray = open_file.readlines()
# print(len(testArray))
# print(testArray)

lineNumber = 1
programNumber = 1

# for each line in the test file
for line in open_file:
  # print(lineNumber)    
  print("Program ", programNumber)
  for character in line: 
    if re.search(regex.leftParen, character):
      print("Found left paren:  " , character , " in line " , lineNumber)
    elif re.search(regex.rightParen, character):
      print("Found right paren: " , character , " in line " , lineNumber)
    elif re.search(regex.eop, character):
      print("End of Program detected: ", character)
  programNumber+=1
  lineNumber+=1

