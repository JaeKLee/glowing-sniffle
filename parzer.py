import lex
import regex
import tree
# import driver

# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
errorCounter = 0
programNumber = 1
cst = tree.Tree()

# # For dynamic test inputs
# x = str(input("Enter the test file: "))

# # Opening as read mode to read the test files
# open_file = open(x, "r")
# # Creating list of individual contents in the file
# listFile = list(open_file.read())
# # Close file
# open_file.close()

# # Create list of tokens from the LEX output
# # It should be 2D list
# tokenList = driver.tokenList

# for i in range(len(tokenList)):
#   for j in range(len(tokenList[i])):
#     print(tokenList[i][j].value)
# print("\nPARSER")
# Testing purpose
# for i in tokenList:
#   for j in i:
#     print(j.kind)

def match(tokenList, expectedToken):
  global rowToken, columnToken
  notVal = False
  if rowToken < len(tokenList):
    if expectedToken == tokenList[rowToken][columnToken].kind:
      notVal = True  
  return notVal
  
def printErrorStmt(tokenList, expectedToken):
  global rowToken, columnToken
  print("Failed - Expected ", expectedToken,  " but found " ,  tokenList[rowToken][columnToken].kind , " with value '" ,  tokenList[rowToken][columnToken].value , "' on line " ,  tokenList[rowToken][columnToken].lineNum)
  # For errors, we skip to the end of the index, so parser doesn't continue
  while columnToken+1 < len(tokenList) and tokenList[rowToken][columnToken].value != "$":
    columnToken+=1
  print("Parse failed with 1 error")

def printValidStmt(tokenList, expectedToken):
  global rowToken, columnToken
  if rowToken < len(tokenList):
    print("Valid - Expected ", expectedToken,  " and got " ,  tokenList[rowToken][columnToken].kind , " with value '" ,  tokenList[rowToken][columnToken].value , "' on line " ,  tokenList[rowToken][columnToken].lineNum)
    columnToken+=1

def parseBoolOp(tokenList):
  print("parseBoolOp()") 
  if match(tokenList, "T_BOOLOP") is True:
    printValidStmt(tokenList, "T_BOOLOP")
  else:
    printErrorStmt(tokenList, "T_BOOLOP")

def parseChar(tokenList):
  if match(tokenList, "T_CHAR") is True:
    print("parseChar()")

def parseCharList(tokenList):
  print("parseCharList()")
  if match(tokenList, "T_CHAR") is True:
    printValidStmt(tokenList, "T_CHAR")
    parseChar(tokenList)
    parseCharList(tokenList)
  elif tokenList[rowToken][columnToken].value == " ":
    printValidStmt(tokenList, "T_SPACE")
    parseCharList(tokenList)

def parseID(tokenList):
  printValidStmt(tokenList, "T_ID parseID")
  # print(tokenList[rowToken][columnToken].value)
  # parseChar()
  if tokenList[rowToken][columnToken].value == "=":
    parseAssignment(tokenList)

def parseExpr(tokenList):
  print("parseExpr()")
  if match(tokenList, "T_DIGIT") is True:
    parseIntExpr(tokenList)
  elif match(tokenList, "T_QUOTE") is True:
    parseStringExpr(tokenList) 
  elif match(tokenList, "T_RPAREN") is True:
    parseBooleanExpr(tokenList)
  else:
    parseID(tokenList)

def parseBooleanExpr(tokenList):
  print("parseBooleanExpr()")
  if match(tokenList, "T_LPAREN") is True:
    printValidStmt(tokenList, "T_LPAREN")
    parseExpr(tokenList)
    parseBoolOp(tokenList)
    parseExpr(tokenList)
    if match(tokenList, "T_RPAREN") is True:
      printValidStmt(tokenList, "T_RPAREN")
    else:
      printErrorStmt(tokenList, "T_RPAREN")
  else:
    printErrorStmt(tokenList, "this is wrong")

def parseStringExpr(tokenList):
  print("parseStringExpr()")
  if match(tokenList, "T_QUOTE") is True:
    printValidStmt(tokenList, "T_QUOTE")
    parseCharList(tokenList) 
    if match(tokenList, "T_QUOTE") is True:
      printValidStmt(tokenList, "T_QUOTE")
  else: 
    print("parse string wrong")

def parseIntExpr(tokenList):
  print("parseIntExpr()")
  if match(tokenList, "T_DIGIT") is True:
    printValidStmt(tokenList, "T_DIGIT")
    if match(tokenList, "T_OP") is True:
      printValidStmt(tokenList, "T_OP")
      parseExpr(tokenList)
  else:
    printErrorStmt(tokenList, "T_DIGIT")

def parseStatement(tokenList):
  global rowToken, columnToken
  notVal = False
  # If print("parseStatement()") is not in individual
  # statements, it will print out countless parseStatement()
  if match(tokenList, "T_PRINT") is True:
    print("parseStatement()")
    notVal = True
    parsePrint(tokenList)
  elif match(tokenList, "T_ID") is True:
    print("parseStatement()")
    notVal = True
    parseAssignment(tokenList)
  elif match(tokenList, "T_TYPE") is True:
    print("parseStatement()")
    notVal = True
    parseVarDecl(tokenList)
  elif match(tokenList, "T_WHILE") is True:
    print("parseStatement()")
    notVal = True
    parseWhile(tokenList)
  elif match(tokenList, "T_IF") is True:
    print("parseStatement()")
    notVal = True
    parseIf(tokenList)
  elif match(tokenList, "T_LBRACE") is True:
    print("parseStatement()")
    notVal = True
    parseBlock(tokenList)
  else: # It will do nothing because statementList allows epsilon
    notVal = False
  return notVal
  
def parseStatementList(tokenList):
  if parseStatement(tokenList) is True:
    print("parseStatementList()")
    parseStatement(tokenList)
    parseStatementList(tokenList)
  elif match(tokenList, "T_RBRACE") is True:
    printValidStmt(tokenList, "T_RBRACE")

def parseBlock(tokenList):
  if match(tokenList, "T_LBRACE") is True:
    printValidStmt(tokenList, "T_LBRACE")
    print("parseBlock()")
    # cst.addNode()
    if parseStatement(tokenList) is True:
      parseStatementList(tokenList)
  if match(tokenList, "T_RBRACE") is True:
    printValidStmt(tokenList, "T_RBRACE")

def parseIf(tokenList):
  print("parseIf()")
  if match(tokenList, "T_IF") is True:
    printValidStmt(tokenList, "T_IF")
    parseBooleanExpr(tokenList)
    parseBlock(tokenList)
  else:
    printErrorStmt(tokenList, "T_IF")

def parseWhile(tokenList):
  print("parseWhile()")  
  if match(tokenList, "T_WHILE") is True:
    printValidStmt(tokenList, "T_WHILE")
    parseBooleanExpr(tokenList)
    parseBlock(tokenList)
  else:
    printErrorStmt(tokenList, "T_WHILE")

def parseVarDecl(tokenList):
  print("parseVarDecl()")
  if match(tokenList, "T_TYPE") is True:
    printValidStmt(tokenList, "T_TYPE")
    parseID(tokenList)
  else:
    printErrorStmt(tokenList, "VARDECL")

def parseAssignment(tokenList):
  print("parseAssignment()")
  if match(tokenList, "T_ID") is True or match(tokenList, "T_ASSIGN") is True:
    # parseID()
    if match(tokenList, "T_ID") is True:
      parseID(tokenList)
    elif match(tokenList, "T_ASSIGN") is True: 
      printValidStmt(tokenList, "T_ASSIGN")
      parseExpr(tokenList)
  else:
    printErrorStmt(tokenList, "parseAssignment")

def parsePrint(tokenList):
  print("parsePrint()")
  if match(tokenList, "T_PRINT") is True:
    printValidStmt(tokenList, "T_PRINT")
    if match(tokenList, "T_LPAREN") is True:
      printValidStmt(tokenList, "T_LPAREN")
      parseExpr(tokenList)
    else:
      printErrorStmt(tokenList, "T_LPARENT")
    if match(tokenList, "T_RPAREN") is True:
      printValidStmt(tokenList, "T_RPAREN")
    else:
      printErrorStmt(tokenList, "T_RPAREN")
  else:
    printErrorStmt(tokenList, "T_PRINT")

def parseProgram(tokenList):
  global programNumber, rowToken, columnToken
  print("parseProgram()")
  cst.addNode("Program", "branch", "", None)
  if rowToken < len(tokenList):
    if match(tokenList, "T_LBRACE") is True:
      parseBlock(tokenList)
    if match(tokenList, "T_EOP") is True:
      printValidStmt(tokenList, "T_EOP")
      programNumber+=1
      # Once it reaches EOP, move to the next row of the 2D array
      rowToken+=1
      # Set columnToken to zero to start from the beginning of the row
      columnToken=0
      # To avoid out of range
      if rowToken < len(tokenList):
        parse(tokenList)

def parse(tokenList):
  global programNumber, rowToken, columnToken
  print("\nProgram " , programNumber , " starting....")
  if match(tokenList, "ERROR") is True:
    print("Parser: Skipped due to Lexer error(s)")
    if rowToken < len(tokenList):
      rowToken+=1
      programNumber+=1
      columnToken=0
      parse(tokenList)
  else:
    parseProgram(tokenList)

# def startParse():
#   parse(tokenList)
# parse()