import token
import re
import lex
import regex

EOP = "$"
tokens = ""
# global tokenIndex
tokenIndex = 0
currentToken = ""
errorCounter = 0

# Opening as read mode to read the test files
open_file = open("test_alan.txt", "r")
# Creating list of individual contents in the file
listFile = list(open_file.read())
# Close file
open_file.close()

tokenList = lex.lex(listFile)
print(len(tokenList))

print("\nPARSER")
# i=0
# while i < len(tokenList):
#   print(tokenList[i].value)
#   # print(token.lineList[i])  
#   i+=1  

def match(expectedToken):
  global tokenIndex
  notVal = False
  print(tokenList[tokenIndex].value)
  if expectedToken == tokenList[tokenIndex].value:
    notVal = True
  tokenIndex+=1  
  return notVal
  
def printErrorStmt(expectedToken):
  global tokenIndex    
  lastIndex = tokenIndex - 1
  print(tokenList[tokenIndex].value)
  # For errors, we skip to the end of the index, so parser doesn't continue
  while tokenList[tokenIndex].value != "$" and tokenIndex+1 < len(tokenList):
    tokenIndex+=1
  # Once it reaches the end, it will print out error messages
  if tokenList[tokenIndex].value == "$" and tokenIndex+1 < len(tokenList):
    print("Expected ", expectedToken,  " but found " ,  tokenList[tokenIndex].kind , " with value '" ,  tokenList[tokenIndex].value , "' on line " ,  tokenList[tokenIndex].lineNum)
    print("Parse failed with 1 error")
  


def parseOp():
  if match("+") is True: 
    print("parseOp()")
  else:
    printErrorStmt("+")

def parseBoolVal():
  if match(regex.digit) is True or match("true") is True:
    print("parseBoolVal")
  else: 
    printErrorStmt("false|true")

def parseBoolOp():
  if match("==") is True:
    print("parseBoolOp")
  else:
    printErrorStmt("==")
  if match("!=") is True:
    print("parseBoolOp()")
  else:
    printErrorStmt("!=")

def parseDigit(): 
  if match(r"[0-9]") is True:
    print("parseDigit()")
  else:
    printErrorStmt("digits")

def parseSpace():
  if match(r"\s") is True:
    print("parseSpace()")
  else:
    printErrorStmt("space")

def parseChar():
  if match(r"[a-z]") is True:
    print("parseChar()")

def parseType():
  if match("int"):
    print("parseType")
  else:
    printErrorStmt("T_INT")
  if match("string"):
    print("parseType")
  else:
    printErrorStmt("T_STRING")
  if match("boolean"):
    print("parseType")
  else:
    printErrorStmt("T_BOOLEAN")

def parseCharList():
  if parseChar() and parseCharList():
    print("parseCharList()")
  else: 
    printErrorStmt("T_CHAR")
  if parseSpace() and parseCharList():
    print("parseCharList()")
  else:
    printErrorStmt("T_SPACE")

def parseID():
  print("parseID()")
  parseChar()

def parseBooleanExpr():
  if match(r"(") is True and parseExpr() and parseBoolOp() and parseExpr() and match(r")") is True:
    print("parseBooleanExpr")
  else:
    printErrorStmt("this is wrong")

def parseStringExpr():
  if match(r"\"") is True and parseCharList() and match(r"\""):
    print("parseStringExpr()")
  else: 
    print("parsestring wrong")

def parseIntExpr():
  if parseDigit() and parseOp() and parseExpr():
    print("parseIntExpr()")
  else:
    printErrorStmt("digits or +")

def parseExpr():
  if parseStringExpr() or parseBooleanExpr() or parseID():
    print("parseExpr()")
  else: 
    printErrorStmt("that's not true")

def parseBlock():
  if match("{") is True:
    parseStatementList()
    if match("}") is True: 
      print("true right brace it is")
    print("true")
  else:
    if match("{") is False:
      printErrorStmt("{")
    elif match("}") is False:
      printErrorStmt("}")

def parseIf():
  if match("if") and parseBooleanExpr() and parseBlock():
    print("parseIf()")
  else:
    print("parseIf wrong")

def parseWhile():
  if match("while") and parseBooleanExpr() and parseBlock():
    print("parseWhile()")
  else:
    print("parseWhile wrong")

def parseVarDecl():
  if parseType() and parseID():
    print("parseVarDecl()")
  else:
    printErrorStmt("VARDECL")

def parseAssignment():
  if parseID() and match(r"=") is True and parseExpr():
    print("parseAssignment()")
  else:
    printErrorStmt("parseAssignment is wrong")

def parsePrint():
  if match(r"print") is True:
    if match(r"(") is True:
      parseExpr()
    if match(r")") is True:
      print("parsePrint()")
  else:
    print("parseprint error")
    printErrorStmt("print(Expr)")

def parseStatementList():
  if parseStatement() or parseStatementList():
    print("parseStatementList()")
  else:
    global tokenList
    tokenList+=1

def parseStatement():
  global tokenIndex
  if tokenList[tokenIndex].value == "print":
    print("parseStatement()")
    parsePrint()
  elif tokenList[tokenIndex].value == "==":
    print("parseStatement()")
    parseAssignment()
  # elif tokenList[tokenIndex].value == r"[int]|[string]|[boolean]|[a-z]": 
  elif tokenList[tokenIndex].value == "int" or tokenList[tokenIndex].value == "string" or tokenList[tokenIndex].value == "boolean":
    print("parseStatement()")
    parseVarDecl()
  elif tokenList[tokenIndex].value == "while":
    print("parseStatement()")
    parseWhile()
  elif tokenList[tokenIndex].value == "if":
    print("parseStatement()")
    parseIf()
  elif tokenList[tokenIndex].value == "{":
    print("parseStatement()")
    parseBlock()
  else:
    printErrorStmt("print|==|type|ID|while|if|{")
    
  # if match("print") is True:
  #   parsePrint()
  #   print("parseStatement()")
  # else:
  #   printErrorStmt("parsePrint()")

  # if match("")
  #   parseAssignment()
  #   print("parseStatement()")
  # else:
  #   printErrorStmt("parseAssignment()")

  # if parseVarDecl():
  #   print("parseStatement()")
  # else:
  #   printErrorStmt("parseVarDecl()")

  # if parseWhile():
  #   print("parseStatement()")
  # else:
  #   printErrorStmt("parseWhile")

  # if parseIf():
  #   print("parseStatement()")
  # else:
  #   printErrorStmt("parseIf")

  # if parseBlock():
  #   print("parseStatement()")
  # else:
  #   printErrorStmt("parseBlock")


def parseProgram():
  print("parseProgram()")
  parseBlock()

def parse():
  print("parse()")
  parseProgram()

# def getNextToken():
#   thisToken = EOP
#   if tokenIndex < tokens.length:
#     thisToken =  tokenList[tokenIndex]
#     print("Current token: ", thisToken)
#     tokenIndex+=1
#   return thisToken
i = 0
while i < len(tokenList):
  parse()
  i+=1