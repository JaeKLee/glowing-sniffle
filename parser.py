import token
import re
import lex
import regex
import tree

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
i=0
while i < len(tokenList):
  print(tokenList[i].value)
  # print(token.lineList[i])  
  i+=1  

def match(expectedToken):
  global tokenIndex
  notVal = False
  # print(tokenList[tokenIndex].kind)
  if expectedToken == tokenList[tokenIndex].kind:
    notVal = True  
    # print(notVal)
  # tokenIndex+=1
  # print(notVal)
  return notVal
  
def printErrorStmt(expectedToken):
  global tokenIndex    
  # lastIndex = tokenIndex - 1
  # print(tokenList[tokenIndex].value)
  print("Failed - Expected ", expectedToken,  " but found " ,  tokenList[tokenIndex].kind , " with value '" ,  tokenList[tokenIndex].value , "' on line " ,  tokenList[tokenIndex].lineNum)
  print("Parse failed with 1 error")
  # For errors, we skip to the end of the index, so parser doesn't continue
  while  tokenIndex+1 < len(tokenList) and tokenList[tokenIndex].value != "$":
    tokenIndex+=1
  # Once it reaches the end, it will print out error messages
  # if tokenIndex+1 < len(tokenList) and tokenList[tokenIndex].value == "$":

def printValidStmt(expectedToken):
  global tokenIndex
  # tokenIndex-=1
  print("Valid - Expected ", expectedToken,  " and got " ,  tokenList[tokenIndex].kind , " with value '" ,  tokenList[tokenIndex].value , "' on line " ,  tokenList[tokenIndex].lineNum)
  tokenIndex+=1

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
  elif tokenList[tokenIndex].value == " ":
    printValidStmt("T_SPACE")
    parseCharList()

def parseID():
  printValidStmt("T_ID parseID")
  parseChar()

def parseExpr():
  print("parseExpr()")
  if tokenList[tokenIndex].kind == "T_DIGIT":
    parseIntExpr()
  elif tokenList[tokenIndex].kind == "T_QUOTE":
    parseStringExpr() 
  elif tokenList[tokenIndex].kind == "T_RPAREN":
    parseBooleanExpr()
  else:
    parseID()
  # else: 
  #   printErrorStmt("that's not true")

def parseBooleanExpr():
  print("parseBooleanExpr")
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

def parseBlock():
  print("parseBlock()")
  if match("T_LBRACE") is True:
    printValidStmt("T_LBRACE")
    parseStatementList()
    if match("T_RBRACE") is True: 
      printValidStmt("T_RBRACE")
  else:
    if match("T_LBRACE") is False:
      printErrorStmt("T_LBRACE")
    elif match("T_RBRACE") is False:
      printErrorStmt("T_RBRACE")

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
  global tokenIndex
  print("parseVarDecl()")
  # if tokenList[tokenIndex].value == "int" or tokenList[tokenIndex].value == "string" or tokenList[tokenIndex].value == "boolean":
  # if match("T_TYPE"):
  if tokenList[tokenIndex].kind == "T_TYPE":
    # tokenIndex-=1
    printValidStmt("T_TYPE")
    # tokenIndex+=1
    parseID()
  else:
    printErrorStmt("VARDECL")

def parseAssignment():
  print("parseAssignment()")
  # if re.match(regex.character, tokenList[tokenIndex].value):
  if match("T_ID") is True:
    parseID()
    # printValidStmt("T_ID")
    if match("T_ASSIGN") is True: 
      printValidStmt("T_ASSIGN")
      parseExpr()
  else:
    printErrorStmt("parseAssignment is wrong")

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

# def epsilon():


def parseStatementList():
  global tokenIndex
  print("parseStatementList()")
  print(tokenList[tokenIndex].kind)
  if match("T_RBRACE") is True or match("T_EOP") is True:
    print("true statement")
  else: 
    parseStatement()
    parseStatementList()
  # if parseStatement() and parseStatementList():
  #   print("parseStatementList()")
  # else:
  #   global tokenIndex
  #   tokenIndex+=1

def parseStatement():
  global tokenIndex
  print("parseStatement()")
  # while tokenIndex+1 < len(tokenList):
  if match("T_PRINT") is True:
    parsePrint()
  # elif re.match(r"[a-z]", tokenList[tokenIndex].value):
  elif match("T_ID") is True:
    parseAssignment()
  # elif tokenList[tokenIndex].value == r"[int]|[string]|[boolean]|[a-z]": 
  elif match("T_TYPE") is True:
    parseVarDecl()
  elif match("T_WHILE") is True:
    parseWhile()
  elif match("T_IF"):
    parseIf()
  elif match("T_LBRACE") is True:
    parseBlock()

def parseProgram():
  print("parseProgram()")
  parseBlock()
  printValidStmt("T_EOP")

def parse():
  print("parse()")
  parseProgram()

parse()