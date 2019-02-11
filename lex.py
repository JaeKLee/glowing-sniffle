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
    print("Found token LEFT PAREN:    " , listFile[indexCounter],   " in line " , lineNumber)
  elif re.search(regex.rightParen, listFile[indexCounter]):
    print("Found token RIGHT PAREN:   " , listFile[indexCounter] ,  " in line " , lineNumber)
  elif re.search(regex.leftBrace, listFile[indexCounter]):
    print("Found token LEFT BRACE:   " , listFile[indexCounter] , " in line ", lineNumber)
  elif re.search(regex.rightBrace, listFile[indexCounter]):
    print("Found token RIGHT BRACE:   " , listFile[indexCounter] , " in line ", lineNumber)
# First it detects for any letters and depending on what it finds, it will loop until there are no more letters
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
              continue
    elif re.search(r"w", listFile[indexCounter]):
      if indexCounter+4 < len(listFile):
        indexCounter+=1
        if re.search(r"h", listFile[indexCounter]) and re.search(r"i", listFile[indexCounter+1]) and re.search(r"l", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]):
          print("Found token WHILE : while in line " ,  lineNumber)
          indexCounter+=4
          continue
    elif re.search(r"p", listFile[indexCounter]):
      if indexCounter+4 < len(listFile):
        indexCounter+=1
        if re.search(r"r", listFile[indexCounter]) and re.search(r"i", listFile[indexCounter+1]) and re.search(r"n", listFile[indexCounter+2]) and re.search(r"t", listFile[indexCounter+3]):
          print("Found token PRINT : print in line " ,  lineNumber)
          indexCounter+=4
          continue
    elif re.search(r"b", listFile[indexCounter]):
      if indexCounter+6 < len(listFile):
        indexCounter+=1
        if re.search(r"o", listFile[indexCounter]) and re.search(r"o", listFile[indexCounter+1]) and re.search(r"l", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]) and re.search(r"a", listFile[indexCounter+4]) and re.search(r"n", listFile[indexCounter+5]):
          print("Found token BOOLEAN : boolean in line " ,  lineNumber)
          indexCounter+=6
          continue
    elif re.search(r"f", listFile[indexCounter]):
      if indexCounter+4 < len(listFile):
        indexCounter+=1
        if re.search(r"a", listFile[indexCounter]) and re.search(r"l", listFile[indexCounter+1]) and re.search(r"s", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]):
          print("Found token FALSE : false in line " ,  lineNumber)
          indexCounter+=4
          continue
    elif re.search(r"t", listFile[indexCounter]):
      if indexCounter+3 < len(listFile):
        indexCounter+=1
        if re.search(r"r", listFile[indexCounter]) and re.search(r"u", listFile[indexCounter+1]) and re.search(r"e", listFile[indexCounter+2]):
          print("Found token TRUE : true in line " ,  lineNumber)
          indexCounter+=3
          continue
    else: 
      print("Found toke ID : " , listFile[indexCounter] , " in line " , lineNumber)
    # End of big word if statement
  elif re.search(regex.quote, listFile[indexCounter]):
    print("Found token START QUOTE : " , listFile[indexCounter] , " in line ", lineNumber)
    if (indexCounter+1 < len(listFile)):
      indexCounter+=1
      while re.search(r"[^\"]", listFile[indexCounter]):
        print("Found token CHAR : " , listFile[indexCounter], " in line " , lineNumber)
        indexCounter+=1
    print("Found token END QUOTE : " , listFile[indexCounter], " in line ", lineNumber)
  elif re.search(r"!", listFile[indexCounter]):
    if re.search(r"=", listFile[indexCounter+1]) and (indexCounter+1) < len(listFile):
      print("Found token NOT EQUAL : != in line ", lineNumber)
    else: 
      errorCounter+=1
      break
  elif re.search(regex.assign, listFile[indexCounter]):
    print("Found token assignment:    " , listFile[indexCounter] , " in line " , lineNumber)
    indexCounter+=1
    if indexCounter < len(listFile) and re.search(r"=", listFile[indexCounter]):
      print("Found token EQUAL :  ==  in line " , lineNumber)
      indexCounter+=1
  elif re.search(r"[0-9]", listFile[indexCounter]):
    print("Found token DIGIT : " , listFile[indexCounter] , " in line " , lineNumber)
  elif re.search(r"\+", listFile[indexCounter]):
    print("Found token INTOP : " , listFile[indexCounter] , " in lin " , lineNumber)
  # elif re.search(r"/", listFile[indexCounter]):
  #   if indexCounter < len(listFile) and re.search(r"=", listFile[indexCounter]):
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
  if errorCounter > 0:
    print("ERROR!! Please fix error in line " , lineNumber)
