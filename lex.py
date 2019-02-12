# Author: Jae Kyoung Lee (LJ)
import re
# Importing list of our grammar regex from regex.py
import regex

# Opening as read mode to read the test files
open_file = open("test_alan.txt", "r")

listFile = list(open_file.read())
open_file.close()
# Variables
lineNumber = 1
programNumber = 1
indexCounter = 0
empty = "" # To improve code readability
errorCounter = 0
warningCounter = 0
lastIndex = len(listFile)-1

print(listFile)

while indexCounter < len(listFile):
  if re.search(regex.leftParen, listFile[indexCounter]):
    print("Found token LEFT PAREN: " , listFile[indexCounter],   " in line " , lineNumber)
  elif re.search(regex.rightParen, listFile[indexCounter]):
    print("Found token RIGHT PAREN: " , listFile[indexCounter] ,  " in line " , lineNumber)
  elif re.search(regex.leftBrace, listFile[indexCounter]):
    print("Found token LEFT BRACE : " , listFile[indexCounter] , " in line ", lineNumber)
  elif re.search(regex.rightBrace, listFile[indexCounter]):
    print("Found token RIGHT BRACE : " , listFile[indexCounter] , " in line ", lineNumber)
# First it detects for any letters and depending on what it finds, it will loop until there are no more letters
  elif re.search(regex.character, listFile[indexCounter]):
    if re.search(r"i", listFile[indexCounter]): # IF or INT
      # To avoid index out of range
      if indexCounter+1 < len(listFile) and (re.search(r"f", listFile[indexCounter+1]) or re.search(r"n", listFile[indexCounter+1])) : 
        indexCounter+=1 
        if re.search(r"f", listFile[indexCounter]):
          print("Found token IF : if in line " , lineNumber)
          indexCounter+=1
        elif re.search(r"n", listFile[indexCounter]):
          if indexCounter+1 < len(listFile):
            indexCounter+=1
            if re.search(r"t", listFile[indexCounter]):
              print("Found token INT : int in line " , lineNumber)
      else: 
        print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
    elif re.search(r"w", listFile[indexCounter]): # WHILE
      # It starts +4 because it's after "w"
      if indexCounter+4 < len(listFile) and re.search(r"h", listFile[indexCounter+1]) and re.search(r"i", listFile[indexCounter+2]) and re.search(r"l", listFile[indexCounter+3]) and re.search(r"e", listFile[indexCounter+4]):
        print("Found token WHILE : while in line " ,  lineNumber)
        indexCounter+=5 # Since indexCounter did not increment, it has to increment by the number of letters
        continue
      elif indexCounter < len(listFile): 
        print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
        indexCounter+=1
        continue
    elif re.search(r"p", listFile[indexCounter]): # PRINT
      if indexCounter+4 < len(listFile) and re.search(r"r", listFile[indexCounter+1]) and re.search(r"i", listFile[indexCounter+2]) and re.search(r"n", listFile[indexCounter+3]) and re.search(r"t", listFile[indexCounter+4]):
        print("Found token PRINT : print in line " ,  lineNumber)
        indexCounter+=5
        continue
      elif indexCounter < len(listFile): 
        print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
    elif re.search(r"b", listFile[indexCounter]): # BOOLEAN
      if indexCounter+6 < len(listFile) and re.search(r"o", listFile[indexCounter+1]) and re.search(r"o", listFile[indexCounter+2]) and re.search(r"l", listFile[indexCounter+3]) and re.search(r"e", listFile[indexCounter+4]) and re.search(r"a", listFile[indexCounter+5]) and re.search(r"n", listFile[indexCounter+6]):
          print("Found token BOOLEAN : boolean in line " ,  lineNumber)
          indexCounter+=7
          continue
      elif indexCounter < len(listFile): 
        print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
    elif re.search(r"s", listFile[indexCounter]): # STRING
      if indexCounter+5 < len(listFile) and re.search(r"t", listFile[indexCounter+1]) and re.search(r"r", listFile[indexCounter+2]) and re.search(r"i", listFile[indexCounter+3]) and re.search(r"n", listFile[indexCounter+4]) and re.search(r"g", listFile[indexCounter+5]):
        print("Found token STRING : string in line " ,  lineNumber)
        indexCounter+=6
        continue
      elif indexCounter < len(listFile): 
        print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
    elif re.search(r"f", listFile[indexCounter]): # FALSE
      if indexCounter+4 < len(listFile) and re.search(r"a", listFile[indexCounter+1]) and re.search(r"l", listFile[indexCounter+2]) and re.search(r"s", listFile[indexCounter+3]) and re.search(r"e", listFile[indexCounter+4]):
        print("Found token FALSE : false in line " ,  lineNumber)
        indexCounter+=5
        continue
      elif indexCounter < len(listFile): 
        print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
    elif re.search(r"t", listFile[indexCounter]): # TRUE
      if indexCounter+3 < len(listFile) and re.search(r"r", listFile[indexCounter+1]) and re.search(r"u", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]):
          print("Found token TRUE : true in line " ,  lineNumber)
          indexCounter+=4
          continue
      elif indexCounter < len(listFile): 
        print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
    else: 
      # All characters that are not reserved words
      print("Found token ID : " , listFile[indexCounter] , " in line " , lineNumber)
    # End of big word if statement
  elif re.search(regex.quote, listFile[indexCounter]): # QUOTE
    print("Found token START QUOTE : " , listFile[indexCounter] , " in line ", lineNumber)
    if (indexCounter+1 < len(listFile)):
      indexCounter+=1
      while re.search(r"[^\"]", listFile[indexCounter]): # CHARLIST
        print("Found token CHAR : " , listFile[indexCounter], " in line " , lineNumber)
        indexCounter+=1
    print("Found token END QUOTE : " , listFile[indexCounter], " in line ", lineNumber)
  elif re.search(r"!", listFile[indexCounter]): # NOT EQUAL
    if re.search(r"=", listFile[indexCounter+1]) and (indexCounter+1) < len(listFile):
      print("Found token NOT EQUAL : != in line ", lineNumber)
    else: # There is no such thing as standalone ' ! ' mark in our grammar = ERROR
      errorCounter+=1
      break
  elif re.search(regex.assign, listFile[indexCounter]): # ASSIGNMENT
    print("Found token assignment : " , listFile[indexCounter] , " in line " , lineNumber)
    indexCounter+=1
    if indexCounter < len(listFile) and re.search(r"=", listFile[indexCounter]): # EQUAL
      print("Found token EQUAL :  ==  in line " , lineNumber)
      indexCounter+=1
    continue
  elif re.findall(regex.digit, listFile[indexCounter]): # DIGIT
    print("Found token DIGIT : " , listFile[indexCounter] , " in line " , lineNumber)
  elif re.search(r"\+", listFile[indexCounter]): # INTOP / PLUS SIGN
    print("Found token INTOP : " , listFile[indexCounter] , " in line " , lineNumber)
  elif re.search(r"/", listFile[indexCounter]) and re.search(r"\*", listFile[indexCounter+1]): # COMMENT
    indexCounter+=2 # indexCounter moves to the content of the comment
    # print(listFile[indexCounter])
    if (indexCounter+1) < len(listFile): 
      while re.search(r"[^\*]", listFile[indexCounter]) and re.search(r"[^/]", listFile[indexCounter+1]):
        indexCounter+=1 # Ignore comments
      indexCounter+=2 # indexCounter moves out of the comment
      continue
    # END OF COMMENT if-statement
  elif re.match(r"\n", listFile[indexCounter]): # LINE NUMBER COUNTER
    lineNumber+=1
  elif re.compile(regex.eop).search(listFile[indexCounter]):
    print("End of Program detected:  ", listFile[indexCounter], " in line " , lineNumber , "\n")  
    programNumber+=1
  elif re.search(r"[\s]", listFile[indexCounter]): # SPACE
    # Could not leave this if statement empty, so increment indexCounter and go back to the top
    indexCounter+=1
    continue
  else:
    errorCounter+=1
    break
  indexCounter+=1 

if re.search(r"[\s]", listFile[lastIndex]):
  # To get to the last element that isn't a white space
  while re.search(r"[\s]", listFile[lastIndex]):
    lastIndex-=1
  if re.search(r"[^\$]", listFile[lastIndex]):
    listFile.append("$")
    print("\nEOP is not found at the end of last program. Adding EOP at ", lineNumber)
    warningCounter+=1

if errorCounter > 0:
  print("ERROR!! Please fix error in line " , lineNumber)
elif warningCounter > 0:
  print("Found " , warningCounter , " warning(s) in LEXER")
