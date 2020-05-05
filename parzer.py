import tree
import printstmt

# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
errorCounter = 0
cst = tree.Tree()
test = []
test2 = []
  
def match(tokenList, expectedToken):
  global rowToken, columnToken
  notVal = False
  if rowToken < len(tokenList):
    if expectedToken == tokenList[rowToken][columnToken].kind:
      notVal = True  
  return notVal
  
def printErrorStmt(tokenList, expectedToken):
  global rowToken, columnToken
  raise Exception("Failed - Expected " + str(expectedToken) +  " but found " +  str(tokenList[rowToken][columnToken].kind) + " with value '" +  str(tokenList[rowToken][columnToken].value) + "' on line " +  str(tokenList[rowToken][columnToken].lineNum))

def printValidStmt(tokenList, expectedToken):
  global rowToken, columnToken
  if rowToken < len(tokenList):
    printstmt.outerStmt[rowToken].append("Valid - Expected " +  str(expectedToken) + " and got " +  str(tokenList[rowToken][columnToken].kind) + " with value '" +  str(tokenList[rowToken][columnToken].value) + "' on line " +  str(tokenList[rowToken][columnToken].lineNum))

def consumeToken(tokenList):
  global rowToken, columnToken
  cst.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
  if rowToken < len(tokenList):
    columnToken+=1

def parseBoolOp(tokenList):
  global rowToken, columnToken
  cst.addNodeDef("BoolOP", "branch")
  printstmt.outerStmt[rowToken].append("parseBoolOp()") 
  if match(tokenList, "T_BOOLOP") is True:
    printValidStmt(tokenList, "T_BOOLOP")
    consumeToken(tokenList)
  else:
    printErrorStmt(tokenList, "T_BOOLOP")
  cst.endChildren()

def parseChar(tokenList):
  if match(tokenList, "T_CHAR") is True:
    printstmt.outerStmt[rowToken].append("parseChar()")
    printValidStmt(tokenList, "T_CHAR")
    consumeToken(tokenList)
  elif tokenList[rowToken][columnToken].value == " ":
    printstmt.outerStmt[rowToken].append("parseChar()")
    printValidStmt(tokenList, "T_SPACE")
    consumeToken(tokenList)
  

def parseCharList(tokenList):
  global rowToken
  if match(tokenList, "T_CHAR") is True:
    cst.addNodeDef("CharList", "branch")
    printstmt.outerStmt[rowToken].append("parseCharList()")
    printValidStmt(tokenList, "T_CHAR")
    consumeToken(tokenList)
    parseCharList(tokenList)
    cst.endChildren()

def parseID(tokenList):
  printValidStmt(tokenList, "T_ID parseID")
  consumeToken(tokenList)
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
  elif match(tokenList, "T_LPAREN") is True or match(tokenList, "T_BOOLVAL") is True:
    parseBooleanExpr(tokenList)
  elif match(tokenList, "T_ID") is True:
    parseID(tokenList)
  else:
    printErrorStmt(tokenList, "T_DIGIT|T_QUOTE|T_LPAREN|T_ID")
  cst.endChildren()

def parseBooleanExpr(tokenList):
  global rowToken
  cst.addNodeDef("BooleanExpr", "branch")
  printstmt.outerStmt[rowToken].append("parseBooleanExpr()")
  if match(tokenList, "T_LPAREN") is True or match(tokenList, "T_BOOLVAL"):
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
    printErrorStmt(tokenList, "T_LPAREN")
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
    printErrorStmt(tokenList, "T_QUOTE")
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
  cst.endChildren()
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
  # return notVal
  
def parseStatementList(tokenList):
  cst.addNodeDef("StatementList", "branch")
  if match(tokenList, "T_PRINT") is True or match(tokenList, "T_ID") is True or match(tokenList, "T_TYPE") is True or match(tokenList, "T_WHILE") is True or match(tokenList, "T_IF") is True or match(tokenList, "T_LBRACE") is True:
    printstmt.outerStmt[rowToken].append("parseStatementList()")
    parseStatement(tokenList)
    parseStatementList(tokenList)
  cst.endChildren()
  if match(tokenList, "T_PRINT") is True or match(tokenList, "T_ID") is True or match(tokenList, "T_TYPE") is True or match(tokenList, "T_WHILE") is True or match(tokenList, "T_IF") is True or match(tokenList, "T_LBRACE") is True:
    printstmt.outerStmt[rowToken].append("parseStatementList()")
    parseStatement(tokenList)
    parseStatementList(tokenList)
  cst.endChildren()
  # else:
  #   printstmt.outerStmt[rowToken].append("Lambda")

def parseBlock(tokenList):
  global rowToken, columnToken
  cst.addNodeDef("Block", "branch")
  if match(tokenList, "T_LBRACE") is True:
    # cst.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    printstmt.outerStmt[rowToken].append("parseBlock()")
    printValidStmt(tokenList, "T_LBRACE")
    consumeToken(tokenList)
  else:
    printErrorStmt(tokenList, "T_LBRACE")
    # raise Exception("Error in Block")
  parseStatementList(tokenList)
 
  if match(tokenList, "T_RBRACE") is True:
    printValidStmt(tokenList, "T_RBRACE")
    consumeToken(tokenList)
  else:
    # raise Exception("Error in Block")
    printErrorStmt(tokenList, "T_RBRACE")
    # raise Exception('Whatever the error is'.format(tokenList[rowToken][columnToken].value))
    # if rowToken < len(tokenList):
    # parse(tokenList)
  cst.endChildren()

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
    # raise Exception("Error in If Statement")
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
    # raise Exception("Error in While Statement")
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
    # raise Exception("Error in VarDecl")
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
    # raise Exception("Error in Assignment")
  cst.endChildren()

def parsePrint(tokenList):
  global rowToken
  cst.addNodeDef("PRINT", "branch")
  printstmt.outerStmt[rowToken].append("parsePrint()")
  if match(tokenList, "T_PRINT") is True:
    printValidStmt(tokenList, "T_PRINT")
    consumeToken(tokenList)
    if match(tokenList, "T_LPAREN") is True:
      # cst.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
      printValidStmt(tokenList, "T_LPAREN")
      consumeToken(tokenList)
      parseExpr(tokenList)
    else:
      printErrorStmt(tokenList, "T_LPARENT")
      # raise Exception("Error in Print Statement")
    if match(tokenList, "T_RPAREN") is True:
      # cst.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
      printValidStmt(tokenList, "T_RPAREN")
      consumeToken(tokenList)
    else:
      printErrorStmt(tokenList, "T_RPAREN")
  else:
    printErrorStmt(tokenList, "T_PRINT")
  cst.endChildren()
test = []
def parseProgram(tokenList):
  global rowToken, columnToken, cst
  if rowToken < len(tokenList):
    if match(tokenList, "T_LBRACE") is True:
      printstmt.outerStmt[rowToken].append("parseProgram()")
      cst.addNodeDef("Program", "branch")      
      parseBlock(tokenList)
    else:
      printErrorStmt(tokenList, "T_LBRACE")  
    if match(tokenList, "T_EOP") is True:
      printValidStmt(tokenList, "T_EOP")
      consumeToken(tokenList)
      printstmt.outerStmt[rowToken].append("\nCST")
      printstmt.outerStmt[rowToken].append(cst.toString())
      cst = tree.Tree()
      rowToken+=1
      columnToken=0
      if rowToken < len(tokenList):
        printstmt.innerStmt = []
        parse(tokenList)
    return tokenList

def parse(tokenList):
  global rowToken, columnToken, cst
  try: 
    if rowToken < len(tokenList):
      printstmt.outerStmt[rowToken].append("\nPARSER")
      cst.addNodeDef("Root", "branch")
      parseProgram(tokenList)
      cst = tree.Tree()
  except Exception as e:
    if rowToken < len(tokenList):
      printstmt.outerStmt[rowToken].append(e)
      printstmt.outerStmt[rowToken].append("\nParse failed with 1 error")
      printstmt.outerStmt[rowToken].append("CZT zkipped cuz Parzer found za error(z)")
      printstmt.outerStmt[rowToken].append("Error in Parzer, not moving to Semantic Analysis and Code Gen")
      rowToken+=1 # Moving onto next program
      columnToken=0
      parse(tokenList)