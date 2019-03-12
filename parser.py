import token
import re
import lex
import regex

EOP = "$"
tokens = ""
# global tokenIndex
tokenIndex = 0
currentToken = ""

# Opening as read mode to read the test files
open_file = open("test_alan.txt", "r")
# Creating list of individual contents in the file
listFile = list(open_file.read())
# Close file
open_file.close()

tokenList = lex.lex(listFile)

print("\nPARSER")
i=0
while i < len(tokenList):
  print(tokenList[i].value)
  # print(token.lineList[i])  
  i+=1  

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
  print("Expected ", expectedToken,  " but found " ,  tokenList[tokenIndex].kind , " with value '" ,  tokenList[tokenIndex].value , "' on line " ,  tokenList[tokenIndex].lineNum)

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
  if match(r"print") is True and match(r"(") is True and parseExpr() and match(r")") is True:
    print("parsePrint()")
  else:
    printErrorStmt("print(Expr)")

def parseStatementList():
  parseStatement()
  parseStatementList()

def parseBlock():
  if match("LEFT BRACE") is True:
    parseStatementList()
    if match("RIGHT BRACE") is True: 
      print("true right brace it is")
    print("true")
  else:
    if match("LEFT BRACE") is False:
      expectedToken = "LEFT BRACE"
      print("Expected ", expectedToken,  " but found " ,  tokenList[tokenIndex].kind , " with value '" ,  tokenList[tokenIndex].value , "' on line " ,  tokenList[tokenIndex].lineNum)
    print("error")
  # match("LEFT BRACE")
  # parseStatementList()
  # match("RIGHT BRACE")

def parseStatement():
  if parsePrint() is True or parseAssignment() is True:
    parsePrint()
    parseAssignment()
    parseVarDecl()
    parseWhile()
    parseIf()
    parseBlock()

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

parse()