import parzer
import printstmt

# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
errorCounter = 0
# print("test")

def match(tokenList, expectedToken):
  global rowToken, columnToken
  notVal = False
  if rowToken < len(tokenList):
    if expectedToken == tokenList[rowToken][columnToken].kind:
      notVal = True  
  return notVal

def semanticAnalysis(tokenList):
    global rowToken,columnToken
    # print("this is to test if semantic analysis is being called properly. I can't see the word test without writing this long sentence.")
    printstmt.outerStmt[rowToken].append("\nSemantic Analysis")
    # printstmt.outerStmt[rowToken].append("\nProgram " , programNumber , " starting....")
    if match(tokenList, "ERROR") is True:
        printstmt.outerStmt[rowToken].append("Semantic Analysis: Skipped due to Parser error(s)")
        if rowToken < len(tokenList):
            rowToken+=1 # Moving onto next program
            # programNumber+=1
            columnToken=0
