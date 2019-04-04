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



def letsDrive():
  import lex
  import parser
  # Create list of tokens from the LEX output
  # It should be 2D list
  tokenList = lex.lex(listFile)
  parser.startParse()