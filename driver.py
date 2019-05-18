# Jae Kyoung Lee

# For dynamic test inputs
x = str(input("Enter the test file: "))

# Opening as read mode to read the test files
open_file = open(x, "r")
# open_file = open("test_alan.8.txt", "r")
# Creating list of individual contents in the file
listFile = list(open_file.read())
# Close file
open_file.close()
# import parser
def letsDrive():
  import lex
  import parzer
  import printstmt
  import semanticAnalysis
  import codegen

  # Create list of tokens from the LEX output
  # It should be 2D list
  tokenList = lex.lex(listFile)

  # parzerList = parzer.parse(tokenList)
  parzer.parse(tokenList)
  semanticAnalysis.semanticAnalysis(tokenList)
  # saCodegen = semanticAnalysis.semanticAnalysis(tokenList)
  # codegen.startCodeGen(saCodegen)
  # print(saCodegen.get('program1').get('AST').toString())


  # Checking for debugging
  # for i in tokenList:
  #   # print(i)
  #   for j in i:
  #     # print(lex.lexstmt)
  #     print(j.kind)

  # Traverses the list of print statements
  for i in printstmt.outerStmt:
    # print(i)
    for j in i:
      # Prints out statements
      print(j)

letsDrive()