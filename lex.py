# Author: Jae Kyoung Lee (LJ)
import re
# Importing list of our grammar regex from regex.py
# Please ensure that you have downloaded regex.py as well
import regex
import parser
import token

def lex(listFile):
  # # Opening as read mode to read the test files
  # open_file = open("test_alan.txt", "r")
  # # Creating list of individual contents in the file
  # listFile = list(open_file.read())
  # # Close file
  # open_file.close()

  # Variables
  lineNumber = 1
  programNumber = 1
  indexCounter = 0
  empty = "" # To improve code readability
  errorCounter = 0
  warningCounter = 0
  lastIndex = len(listFile)-1
  running = False
  errorCheck = True

  tokenList = []

  class Token:
    def __init__(self, tokenKind, tokenValue, lineNumber):
      self.kind = tokenKind
      self.value = tokenValue
      self.lineNum = lineNumber
  def createToken(kind, value, lineNum):
    # tokens = token.Token(kind, value, lineNum)
    tokens = Token(kind, value, lineNum)
    tokenList.append(tokens)

  print("LEXER")
  # This while is to print Program starting statement
  while indexCounter < len(listFile):
    if errorCheck:
      # if re.search(r"[^\s]", listFile[indexCounter]):
      if re.search(regex.leftBrace, listFile[indexCounter]):
        print("Program " , programNumber , " starting....")
        running=not running # This should equal to True
      # This while will actually go through the list and do the lexing
      while running and indexCounter+1 < len(listFile):
        if re.search(regex.leftParen, listFile[indexCounter]):
          createToken("LEFT PAREN", listFile[indexCounter], lineNumber)
          print("Found token LEFT PAREN: " , listFile[indexCounter],   " in line " , lineNumber)
        elif re.search(regex.rightParen, listFile[indexCounter]):
          print("Found token RIGHT PAREN: " , listFile[indexCounter] ,  " in line " , lineNumber)
        elif re.search(regex.leftBrace, listFile[indexCounter]):
          createToken("LEFT BRACE", listFile[indexCounter], lineNumber)
          print("Found token LEFT BRACE : " , listFile[indexCounter] , " in line ", lineNumber)
        elif re.search(regex.rightBrace, listFile[indexCounter]):
          createToken("RIGHT BRACE", listFile[indexCounter], lineNumber)
          print("Found token RIGHT BRACE : " , listFile[indexCounter] , " in line ", lineNumber)
        
        # First it detects for any letters and depending on what it finds, it will loop until there are no more letters
        elif re.search(regex.character, listFile[indexCounter]):
          if re.search(r"i", listFile[indexCounter]): # IF or INT
            # To avoid index out of range
            if indexCounter+1 < len(listFile) and (re.search(r"f", listFile[indexCounter+1]) or re.search(r"n", listFile[indexCounter+1])) : 
              # indexCounter+=1 
              if re.search(r"f", listFile[indexCounter+1]):
                createToken("T_IF", "if", lineNumber)
                print("Found token IF : if in line " , lineNumber)
                indexCounter+=1 # This will reach ' f ' after i
              elif re.search(r"n", listFile[indexCounter+1]) and re.search(r"t", listFile[indexCounter+2]) and indexCounter+1 < len(listFile):
                createToken("T_INT", "int", lineNumber)
                print("Found token INT : int in line " , lineNumber)
                indexCounter+=2 # This will reach ' t ' after in
            else: 
              createToken("T_ID", listFile[indexCounter], lineNumber)
              print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
          
          elif re.search(r"w", listFile[indexCounter]): # WHILE
            # This first checks to see if index exists to identify the word WHILE
            if indexCounter+4 < len(listFile) and re.search(r"h", listFile[indexCounter+1]) and re.search(r"i", listFile[indexCounter+2]) and re.search(r"l", listFile[indexCounter+3]) and re.search(r"e", listFile[indexCounter+4]):
              createToken("T_WHILE", "while", lineNumber)
              # If there exist an index and every index within matches h i l e then, we found WHILE
              print("Found token WHILE : while in line " ,  lineNumber)
              # Incrementing by the number of letters in the reserved word
              indexCounter+=5 
              # To skip indexCounter+=1 at the end of the while-loop
              continue
            elif indexCounter < len(listFile):  # ID
              createToken("T_ID", listFile[indexCounter], lineNumber)
              print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
          elif re.search(r"p", listFile[indexCounter]): # PRINT
            if indexCounter+4 < len(listFile) and re.search(r"r", listFile[indexCounter+1]) and re.search(r"i", listFile[indexCounter+2]) and re.search(r"n", listFile[indexCounter+3]) and re.search(r"t", listFile[indexCounter+4]):
              createToken("T_PRINT", "print", lineNumber)
              print("Found token PRINT : print in line " ,  lineNumber)
              indexCounter+=5
              continue
            elif indexCounter < len(listFile): 
              createToken("T_ID", listFile[indexCounter], lineNumber)
              print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
          elif re.search(r"b", listFile[indexCounter]): # BOOLEAN
            if indexCounter+6 < len(listFile) and re.search(r"o", listFile[indexCounter+1]) and re.search(r"o", listFile[indexCounter+2]) and re.search(r"l", listFile[indexCounter+3]) and re.search(r"e", listFile[indexCounter+4]) and re.search(r"a", listFile[indexCounter+5]) and re.search(r"n", listFile[indexCounter+6]):
                createToken("T_BOOLEAN", "boolean", lineNumber)
                print("Found token BOOLEAN : boolean in line " ,  lineNumber)
                indexCounter+=7
                continue
            elif indexCounter < len(listFile): 
              createToken("T_ID", listFile[indexCounter], lineNumber)
              print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
          elif re.search(r"s", listFile[indexCounter]): # STRING
            if indexCounter+5 < len(listFile) and re.search(r"t", listFile[indexCounter+1]) and re.search(r"r", listFile[indexCounter+2]) and re.search(r"i", listFile[indexCounter+3]) and re.search(r"n", listFile[indexCounter+4]) and re.search(r"g", listFile[indexCounter+5]):
              createToken("T_STRING", "string", lineNumber)
              print("Found token STRING : string in line " ,  lineNumber)
              indexCounter+=6
              continue
            elif indexCounter < len(listFile): 
              createToken("T_ID", listFile[indexCounter], lineNumber)
              print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
          elif re.search(r"f", listFile[indexCounter]): # FALSE
            if indexCounter+4 < len(listFile) and re.search(r"a", listFile[indexCounter+1]) and re.search(r"l", listFile[indexCounter+2]) and re.search(r"s", listFile[indexCounter+3]) and re.search(r"e", listFile[indexCounter+4]):
              createToken("T_FALSE", "false", lineNumber)
              print("Found token FALSE : false in line " ,  lineNumber)
              indexCounter+=5
              continue
            elif indexCounter < len(listFile): 
              createToken("T_ID", listFile[indexCounter], lineNumber)
              print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
          elif re.search(r"t", listFile[indexCounter]): # TRUE
            if indexCounter+3 < len(listFile) and re.search(r"r", listFile[indexCounter+1]) and re.search(r"u", listFile[indexCounter+2]) and re.search(r"e", listFile[indexCounter+3]):
              createToken("T_TRUE", "true", lineNumber)
              print("Found token TRUE : true in line " ,  lineNumber)
              indexCounter+=4
              continue
            elif indexCounter < len(listFile): 
              createToken("T_ID", listFile[indexCounter], lineNumber)
              print("Found token ID : " , listFile[indexCounter], " in line ", lineNumber)
          else: 
            createToken("T_ID", listFile[indexCounter], lineNumber)
            # All characters that are not reserved words
            print("Found token ID : " , listFile[indexCounter] , " in line " , lineNumber)
          # End of big word if statement
        elif re.search(regex.quote, listFile[indexCounter]): # QUOTE
          createToken("T_QUOTE", listFile[indexCounter], lineNumber)
          print("Found token START QUOTE : " , listFile[indexCounter] , " in line ", lineNumber)
          if (indexCounter+1 < len(listFile)):
            indexCounter+=1
            if re.search(r"[^\"]", listFile[indexCounter]) and indexCounter+1 < len(listFile): # CHARLIST
              while re.search(r"[a-z]|[\t]|[ ]", listFile[indexCounter]) or re.search(r"/", listFile[indexCounter]) and re.search(r"\*", listFile[indexCounter+1]):
                createToken("T_CHAR", listFile[indexCounter], lineNumber)
                print("Found token CHAR : " , listFile[indexCounter], " in line " , lineNumber)
                indexCounter+=1
                while re.search(r"/", listFile[indexCounter]) and re.search(r"\*", listFile[indexCounter+1]): # COMMENT
                    # indexCounter moves to the content of the comment
                    indexCounter+=2
                    if (indexCounter+1) < len(listFile): 
                      while re.search(r"[^\*]", listFile[indexCounter]) and re.search(r"[^/]", listFile[indexCounter+1]):
                        indexCounter+=1 # Ignore comments
                      indexCounter+=2 # indexCounter moves out of the comment
              if re.search(regex.quote, listFile[indexCounter]):
                createToken("T_QUOTE", listFile[indexCounter], lineNumber)
                print("Found token END QUOTE : " , listFile[indexCounter], " in line ", lineNumber)
              else:# re.search(r"[^a-z]|[^\t]|[^ ]|[^\"]", listFile[indexCounter]):
                  errorCounter+=1
                  errorCheck = not errorCheck
                  while re.search(r"[^\"]", listFile[indexCounter]) and indexCounter+1 < len(listFile):
                    # print(listFile[indexCounter])
                    if re.search(regex.newLine, listFile[indexCounter]):
                      lineNumber+=1
                    indexCounter+=1
                  break  
        elif re.search(r"!", listFile[indexCounter]): # NOT EQUAL
          if re.search(r"=", listFile[indexCounter+1]) and (indexCounter+1) < len(listFile):
            createToken("T_NOT_EQUAL", "!=", lineNumber)
            print("Found token NOT EQUAL : != in line ", lineNumber)
          # There is no such thing as standalone ' ! ' mark in our grammar = ERROR
          else:   
            errorCounter+=1
            break
        elif re.search(regex.assign, listFile[indexCounter]): # ASSIGNMENT
          createToken("T_ASSIGN", listFile[indexCounter], lineNumber)
          print("Found token assignment : " , listFile[indexCounter] , " in line " , lineNumber)
          indexCounter+=1
          if indexCounter < len(listFile) and re.search(r"=", listFile[indexCounter]): # EQUAL
            createToken("T_EQUAL", listFile[indexCounter], lineNumber)
            print("Found token EQUAL :  ==  in line " , lineNumber)
            indexCounter+=1
          continue
        elif re.findall(regex.digit, listFile[indexCounter]): # DIGIT
          createToken("T_DIGIT", listFile[indexCounter], lineNumber)
          print("Found token DIGIT : " , listFile[indexCounter] , " in line " , lineNumber)
        elif re.search(r"\+", listFile[indexCounter]): # INTOP / PLUS SIGN
          createToken("T_OP", listFile[indexCounter], lineNumber)
          print("Found token OP : " , listFile[indexCounter] , " in line " , lineNumber)
        elif re.search(r"/", listFile[indexCounter]) and re.search(r"\*", listFile[indexCounter+1]): # COMMENT
          # indexCounter moves to the content of the comment
          indexCounter+=2
          if (indexCounter+1) < len(listFile): 
            while re.search(r"[^\*]", listFile[indexCounter]) and re.search(r"[^/]", listFile[indexCounter+1]):
              indexCounter+=1 # Ignore comments
            indexCounter+=2 # indexCounter moves out of the comment
            continue
          # END OF COMMENT if-statement
        elif re.match(r"\n", listFile[indexCounter]): # LINE NUMBER COUNTER
          lineNumber+=1
        elif re.compile(regex.eop).search(listFile[indexCounter]):
          createToken("T_EOP", listFile[indexCounter], lineNumber)
          print("End of Program detected:  ", listFile[indexCounter], " in line " , lineNumber , "\n")  
          programNumber+=1
          errorCounter=0
          running = not running # This should equal false  
        elif re.search(regex.space, listFile[indexCounter]): # SPACE
          # Could not leave this if statement empty, so increment indexCounter and go back to the top
          indexCounter+=1
          continue
        else:
          errorCounter+=1
          errorCheck = not errorCheck
          break
        indexCounter+=1
        # End of running while-loop
      # End of errorCheck if statement
    elif not errorCheck: # If there are any errors, 
      if errorCounter > 0:
        print("ERROR!! Please fix error in line " , lineNumber , " by fixing invalid character\n")
        while re.search(r"[^$]", listFile[indexCounter]):
          if re.search(regex.newLine, listFile[indexCounter]):
            lineNumber+=1
          indexCounter+=1
      # print(listFile[indexCounter], "printing inside errorCheck")
      if re.compile(regex.eop).search(listFile[indexCounter]):
        programNumber+=1
        errorCounter=0
        running = not running # This should equal false  
        errorCheck = True

    if (indexCounter < len(listFile)) and re.match(regex.newLine, listFile[indexCounter]): # LINE NUMBER COUNTER
      lineNumber+=1 
    indexCounter+=1
  # End of while-loop
  
  if re.search(regex.space, listFile[lastIndex]) or re.search(r"[^\$]", listFile[lastIndex]):
    # To get to the last element that isn't a white space
    while re.search(r"[\s]", listFile[lastIndex]):
      lastIndex-=1
    if re.search(r"[^\$]", listFile[lastIndex]):
      listFile.append("$")
      createToken("T_EOP", listFile[indexCounter], lineNumber)
      print("\nEOP is not found at the end of last program. Adding EOP at ", lineNumber)
      warningCounter+=1
  if warningCounter > 0:
    print("Found " , warningCounter , " warning(s) in LEXER")

  return tokenList

  # print("separate")
  # i = 0
  # # while running:
  # #   print(tokenList[i])
  # #   # print(token.lineList[i])  
  # #   i+=1

  # for i in range(len(tokenList)):
  #   print(tokenList[i].kind, tokenList[i].value, tokenList[i].lineNum)

  # # print(tokenList.kind)