# Author: Jae Kyoung Lee (LJ)
import re
# Importing list of our grammar regex from regex.py
import regex

# Opening as read mode to read the test files
open_file = open("test_alan.txt", "r")

listFile = list(open_file.read())
# print(listFile)

lineNumber = 1
programNumber = 1
# for line in listFile: 
#   print(line)
#   if re.compile(regex.leftParen).match(line):
#     print("Found token left paren:    " , line , " in line " , lineNumber)
print(listFile)
wordList = []
for line in listFile:
  # print("Program ", programNumber)
  # for character in line: 
    # print(character)
  if re.search(regex.leftParen, line):
    print("Found token left paren:    " , line,   " in line " , lineNumber)
  elif re.search(regex.rightParen, line):
    print("Found token right paren:   " , line ,  " in line " , lineNumber)
# First it detects for any characters and depending on what it finds, it will output different results
  elif re.search(regex.character, line):
    if re.search(r"i", line):
      print("character: ", line , " in line " , lineNumber)
    # if re.search(regex.typeInt, line): # Integer
    #   print("Found token type Integer:  " , line , " in line " , lineNumber)
    # elif re.search(regex.typeString, line): # String
    #   print("Found token type String:   " , line , " in line " , lineNumber)
    # elif re.search(regex.typeboolean, line): # Boolean
    #   print("Found token type Boolean:  " , line , " in line " , lineNumber)
    # elif re.search(regex.boolFalse, line): # False
    #   print("Found token boolean false: " , line , " in line " , lineNumber)
    # elif re.search(regex.boolTrue, line): # True
    #   print("Found token boolean True:  " , line , " in line " , lineNumber)
    # else: # if none were found, then print as character 
    #   print("character: ", line , " in line " , lineNumber)
      # newList = list(line) # This splits characters into one
      # indexCounter = 0
      # lastIndex = len(newList)
      # # This is to remove the l
      # if indexCounter < len(newList):      
      #   if newList[lastIndex-1] == "\n":
      #     lineNumber+=1
      #     del newList[lastIndex-1]
      #     while indexCounter < len(newList):
      #       print("character: ", newList[indexCounter] , " in line " , lineNumber)
      #       indexCounter+=1
  # End of character elif
  elif re.search(regex.equal, line): 
    print("Found token equal:         " , line , " in line " , lineNumber)
  elif re.search(regex.notEqual, line):
    print("Found token not Equal:     " , line , " in line " , lineNumber)
  elif re.search(regex.assign, line):
    print("Found token assignment:    " , line , " in line " , lineNumber)
  elif re.match(r"\n", line):
    lineNumber+=1
  elif re.compile(regex.eop).search(line):
    print("End of Program detected:  ", line, "\n")  
    programNumber+=1
