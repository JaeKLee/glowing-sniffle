import printstmt
import astTree
import re
import symbol

# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
warningCounter = 0
errorCounter = 0
scopeLevel = 0
scope = 0
ast = astTree.Tree()
# symbolTree = treeSymbol.Tree()
symbolTable = []

class Symbol:
  def __init__(self, name, typeName=None):
    self.name = name
    self.type = typeName
    self.category = category

def createSymbol(name, typeName):
  symbols = Symbol(name, typeName)
  symbolTable.append(symbols)




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

def parseCharList(tokenList):
  global rowToken, columnToken
  if match(tokenList, "T_CHAR") is True:
    # ast.addNodeDef("CHARLIST", "branch")
    ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
    consumeToken(tokenList)
    # parseChar(tokenList)
    parseCharList(tokenList)
  # elif tokenList[rowToken][columnToken].value == " ":
  #   parseCharList(tokenList)
  #   consumeToken
    ast.endChildren()

def parseID(tokenList):
  global rowToken, columnToken
  ast.addNodeDef(tokenList[rowToken][columnToken].value, "leaf")
  # ast.endChildren()
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
      ast.addNodeDef("!EQUAL", "branch")
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
  # ast.endChildren()

def parseIntExpr(tokenList):
  global rowToken, columnToken
  # ast.addNodeDef("IntExpr", "branch")
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
  global scope, scopeLevel
  scope+=1
  scopeLevel+=1
  ast.addNodeDef("Block", "branch")
  if match(tokenList, "T_LBRACE") is True:
    consumeToken(tokenList)
  parseStatementList(tokenList)
  if match(tokenList, "T_RBRACE") is True:
    consumeToken(tokenList)
  ast.endChildren()

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
  global rowToken, columnToken, ast
  ast.addNodeDef("Program", "branch")
  if rowToken < len(tokenList):
    if match(tokenList, "T_LBRACE") is True:
      parseBlock(tokenList)
    if match(tokenList, "T_EOP") is True:
      consumeToken(tokenList)
      printstmt.outerStmt[rowToken].append("\nAST")
      printstmt.outerStmt[rowToken].append(ast.toString())
      printstmt.outerStmt[rowToken].append("--------------------------------------")
      printstmt.outerStmt[rowToken].append("Name      Type        Scope       Line")
      printstmt.outerStmt[rowToken].append("--------------------------------------")
      # Once it reaches EOP, move to the next row of the 2D array
      rowToken+=1
      # Set columnToken to zero to start from the beginning of the row
      columnToken = 0
      warningCounter = 0
      errorCounter = 0
      scopeLevel = 0
      scope = 0
      ast = astTree.Tree()
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
