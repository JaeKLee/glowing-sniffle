import lex
import regex
import tree

# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
errorCounter = 0
programNumber = 1
# cst = tree.Tree()

# For dynamic test inputs
x = str(input("Enter the test file: "))

# Opening as read mode to read the test files
open_file = open(x, "r")
# Creating list of individual contents in the file
listFile = list(open_file.read())
# Close file
open_file.close()

# Create list of tokens from the LEX output
# It should be 2D list
tokenList = lex.lex(listFile)

# for i in range(len(tokenList)):
#   for j in range(len(tokenList[i])):
#     print(tokenList[i][j].value)
print("\nPARSER")
# Testing purpose
# for i in tokenList:
#   for j in i:
#     print(j.kind)

def match(expectedToken):
  global rowToken, columnToken
  notVal = False
  if rowToken < len(tokenList):
    if expectedToken == tokenList[rowToken][columnToken].kind:
      notVal = True  
  return notVal
  
def printErrorStmt(expectedToken):
  global rowToken, columnToken
  print("Failed - Expected ", expectedToken,  " but found " ,  tokenList[rowToken][columnToken].kind , " with value '" ,  tokenList[rowToken][columnToken].value , "' on line " ,  tokenList[rowToken][columnToken].lineNum)
  # For errors, we skip to the end of the index, so parser doesn't continue
  while columnToken+1 < len(tokenList) and tokenList[rowToken][columnToken].value != "$":
    columnToken+=1
  print("Parse failed with 1 error")

def printValidStmt(expectedToken):
  global rowToken, columnToken
  if rowToken < len(tokenList):
    print("Valid - Expected ", expectedToken,  " and got " ,  tokenList[rowToken][columnToken].kind , " with value '" ,  tokenList[rowToken][columnToken].value , "' on line " ,  tokenList[rowToken][columnToken].lineNum)
    columnToken+=1

def parseBoolOp():
  print("parseBoolOp()") 
  if match("T_BOOLOP") is True:
    printValidStmt("T_BOOLOP")
  else:
    printErrorStmt("T_BOOLOP")

def parseChar():
  if match("T_CHAR") is True:
    print("parseChar()")

def parseCharList():
  print("parseCharList()")
  if match("T_CHAR") is True:
    printValidStmt("T_CHAR")
    parseChar()
    parseCharList()
  elif tokenList[rowToken][columnToken].value == " ":
    printValidStmt("T_SPACE")
    parseCharList()

def parseID():
  printValidStmt("T_ID parseID")
  print(tokenList[rowToken][columnToken].value)
  # parseChar()
  if tokenList[rowToken][columnToken].value == "=":
    parseAssignment()

def parseExpr():
  print("parseExpr()")
  if match("T_DIGIT") is True:
    parseIntExpr()
  elif match("T_QUOTE") is True:
    parseStringExpr() 
  elif match("T_RPAREN") is True:
    parseBooleanExpr()
  else:
    parseID()

def parseBooleanExpr():
  print("parseBooleanExpr()")
  if match("T_LPAREN") is True:
    printValidStmt("T_LPAREN")
    parseExpr()
    parseBoolOp()
    parseExpr()
    if match("T_RPAREN") is True:
      printValidStmt("T_RPAREN")
    else:
      printErrorStmt("T_RPAREN")
  else:
    printErrorStmt("this is wrong")

def parseStringExpr():
  print("parseStringExpr()")
  if match("T_QUOTE") is True:
    printValidStmt("T_QUOTE")
    parseCharList() 
    if match("T_QUOTE") is True:
      printValidStmt("T_QUOTE")
  else: 
    print("parse string wrong")

def parseIntExpr():
  print("parseIntExpr()")
  if match("T_DIGIT") is True:
    printValidStmt("T_DIGIT")
    if match("T_OP") is True:
      printValidStmt("T_OP")
      parseExpr()
  else:
    printErrorStmt("T_DIGIT")

def parseStatement():
  global rowToken, columnToken
  notVal = False
  # If print("parseStatement()") is not in individual
  # statements, it will print out countless parseStatement()
  if match("T_PRINT") is True:
    print("parseStatement()")
    notVal = True
    parsePrint()
  elif match("T_ID") is True:
    print("parseStatement()")
    notVal = True
    parseAssignment()
  elif match("T_TYPE") is True:
    print("parseStatement()")
    notVal = True
    parseVarDecl()
  elif match("T_WHILE") is True:
    print("parseStatement()")
    notVal = True
    parseWhile()
  elif match("T_IF") is True:
    print("parseStatement()")
    notVal = True
    parseIf()
  elif match("T_LBRACE") is True:
    print("parseStatement()")
    notVal = True
    parseBlock()
  else: # It will do nothing because statementList allows epsilon
    notVal = False
  return notVal
  
def parseStatementList():
  if parseStatement() is True:
    print("parseStatementList()")
    parseStatement()
    parseStatementList()
  elif match("T_RBRACE") is True:
    printValidStmt("T_RBRACE")

def parseBlock():
  if match("T_LBRACE") is True:
    printValidStmt("T_LBRACE")
    print("parseBlock()")
    if parseStatement() is True:
      parseStatementList()
  if match("T_RBRACE") is True:
    printValidStmt("T_RBRACE")

def parseIf():
  print("parseIf()")
  if match("T_IF") is True:
    printValidStmt("T_IF")
    parseBooleanExpr()
    parseBlock()
  else:
    printErrorStmt("T_IF")

def parseWhile():
  print("parseWhile()")  
  if match("T_WHILE") is True:
    printValidStmt("T_WHILE")
    parseBooleanExpr()
    parseBlock()
  else:
    printErrorStmt("T_WHILE")

def parseVarDecl():
  print("parseVarDecl()")
  if match("T_TYPE") is True:
    printValidStmt("T_TYPE")
    parseID()
  else:
    printErrorStmt("VARDECL")

def parseAssignment():
  print("parseAssignment()")
  if match("T_ID") is True or match("T_ASSIGN") is True:
    # parseID()
    if match("T_ID") is True:
      parseID()
    elif match("T_ASSIGN") is True: 
      printValidStmt("T_ASSIGN")
      parseExpr()
  else:
    printErrorStmt("parseAssignment")

def parsePrint():
  print("parsePrint()")
  if match("T_PRINT") is True:
    printValidStmt("T_PRINT")
    if match("T_LPAREN") is True:
      printValidStmt("T_LPAREN")
      parseExpr()
    else:
      printErrorStmt("T_LPARENT")
    if match("T_RPAREN") is True:
      printValidStmt("T_RPAREN")
    else:
      printErrorStmt("T_RPAREN")
  else:
    printErrorStmt("T_PRINT")

def parseProgram():
  global programNumber, rowToken, columnToken
  print("parseProgram()")
  # cst.addNode("Program", "branch", "")
  if rowToken < len(tokenList):
    if match("T_LBRACE") is True:
      parseBlock()
    if match("T_EOP") is True:
      printValidStmt("T_EOP")
      programNumber+=1
      # Once it reaches EOP, move to the next row of the 2D array
      rowToken+=1
      # Set columnToken to zero to start from the beginning of the row
      columnToken=0
      # To avoid out of range
      if rowToken < len(tokenList):
        parse()

def parse():
  global programNumber, rowToken, columnToken
  print("\nProgram " , programNumber , " starting....")
  if match("ERROR") is True:
    print("Parser: Skipped due to Lexer error(s)")
    if rowToken < len(tokenList):
      rowToken+=1
      programNumber+=1
      columnToken=0
      parse()
  else:
    parseProgram()

# def startParse():
#   parse(tokenList)
parse()