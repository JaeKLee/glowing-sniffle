import token
import re

currentIndex = 0

def parseProgram():
  parseBlock()

def parseBlock():
  currentIndex = 0
  while currentIndex < len(token.tokenList):
    if re.match(r"{", token.tokenList[currentIndex]):
      parseStatementList()
      currentIndex+=1
      re.match(r"}", token.tokenList[currentIndex])

def parseStatementList():
  parseStatement()
  parseStatementList()

def parseStatement():
  parsePrint()
  # parseAssignment()

def parsePrint():
  currentIndex = 0
  while currentIndex < len(token.tokenList):
    if re.match(r"print", token.tokenList[currentIndex]):
      currentIndex+=1
      
def match(expectedToken):
  notVal = False
  if expectedToken is token.tokenList[currentIndex]:
    notVal = True
  return notVal
