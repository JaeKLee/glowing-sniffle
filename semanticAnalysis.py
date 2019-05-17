import printstmt
import astTree
import re
import symbolTree

# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
warningCounter = 0
errorCounter = 0
scope = -1
ast = astTree.Tree()
scopeTree = symbolTree.Tree()

def match(tokenList, expectedToken):
  global rowToken, columnToken
  notVal = False
  if rowToken < len(tokenList):
    if expectedToken == tokenList[rowToken][columnToken].kind:
      notVal = True  
  return notVal

def consumeToken(tokenList):
  global rowToken, columnToken
  # ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
  if rowToken < len(tokenList):
    columnToken+=1

def findVariable(tokenList, node):
  global rowToken, columnToken
  notVal = False
  # if tokenList[rowToken][columnToken].kind == "T_ID":
  #   printstmt[rowToken][columnToken]
  if node.parent is None:
    if match(tokenList, "T_ID") is True:
      printstmt.outerStmt[rowToken].append("No such variable is detected")
      notVal = False
  else:
    if node.dicto.get(tokenList[rowToken][columnToken].value):
      notVal = True
      vari = node.name
    else:
      if tokenList[rowToken][columnToken].kind == "T_ID":
        printstmt.outerStmt[rowToken][columnToken] = "No such variable is detected"
      if findVariable(tokenList, node.parent):
        notVal = True 
      else:
        notVal = False
  return notVal

def getVariable(tokenList, node, columnToken):
  global rowToken
  if node.paren is None:
    val = None
  else:
    if any(len(counts) > 0 for counts in node.dicto.get(tokenList[rowToken][columnToken].value)):
      val = node.dicto.get(tokenList[rowToken][columnToken].value)
    else:
      if findVariable(tokenList,node.parent) is True:
        val = getVariable(tokenList, node.parent)
      else:
        val = None

#-------------------------------------------------Checking--------------------------------------------------------------------------------

def checkID(tokenList):
  global rowToken, columnToken
  vals = getVariable(tokenList, scopeTree.cur, columnToken-2)
  vals2 = getVariable(tokenList, scopeTree.cur, columnToken)
  if tokenList[rowToken][columnToken-1].kind == "T_ASSIGN":
    if vals.kind != vals2.kind:
      printstmt.outerStmt[rowToken].append("Type mismatch: ID does not match with type ")
  else:
    if tokenList[rowToken][columnToken-1].kind == "T_OP":
      if vals2.value != "int":
        printstmt.outerStmt[rowToken].append("Type mismatch: cannot add ID")
      else:
        if tokenList[rowToken][columnToken-1].kind == "T_BOOLOP":
          if vals is not None:
            if vals.kind != vals2.kind:
              printstmt.outerStmt[rowToken].append("Type mismatch: ID type")
          else:
            if tokenList[rowToken][columnToken-2].kind == "T_QUOTE" and vals2.value != "string":
              printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare a string to non-string ID")
            else:
              if tokenList[rowToken][columnToken-2].kind == "T_DIGIT" and vals2.value != "int":
                printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare integer to non-integer ID")
              elif tokenList[rowToken][columnToken-2].kind == "T_RPAREN" or tokenList[rowToken][columnToken-2].kind == "T_BOOLVAL" and vals2.value != "boolean":
                printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare boolean to non-boolean ID")

def checkBool(tokenList):
  global rowToken, columnToken
  val = getVariable(tokenList, scopeTree, columnToken-2)
  if tokenList[rowToken][columnToken-1].kind == "T_ASSIGN":
    if val.value != "boolean":
      printstmt.outerStmt[rowToken].append("Type mismatch: on ID and boolean ")
  else:
    if tokenList[rowToken][columnToken-1].kind == "T_OP":
      printstmt.outerStmt[rowToken].append("Type mismatch: cannot add boolean to int")
    else:
      if tokenList[rowToken][columnToken-1].kind == "T_BOOLOP":
        if val is not None:
          if val.value == "string":
            printstmt.outerStmt[rowToken].append("Type mismatch: cannot add boolean to string")
          elif val.value == "int":
            printstmt.outerStmt[rowToken].append("Type mismatch: cannot add boolean to int")
        else:
          if tokenList[rowToken][columnToken-2].kind == "T_QUOTE":
            printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare a string to boolean")
          else:
            if tokenList[rowToken][columnToken-2].kind == "T_DIGIT":
              printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare integer to boolean")
            
def checkString(tokenList):
  val = getVariable(tokenList, scopeTree, columnToken-2)
  if tokenList[rowToken][columnToken-1].kind == "T_ASSIGN":
    if val.value != "string":
      printstmt.outerStmt[rowToken].append("Type mismatch: on ID and string ")

  else:
    if tokenList[rowToken][columnToken-1].kind == "T_OP":
      printstmt.outerStmt[rowToken].append("Type mismatch: cannot add integer to string")
    else:
      if tokenList[rowToken][columnToken-1].kind == "T_BOOLOP":
        if val is not None:
          if val.value == "int":            
            printstmt.outerStmt[rowToken].append("Type mismatch: cannot add compare integer to string")
          elif val.value == "boolean":
            printstmt.outerStmt[rowToken].append("Type mismatch: cannot add compare boolean to string")
        else:
          if tokenList[rowToken][columnToken-2].kind == "T_DIGIT":
            printstmt.outerStmt[rowToken].append("Type mismatch: cannot add compare integer to string")
          elif tokenList[rowToken][columnToken-2].kind == "T_RPAREN" or tokenList[rowToken][columnToken-2].kind == "T_BOOLVAL":
            printstmt.outerStmt[rowToken].append("Type mismatch: cannot add compare boolean to string")
    
def checkInteger(tokenList):
  val = getVariable(tokenList, scopeTree, columnToken-2)
  if tokenList[rowToken][columnToken-1].kind == "T_ASSIGN":
    if val.value != "int":
      printstmt.outerStmt[rowToken].append("Type mismatch: on ID and integer ")
  else:
    # if tokenList[rowToken][columnToken-1].kind == "T_OP":
    # else:
    if tokenList[rowToken][columnToken-1].kind == "T_BOOLOP":
      if val is not None:
        if val.value == "string":            
          printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare string to integer")
        elif val.value == "boolean":
          printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare boolean to integer")
      else:
        if tokenList[rowToken][columnToken-2].kind == "T_QUOTE":
          printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare string to integer")
        elif tokenList[rowToken][columnToken-2].kind == "T_RPAREN" or tokenList[rowToken][columnToken-2].kind == "T_BOOLVAL":
          printstmt.outerStmt[rowToken].append("Type mismatch: cannot compare boolean to integer")

# --------------------------------------------------------PARSING-------------------------------------------------------------------------

def parseCharList(tokenList):
  global rowToken, columnToken
  if match(tokenList, "T_CHAR") is True:
    ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
    parseCharList(tokenList)
    ast.endChildren()

def parseID(tokenList):
  global rowToken, columnToken
  if findVariable(tokenList, scopeTree.cur) is True:
    val = getVariable(tokenList, scopeTree.cur, columnToken)
    if ast.cur.name == "Assignment" and val is not None:
      val.initialized = True
    else:
      if ast.cur.name != "VarDecl" and val is not None:
        val.used = True
  else:
    printstmt.outerStmt[rowToken].append("ERROR - '" + tokenList[rowToken][columnToken].value + "' undeclared" )
  ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
  consumeToken(tokenList)
  if tokenList[rowToken][columnToken].value == "=":
    parseAssignment(tokenList)

def parseExpr(tokenList):
  global rowToken
  if match(tokenList, "T_DIGIT") is True:
    parseIntExpr(tokenList)
  elif match(tokenList, "T_QUOTE") is True:
    parseStringExpr(tokenList) 
  elif match(tokenList, "T_RPAREN") is True:
    parseBooleanExpr(tokenList)
  elif match(tokenList, "T_ID") is True:
    parseID(tokenList)
  else:
    consumeToken(tokenList)
  # ast.endChildren()

def parseBooleanExpr(tokenList):
  global rowToken, columnToken
  ast.addNodeDef("BooleanExpr", "branch")
  if match(tokenList, "T_LPAREN") is True:
    if tokenList[rowToken][columnToken+2].value == "==":
      ast.addNodeDef("EQUAL", "branch")
    if tokenList[rowToken][columnToken+2].value == "!=":
      ast.addNodeDef("NotEQUAL", "branch")
    consumeToken(tokenList)
    parseExpr(tokenList)
    consumeToken(tokenList)
    parseExpr(tokenList)
    if match(tokenList, "T_RPAREN") is True:
      consumeToken(tokenList)
    ast.endChildren()
  elif match(tokenList, "T_BOOLVAL") is True:
    ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
  else:
    errorCounter+=1
  
def parseStringExpr(tokenList):
  global rowToken
  if match(tokenList, "T_QUOTE") is True:
    consumeToken(tokenList)
    parseCharList(tokenList) 
    if match(tokenList, "T_QUOTE") is True:
      consumeToken(tokenList)

def parseIntExpr(tokenList):
  global rowToken, columnToken
  if tokenList[rowToken][columnToken+1].kind == "T_OP":
    ast.addNodeDef("ADD", "branch")
  if match(tokenList, "T_DIGIT") is True:
    ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
  if match(tokenList, "T_OP") is True:
      # ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
    parseExpr(tokenList)
    ast.endChildren()

def parseStatement(tokenList):
  notVal = False
  # If print("parseStatement()") is not in individual
  # statements, it will print out countless parseStatement()
  if match(tokenList, "T_PRINT") is True:
    notVal = True
    parsePrint(tokenList)
  elif match(tokenList, "T_ID") is True:
    notVal = True
    parseAssignment(tokenList)
  elif match(tokenList, "T_TYPE") is True:
    notVal = True
    parseVarDecl(tokenList)
  elif match(tokenList, "T_WHILE") is True:
    notVal = True
    parseWhile(tokenList)
  elif match(tokenList, "T_IF") is True:
    notVal = True
    parseIf(tokenList)
  elif match(tokenList, "T_LBRACE") is True:
    notVal = True
    parseBlock(tokenList)
  else: # It will do nothing because statementList allows epsilon
    notVal = False
  # ast.endChildren()
  # return notVal
  
def parseStatementList(tokenList):
  if match(tokenList, "T_RBRACE") is False:
    parseStatement(tokenList)
    parseStatementList(tokenList)
    ast.endChildren()
  # if match(tokenList, "T_PRINT") is True or match(tokenList, "T_ID") is True or match(tokenList, "T_TYPE") is True or match(tokenList, "T_WHILE") is True or match(tokenList, "T_IF") is True or match(tokenList, "T_LBRACE") is True:
  #   parseStatement(tokenList)
  #   parseStatementList(tokenList)
  # ast.endChildren()
  # if match(tokenList, "T_PRINT") is True or match(tokenList, "T_ID") is True or match(tokenList, "T_TYPE") is True or match(tokenList, "T_WHILE") is True or match(tokenList, "T_IF") is True or match(tokenList, "T_LBRACE") is True:
  #   parseStatement(tokenList)
  #   parseStatementList(tokenList)

def parseBlock(tokenList):
  global scope
  scope+=1
  scopeTree.addNodeDef("Scope " + str(scope), "branch")
  ast.addNodeDef("Block", "branch")
  if match(tokenList, "T_LBRACE") is True:
    consumeToken(tokenList)
  parseStatementList(tokenList)
  if match(tokenList, "T_RBRACE") is True:
    consumeToken(tokenList)
  ast.endChildren()
  scopeTree.endChildren()

def parseIf(tokenList):
  global rowToken
  ast.addNodeDef("IF", "branch")
  if match(tokenList, "T_IF") is True:
    consumeToken(tokenList)
    parseBooleanExpr(tokenList)
    parseBlock(tokenList)
  ast.endChildren()

def parseWhile(tokenList):
  global rowToken
  ast.addNodeDef("WHILE", "branch")
  if match(tokenList, "T_WHILE") is True:
    consumeToken(tokenList)
    parseBooleanExpr(tokenList)
    parseBlock(tokenList)
  ast.endChildren()
 
def parseVarDecl(tokenList):
  global rowToken, columnToken
  ast.addNodeDef("VarDecl", "branch")
  # print(type(scopeTree.cur.dicto))
  if scopeTree.cur.dicto.get(tokenList[rowToken][columnToken+1].value) is not None:
    printstmt.outerStmt[rowToken].append("Redeclaration is not allowed")
  else:
    getType = tokenList[rowToken][columnToken].value
    getLineNum = tokenList[rowToken][columnToken+1].lineNum
    varInfo = {'type': getType, 'lineNum':getLineNum, 'used': False, 'initialized': False, 'declared': True}
    scopeTree.cur.dicto = {tokenList[rowToken][columnToken+1].value: varInfo}
  if match(tokenList, "T_TYPE") is True:
    ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
    parseID(tokenList)
  ast.endChildren()

def parseAssignment(tokenList):
  ast.addNodeDef("Assignment", "branch")
  if match(tokenList, "T_ID") is True or match(tokenList, "T_ASSIGN") is True:
    # parseID()
    if match(tokenList, "T_ID") is True:
      parseID(tokenList)
    elif match(tokenList, "T_ASSIGN") is True: 
      consumeToken(tokenList)
      parseExpr(tokenList)
  ast.endChildren()

def parsePrint(tokenList):
  ast.addNodeDef("PRINT", "branch")
  if match(tokenList, "T_PRINT") is True:
    consumeToken(tokenList)
    if match(tokenList, "T_LPAREN") is True:
      consumeToken(tokenList)
      parseExpr(tokenList)
    else:
      consumeToken(tokenList)
    if match(tokenList, "T_RPAREN") is True:
      consumeToken(tokenList)
  ast.endChildren()

def parseProgram(tokenList):
  global rowToken, columnToken, ast, scopeTree
  ast.addNodeDef("Program", "branch")
  if rowToken < len(tokenList):
    if match(tokenList, "T_LBRACE") is True:
      parseBlock(tokenList)
    if match(tokenList, "T_EOP") is True:
      consumeToken(tokenList)
      printstmt.outerStmt[rowToken].append("\nAST")
      printstmt.outerStmt[rowToken].append(ast.toString())
      printstmt.outerStmt[rowToken].append("\nSymbol Table")
      printstmt.outerStmt[rowToken].append(scopeTree.toString())
      # Once it reaches EOP, move to the next row of the 2D array
      rowToken+=1
      # Set columnToken to zero to start from the beginning of the row
      columnToken = 0
      warningCounter = 0
      errorCounter = 0
      scopeLevel = 0
      scope = 0
      ast = astTree.Tree()
      scopeTree = symbolTree.Tree()
      # To avoid out of range
      if rowToken < len(tokenList):
        semanticAnalysis(tokenList)
  # ast.endChildren()

def semanticAnalysis(tokenList):
  import parzer
  global rowToken,columnToken, errorCounter
  # print("this is to test if semantic analysis is being called properly. I can't see the word test without writing this long sentence.")
  # printstmt.outerStmt[rowToken].append("\nSemantic Analysis")
  # if match(tokenList, "ERROR") is True:
  # print(rowToken)
  # printstmt.outerStmt[rowToken].append("\nSemantic Analysis")
  # for i in parzer.test:
  # print(tokenList[rowToken][columnToken ])
  i = 0
  # while i < len(tokenList):
    # global rowToken, columnToken
  # print(str(parzer.test[i]) +  "in semantic")
  # if parzer.test[i] > 0:
  # if parzer.errorCounter > 0:
  # print(tokenList[rowToken][columnToken])
  # if re.search(r"ERROR", tokenList[rowToken][columnToken]):
  # if match(tokenList, "ERROR") is True:
  if tokenList is None:
    if rowToken < len(tokenList):
      printstmt.outerStmt[rowToken].append("\nSemantic Analysis" + str(parzer.test[i]))
      printstmt.outerStmt[rowToken].append("Semantic Analysis: Skipped due to Parser error(s)")
      rowToken+=1 # Moving onto next program
      # programNumber+=1
      # columnToken=0
      semanticAnalysis(tokenList)
  else:
    if rowToken < len(tokenList):
      printstmt.outerStmt[rowToken].append("\nSemantic Analysis")
      ast.addNodeDef("Root", "branch")
      printstmt.outerStmt[rowToken].append("Semantic Analysis... Commence!")
      parseProgram(tokenList)
    # i+=1
