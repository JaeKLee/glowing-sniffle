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
symbolTable = symbolTree.Tree()

def match(tokenList, expectedToken):
  global rowToken, columnToken
  notVal = False
  if rowToken < len(tokenList):
    if expectedToken == tokenList[rowToken][columnToken].kind:
      notVal = True
  return notVal

def consumeToken(tokenList):
  global rowToken, columnToken
  if rowToken < len(tokenList):
    columnToken+=1

def findVariable(tokenList, node):
  global rowToken, columnToken
  notVal = False
  if match(tokenList, "T_ID") is True:
    if node.parent is None:
      if node.dicto.get(tokenList[rowToken][columnToken].value) is not None:
        printstmt.outerStmt[rowToken].append("Found " + tokenList[rowToken][columnToken].value + " at " + node.name + " in line " + str(tokenList[rowToken][columnToken].lineNum))
        notVal = True
    else:
      if node.dicto.get(tokenList[rowToken][columnToken].value) is not None:
        printstmt.outerStmt[rowToken].append("Found " + tokenList[rowToken][columnToken].value + " at " + node.name + " in line " + str(tokenList[rowToken][columnToken].lineNum))
        notVal = True
      else:
        if match(tokenList, "T_ID") is True: #tokenList[rowToken][columnToken].kind == "T_ID":
          printstmt.outerStmt[rowToken].append("Variable '" + tokenList[rowToken][columnToken].value + "' is not detected at " + node.name)
        if findVariable(tokenList, node.parent) is True:
          notVal = True
        else:
          notVal = False
  else:
    raise Exception("Token '" + tokenList[rowToken][columnToken].value + "' is not a variable")
  return notVal

def getVariable(tokenList, node, columnToken):
  global rowToken
  if node.parent is None:
    val = None
  else:
    if node.dicto.get(tokenList[rowToken][columnToken].value) is not None:
      val = node.dicto.get(tokenList[rowToken][columnToken].value)
    else:
      if findVariable(tokenList,node.parent) is True:
        val = getVariable(tokenList, node.parent, columnToken)
      else:
        val = None

#-------------------------------------------------Checking--------------------------------------------------------------------------------

def checkID(tokenList):
  global rowToken, columnToken
  vals = getVariable(tokenList, symbolTable.cur, columnToken-2)
  vals2 = getVariable(tokenList, symbolTable.cur, columnToken)
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
  val = getVariable(tokenList, symbolTable, columnToken-2)
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
  val = getVariable(tokenList, symbolTable, columnToken-2)
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
  val = getVariable(tokenList, symbolTable.cur, columnToken-2)
  if tokenList[rowToken][columnToken-1].kind == "T_ASSIGN":
    if val.value != "int":
      printstmt.outerStmt[rowToken].append("Type mismatch: on ID and integer ")
  else:
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
  if findVariable(tokenList, symbolTable.cur) is True:
    val = getVariable(tokenList, symbolTable.cur, columnToken)
    if ast.cur.name == "Assignment" and val is not None:
      val.initialized = True
    else:
      if ast.cur.name != "VarDecl" and val is not None:
        val.used = True
  else:
    raise Exception("Undeclared '" + tokenList[rowToken][columnToken].value + "' at " + str(tokenList[rowToken][columnToken].lineNum))
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
    raise Exception("Error in Expression at " + str(tokenList[rowToken][columnToken].lineNum))

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
    raise Exception("Error in Boolean Expression at " + str(tokenList[rowToken][columnToken].lineNum))
  
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
  else:
    raise Exception("Error in Integer Expression at " + str(tokenList[rowToken][columnToken].lineNum))
  if match(tokenList, "T_OP") is True:
    consumeToken(tokenList)
    parseExpr(tokenList)
    ast.endChildren()

def parseStatement(tokenList):
  global errorCounter
  # If print("parseStatement()") is not in individual
  # statements, it will print out countless parseStatement()
  if match(tokenList, "T_PRINT") is True:
    parsePrint(tokenList)
  elif match(tokenList, "T_ID") is True:
    parseAssignment(tokenList)
  elif match(tokenList, "T_TYPE") is True:
    parseVarDecl(tokenList)
  elif match(tokenList, "T_WHILE") is True:
    parseWhile(tokenList)
  elif match(tokenList, "T_IF") is True:
    parseIf(tokenList)
  elif match(tokenList, "T_LBRACE") is True:
    parseBlock(tokenList)
  else:
    raise Exception("Error in Statement at " + str(tokenList[rowToken][columnToken].lineNum))
  # ast.endChildren()
  # return notVal
  
def parseStatementList(tokenList):
  if match(tokenList, "T_RBRACE") is False:
    parseStatement(tokenList)
    parseStatementList(tokenList)
    ast.endChildren()

def parseBlock(tokenList):
  global scope
  scope+=1
  symbolTable.addNodeDef("Scope " + str(scope), "branch")
  ast.addNodeDef("Block", "branch")
  consumeToken(tokenList) # Skipping LBRACE
  if match(tokenList, "T_RBRACE") is False:
    parseStatementList(tokenList)
  consumeToken(tokenList) # Skipping RBRACE
  ast.endChildren()
  symbolTable.endChildren()

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
  if symbolTable.cur.dicto.get(tokenList[rowToken][columnToken+1].value) is None:
    getType = tokenList[rowToken][columnToken].value
    getLineNum = tokenList[rowToken][columnToken+1].lineNum
    varInfo = {'type': getType, 'lineNum':getLineNum, 'used': False, 'initialized': False, 'declared': True}
    symbolTable.cur.dicto.setdefault(tokenList[rowToken][columnToken+1].value,varInfo)
  else:
    raise Exception("Redeclaration of '" + tokenList[rowToken][columnToken].value + "' is not allowed. Please revise at line number " + str(tokenList[rowToken][columnToken].lineNum))
  if match(tokenList, "T_TYPE") is True:
    ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
    parseID(tokenList)
  else:
    raise Exception("Error in Variable Declaration at " + str(tokenList[rowToken][columnToken].lineNum))
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
  global rowToken, columnToken, ast, symbolTable
  ast.addNodeDef("Program", "branch")
  if rowToken < len(tokenList):
    if match(tokenList, "T_LBRACE") is True:
      parseBlock(tokenList)
    if match(tokenList, "T_EOP") is True:
      consumeToken(tokenList)
      printstmt.outerStmt[rowToken].append("\nAST")
      printstmt.outerStmt[rowToken].append(ast.toString())
      printstmt.outerStmt[rowToken].append("\nSymbol Table")      
      printstmt.outerStmt[rowToken].append("\nName    Type       Scope       Line")
      printstmt.outerStmt[rowToken].append(symbolTable.toString())
      # Once it reaches EOP, move to the next row of the 2D array
      rowToken+=1
      # Set columnToken to zero to start from the beginning of the row
      columnToken = 0
      scopeLevel = 0
      scope = 0
      ast = astTree.Tree()
      symbolTable = symbolTree.Tree()
      # To avoid out of range
      if rowToken < len(tokenList):
        semanticAnalysis(tokenList)
    else:
          raise Exception("Error in Program at " + str(tokenList[rowToken][columnToken].lineNum))

def semanticAnalysis(tokenList):
  global rowToken,columnToken, ast
  if rowToken < len(tokenList):
    printstmt.outerStmt[rowToken].append("\nSemantic Analysis")
  try:
    if rowToken < len(tokenList):
      ast.addNodeDef("Root", "branch")
      parseProgram(tokenList)
  except Exception as e:
    printstmt.outerStmt[rowToken].append("Error in Semantic Analysis, not moving to Code Gen")
    printstmt.outerStmt[rowToken].append(e)
    rowToken+=1
    columnToken=0
    scope = 0
    ast = astTree.Tree()
    symbolTable.cur.dicto.clear()
    semanticAnalysis(tokenList)