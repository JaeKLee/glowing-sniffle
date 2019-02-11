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
indexCounter = 0
nextIndex = indexCounter+1
empty = "" # To improve code readability
errorCounter = 0
warningCounter = 0
print(listFile)
emptyList = []

while indexCounter < len(listFile):
  if re.search(regex.leftParen, listFile[indexCounter]):
    print("Found token left paren:    " , listFile[indexCounter],   " in line " , lineNumber)
  elif re.search(regex.rightParen, listFile[indexCounter]):
    print("Found token right paren:   " , listFile[indexCounter] ,  " in line " , lineNumber)

# First it detects for any characters and depending on what it finds, it will output different results
  elif re.search(regex.character, listFile[indexCounter]):
    if re.search(r"i", listFile[indexCounter]):
      if indexCounter+1 < len(listFile): # To avoid index out of range
        indexCounter+=1 
        if re.search(r"f", listFile[indexCounter]):
          print("Found token IF : if in line " , lineNumber)
          indexCounter+=1
        elif re.search(r"n", listFile[indexCounter]):
          if indexCounter+1 < len(listFile):
            indexCounter+=1
            if re.search(r"t", listFile[indexCounter]):
              print("Found token INT : int in line " , lineNumber)
              indexCounter+=1
    elif re.search(r"w", listFile[indexCounter]):
      if indexCounter+4 < len(listFile):
        indexCounter+=1
        if re.search(r"h", listFile[indexCounter]) and re.search(r"i", listFile[indexCounter+1]) and re.search(r"l", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]):
          print("Found token WHILE : while in line " ,  lineNumber)
    elif re.search(r"p", listFile[indexCounter]):
      if indexCounter+4 < len(listFile):
        indexCounter+=1
        if re.search(r"r", listFile[indexCounter]) and re.search(r"i", listFile[indexCounter+1]) and re.search(r"n", listFile[indexCounter+2]) and re.search(r"t", listFile[indexCounter+3]):
          print("Found token PRINT : print in line " ,  lineNumber)
    elif re.search(r"b", listFile[indexCounter]):
      if indexCounter+6 < len(listFile):
        indexCounter+=1
        if re.search(r"o", listFile[indexCounter]) and re.search(r"o", listFile[indexCounter+1]) and re.search(r"l", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]) and re.search(r"a", listFile[indexCounter+4]) and re.search(r"n", listFile[indexCounter+5]):
          print("Found token BOOLEAN : boolean in line " ,  lineNumber)
    elif re.search(r"f", listFile[indexCounter]):
      if indexCounter+4 < len(listFile):
        indexCounter+=1
        if re.search(r"a", listFile[indexCounter]) and re.search(r"l", listFile[indexCounter+1]) and re.search(r"s", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]):
          print("Found token FALSE : false in line " ,  lineNumber)
    elif re.search(r"t", listFile[indexCounter]):
      if indexCounter+3 < len(listFile):
        indexCounter+=1
        if re.search(r"r", listFile[indexCounter]) and re.search(r"u", listFile[indexCounter+1]) and re.search(r"e", listFile[indexCounter+2]):
          print("Found token TRUE : true in line " ,  lineNumber)
    # End of big word if statement
  # elif re.search(regex.startQuote, listFile[indexCounter]):
    
  elif re.search(regex.equal, listFile[indexCounter]): 
    print("Found token equal:         " , listFile[indexCounter] , " in line " , lineNumber)
  elif re.search(regex.notEqual, listFile[indexCounter]):
    print("Found token not Equal:     " , listFile[indexCounter] , " in line " , lineNumber)
  elif re.search(regex.assign, listFile[indexCounter]):
    print("Found token assignment:    " , listFile[indexCounter] , " in line " , lineNumber)
  elif re.match(r"\n", listFile[indexCounter]):
    lineNumber+=1
  elif re.compile(regex.eop).search(listFile[indexCounter]):
    print("End of Program detected:  ", listFile[indexCounter], "\n")  
    programNumber+=1
  # else:
    # warningCounter+=1
    # print("Error detected at " , lineNumber)
    

    # if re.search(regex.typeInt, indexCounter): # Integer
    #   print("Found token type Integer:  " , indexCounter , " in indexCounter " , lineNumber)
    # elif re.search(regex.typeString, indexCounter): # String
    #   print("Found token type String:   " , indexCounter , " in indexCounter " , lineNumber)
    # elif re.search(regex.typeboolean, indexCounter): # Boolean
    #   print("Found token type Boolean:  " , indexCounter , " in indexCounter " , lineNumber)
    # elif re.search(regex.boolFalse, indexCounter): # False
    #   print("Found token boolean false: " , indexCounter , " in indexCounter " , lineNumber)
    # elif re.search(regex.boolTrue, indexCounter): # True
    #   print("Found token boolean True:  " , indexCounter , " in indexCounter " , lineNumber)
    # else: # if none were found, then print as character 
    #   print("character: ", indexCounter , " in indexCounter " , lineNumber)
      # newList = list(indexCounter) # This splits characters into one
      # indexCounter = 0
      # lastIndex = len(newList)
      # # This is to remove the l
      # if indexCounter < len(newList):      
      #   if newList[lastIndex-1] == "\n":
      #     lineNumber+=1
      #     del newList[lastIndex-1]
      #     while indexCounter < len(newList):
      #       print("character: ", newList[indexCounter] , " in indexCounter " , lineNumber)
      #       indexCounter+=1
  # End of character elif
  
  indexCounter+=1
