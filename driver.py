# This will traverse through each row of the 2D
rowToken = 0
# This will traverse through each value in the row
columnToken = 0
errorCounter = 0
programNumber = 1
# cst = tree.Tree()

# For dynamic test inputs
x = str(input("Enter the test file: "))

# Opening as read mode to read the test files
open_file = open(x, "r")
# Creating list of individual contents in the file
listFile = list(open_file.read())
# Close file
open_file.close()
# import parser
def letsDrive():
  import re
  import lex
  import parzer
  import regex
  import printstmt
  # Create list of tokens from the LEX output
  # It should be 2D list
  tokenList = lex.lex(listFile)
  # for i in tokenList:
  #   for j in i:
  #     # print(j.kind)
  #     if re.search(regex.eop, j.value):
  #       print("Found token", j.kind , ": " , j.value , " in line ", j.lineNum)
  #       parzer.parse(tokenList)
  #     else:
  #       print("Found token", j.kind , ": " , j.value , " in line ", j.lineNum)
  # print("\nPARSER")

  # parzer.parse(tokenList)

  # lex.printLex(tokenList)
  # for i in lex.lexstmt:
  # print(lex.printstmt)
  parzer.parse(tokenList)
  for i in printstmt.outerStmt:
    # print(i)
    for j in i:
      # print(lex.lexstmt)
      print(j)
  # print(tokenList)
  # parzer.parse(tokenList)

  # if tokenList[rowToken][columnToken].kind == regex.eop:
  #   parzer.parse(tokenList)


letsDrive()