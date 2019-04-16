import lex
import regex
import tree
import printstmt

# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
errorCounter = 0
cst = tree.Tree()
# print(cst)
parserToken = []



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
  global rowToken, columnToken, errorCounter
  errorCounter+=1
  print("Failed - Expected ", expectedToken,  " but found " ,  tokenList[rowToken][columnToken].kind , " with value '" ,  tokenList[rowToken][columnToken].value , "' on line " ,  tokenList[rowToken][columnToken].lineNum)
  # For errors, we skip to the end of the index, so parser doesn't continue
  while columnToken+1 < len(tokenList) and tokenList[rowToken][columnToken].value != "$":
    columnToken+=1
  print("Parse failed with 1 error")

def printValidStmt(tokenList, expectedToken):
  global rowToken, columnToken
  if rowToken < len(tokenList):
    printstmt.outerStmt[rowToken].append("Valid - Expected " +  str(expectedToken) + " and got " +  str(tokenList[rowToken][columnToken].kind) + " with value '" +  str(tokenList[rowToken][columnToken].value) + "' on line " +  str(tokenList[rowToken][columnToken].lineNum))
    # print("Valid - Expected ", expectedToken,  " and got " ,  tokenList[rowToken][columnToken].kind , " with value '" ,  tokenList[rowToken][columnToken].value , "' on line " ,  tokenList[rowToken][columnToken].lineNum)
    # columnToken+=1

def consumeToken(tokenList):
  global rowToken, columnToken
  if rowToken < len(tokenList):
    columnToken+=1

def parseBoolOp(tokenList):
  global rowToken, columnToken
  cst.addNodeDef("BoolOP", "branch")
  printstmt.outerStmt[rowToken].append("parseBoolOp()") 
  if match(tokenList, "T_BOOLOP") is True:
    printValidStmt(tokenList, "T_BOOLOP")
    cst.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
  else:
    printErrorStmt(tokenList, "T_BOOLOP")
  cst.endChildren()

def parseChar(tokenList):
  if match(tokenList, "T_CHAR") is True:
    printstmt.outerStmt[rowToken].append("parseChar()")
    consumeToken(tokenList)
    cst.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
  cst.endChildren()

def parseCharList(tokenList):
  global rowToken
  cst.addNodeDef("CharList", "branch")
  printstmt.outerStmt[rowToken].append("parseCharList()")
  if match(tokenList, "T_CHAR") is True:
    printValidStmt(tokenList, "T_CHAR")
    consumeToken(tokenList)
    parseChar(tokenList)
    parseCharList(tokenList)
  elif tokenList[rowToken][columnToken].value == " ":
    printValidStmt(tokenList, "T_SPACE")
    consumeToken(tokenList)
    parseCharList(tokenList)
  cst.endChildren()

def parseID(tokenList):
  printValidStmt(tokenList, "T_ID parseID")
  consumeToken(tokenList)
  cst.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
  # print(tokenList[rowToken][columnToken].value)
  # parseChar()
  cst.endChildren()
  if tokenList[rowToken][columnToken].value == "=":
    parseAssignment(tokenList)

def parseExpr(tokenList):
  global rowToken
  cst.addNodeDef("Expr", "branch")
  printstmt.outerStmt[rowToken].append("parseExpr()")
  if match(tokenList, "T_DIGIT") is True:
    parseIntExpr(tokenList)
  elif match(tokenList, "T_QUOTE") is True:
    parseStringExpr(tokenList) 
  elif match(tokenList, "T_RPAREN") is True:
    parseBooleanExpr(tokenList)
  elif match(tokenList, "T_ID") is True:
    parseID(tokenList)
  else:
    printErrorStmt(tokenList, "T_ID")
  cst.endChildren()

def parseBooleanExpr(tokenList):
  global rowToken
  cst.addNodeDef("BooleanExpr", "branch")
  printstmt.outerStmt[rowToken].append("parseBooleanExpr()")
  if match(tokenList, "T_LPAREN") is True:
    printValidStmt(tokenList, "T_LPAREN")
    consumeToken(tokenList)
    parseExpr(tokenList)
    parseBoolOp(tokenList)
    parseExpr(tokenList)
    if match(tokenList, "T_RPAREN") is True:
      printValidStmt(tokenList, "T_RPAREN")
      consumeToken(tokenList)
    else:
      printErrorStmt(tokenList, "T_RPAREN")
  else:
    printErrorStmt(tokenList, "this is wrong")
  cst.endChildren()

def parseStringExpr(tokenList):
  global rowToken
  cst.addNodeDef("StringExpr", "branch")
  printstmt.outerStmt[rowToken].append("parseStringExpr()")
  if match(tokenList, "T_QUOTE") is True:
    printValidStmt(tokenList, "T_QUOTE")
    consumeToken(tokenList)
    parseCharList(tokenList) 
    if match(tokenList, "T_QUOTE") is True:
      printValidStmt(tokenList, "T_QUOTE")
      consumeToken(tokenList)
  else: 
    printstmt.outerStmt[rowToken].append("parse string wrong")
  cst.endChildren()

def parseIntExpr(tokenList):
  global rowToken
  cst.addNodeDef("IntExpr", "branch")
  printstmt.outerStmt[rowToken].append("parseIntExpr()")
  if match(tokenList, "T_DIGIT") is True:
    printValidStmt(tokenList, "T_DIGIT")
    consumeToken(tokenList)
    if match(tokenList, "T_OP") is True:
      printValidStmt(tokenList, "T_OP")
      consumeToken(tokenList)
      parseExpr(tokenList)
  else:
    printErrorStmt(tokenList, "T_DIGIT")
  cst.endChildren()

def parseStatement(tokenList):
  cst.addNodeDef("Statement", "branch")
  global rowToken, columnToken
  notVal = False
  # If print("parseStatement()") is not in individual
  # statements, it will print out countless parseStatement()
  if match(tokenList, "T_PRINT") is True:
    printstmt.outerStmt[rowToken].append("parseStatement()")
    notVal = True
    parsePrint(tokenList)
  elif match(tokenList, "T_ID") is True:
    printstmt.outerStmt[rowToken].append("parseStatement()")
    notVal = True
    parseAssignment(tokenList)
  elif match(tokenList, "T_TYPE") is True:
    printstmt.outerStmt[rowToken].append("parseStatement()")
    notVal = True
    parseVarDecl(tokenList)
  elif match(tokenList, "T_WHILE") is True:
    printstmt.outerStmt[rowToken].append("parseStatement()")
    notVal = True
    parseWhile(tokenList)
  elif match(tokenList, "T_IF") is True:
    printstmt.outerStmt[rowToken].append("parseStatement()")
    notVal = True
    parseIf(tokenList)
  elif match(tokenList, "T_LBRACE") is True:
    printstmt.outerStmt[rowToken].append("parseStatement()")
    notVal = True
    parseBlock(tokenList)
  else: # It will do nothing because statementList allows epsilon
    notVal = False
  cst.endChildren()
  return notVal
  
def parseStatementList(tokenList):
  cst.addNodeDef("StatementList", "branch")
  if parseStatement(tokenList) is True:
    printstmt.outerStmt[rowToken].append("parseStatementList()")
    parseStatement(tokenList)
    parseStatementList(tokenList)
  cst.endChildren()
  if match(tokenList, "T_RBRACE") is True:
    printValidStmt(tokenList, "T_RBRACE")
    consumeToken(tokenList)

def parseBlock(tokenList):
  cst.addNodeDef("Block", "branch")
  if match(tokenList, "T_LBRACE") is True:
    printValidStmt(tokenList, "T_LBRACE")
    consumeToken(tokenList)
    printstmt.outerStmt[rowToken].append("parseBlock()")
    # cst.addNode()
    if parseStatement(tokenList) is True:
      parseStatementList(tokenList)
  cst.endChildren()
  if match(tokenList, "T_RBRACE") is True:
    printValidStmt(tokenList, "T_RBRACE")
    consumeToken(tokenList)

def parseIf(tokenList):
  global rowToken
  cst.addNodeDef("IF", "branch")
  printstmt.outerStmt[rowToken].append("parseIf()")
  if match(tokenList, "T_IF") is True:
    printValidStmt(tokenList, "T_IF")
    consumeToken(tokenList)
    parseBooleanExpr(tokenList)
    parseBlock(tokenList)
  else:
    printErrorStmt(tokenList, "T_IF")
  cst.endChildren()

def parseWhile(tokenList):
  global rowToken
  cst.addNodeDef("WHILE", "branch")
  printstmt.outerStmt[rowToken].append("parseWhile()")  
  if match(tokenList, "T_WHILE") is True:
    printValidStmt(tokenList, "T_WHILE")
    consumeToken(tokenList)
    parseBooleanExpr(tokenList)
    parseBlock(tokenList)
  else:
    printErrorStmt(tokenList, "T_WHILE")
  cst.endChildren()

def parseVarDecl(tokenList):
  global rowToken
  cst.addNodeDef("VarDecl", "branch")
  printstmt.outerStmt[rowToken].append("parseVarDecl()")
  if match(tokenList, "T_TYPE") is True:
    printValidStmt(tokenList, "T_TYPE")
    consumeToken(tokenList)
    parseID(tokenList)
  else:
    printErrorStmt(tokenList, "VARDECL")
  cst.endChildren()

def parseAssignment(tokenList):
  global rowToken
  cst.addNodeDef("Assignment", "branch")
  printstmt.outerStmt[rowToken].append("parseAssignment()")
  if match(tokenList, "T_ID") is True or match(tokenList, "T_ASSIGN") is True:
    # parseID()
    if match(tokenList, "T_ID") is True:
      parseID(tokenList)
    elif match(tokenList, "T_ASSIGN") is True: 
      printValidStmt(tokenList, "T_ASSIGN")
      consumeToken(tokenList)
      parseExpr(tokenList)
  else:
    printErrorStmt(tokenList, "parseAssignment")
  cst.endChildren()

def parsePrint(tokenList):
  global rowToken
  cst.addNodeDef("PRINT", "branch")
  printstmt.outerStmt[rowToken].append("parsePrint()")
  if match(tokenList, "T_PRINT") is True:
    printValidStmt(tokenList, "T_PRINT")
    consumeToken(tokenList)
    if match(tokenList, "T_LPAREN") is True:
      printValidStmt(tokenList, "T_LPAREN")
      consumeToken(tokenList)
      parseExpr(tokenList)
    else:
      printErrorStmt(tokenList, "T_LPARENT")
    if match(tokenList, "T_RPAREN") is True:
      printValidStmt(tokenList, "T_RPAREN")
      consumeToken(tokenList)
    else:
      printErrorStmt(tokenList, "T_RPAREN")
  else:
    printErrorStmt(tokenList, "T_PRINT")
  cst.endChildren()

def parseProgram(tokenList):
  global rowToken, columnToken
  # print(type(printstmt.outerStmt[rowToken]))
  printstmt.outerStmt[rowToken].append("parseProgram()")
  cst.addNodeDef("Program", "branch")
  # for c in cst:
  cst.endChildren()
  # print(cst.toString() + "trying to print cst")
  if rowToken < len(tokenList):
    if match(tokenList, "T_LBRACE") is True:
      parseBlock(tokenList)
    if match(tokenList, "T_EOP") is True:
      printValidStmt(tokenList, "T_EOP")
      consumeToken(tokenList)
      printstmt.outerStmt[rowToken].append("\nCST")
      printstmt.outerStmt[rowToken].append(cst.toString())
      # Once it reaches EOP, move to the next row of the 2D array
      rowToken+=1
      # Set columnToken to zero to start from the beginning of the row
      columnToken=0
      # driver.letsDrive()
      # To avoid out of range
      # printParzer()
      if rowToken < len(tokenList):
        parse(tokenList)

def parse(tokenList):
  global rowToken, columnToken
  print(rowToken, columnToken)
  printstmt.outerStmt[rowToken].append("\nPARSER")
  # printstmt.outerStmt[rowToken].append("\nProgram " , programNumber , " starting....")
  if match(tokenList, "ERROR") is True:
    printstmt.outerStmt[rowToken].append("Parser: Skipped due to Lexer error(s)")
    if rowToken < len(tokenList):
      rowToken+=1 # Moving onto next program
      columnToken=0
      parse(tokenList)
      # lex.printLex(tokenList)
  else:
    cst.addNodeDef("Root", "branch")
    parseProgram(tokenList)

# print(cst)
