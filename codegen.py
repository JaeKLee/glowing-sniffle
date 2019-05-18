import printstmt as ps

symTree = None

symTab = {}
# symTab = []
symTabin = []
pcCounterNum = 0
pcCounterStr = 0
checkVarDecl = False
checkAssign = False
checkPrint = False
checkWhile = False
checkIf = False
checkAdd = False
newVarScope = ""

traversalResult = ""

def startCodeGen(codeGen):
  global symTree
  # print(codeGen.get('program1').get('AST').toString())
  for key, value in codeGen.items():
    # print(value.get('AST').toString())
    # print(value.get('symbolTable').root.dicto)
    symTreeExpand(value.get('symbolTable').root, 0)
  # print(codeGen.get('program1').get('symbolTable').root)
  # symTreeExpand(codeGen.get('program1').get('symbolTable').root, 0)
  # symTreeExpand(codeGen.get('symbolTable').root, 0)
    # print(symTree.toString())
  for key, value in codeGen.items():
    expand(value.get('AST').root, 0)

def symTreeExpand(node, depth):
  global pcCounterNum, pcCounterStr, newVarScope
  if node.children is None or len(node.children) == 0:
    for key,value in node.dicto.items():
      # print(value)
      if value.get('type') is not None:
        # print(value.get('type'))
        if value.get('type') == "int" or value.get('type') == "boolean":
          newVarScope = key + "@" + node.name[len(node.name)-1]
          tempAddrs = "T" + str(pcCounterNum) + "XX"
          # symTab[pcCounterNum] = [tempAddrs, value.get('type'), pcCounterNum]
          test = {'tempAddrs':tempAddrs, 'symTableType':value.get('type'), 'staticPlaceHolder':pcCounterNum}
          # symTab.update({newVarScope: test})
          symTab.setdefault(newVarScope, test)
          pcCounterNum+=1
        if value.get('type') == "string":
          newVarScope = key + "@" + node.name[len(node.name)-1]
          tempAddrs = "S" + str(pcCounterStr) + "XX"
          # symTab[pcCounterStr] = [tempAddrs, value.get('type'), pcCounterStr]
          test = {'tempAddrs':tempAddrs, 'symTableType':value.get('type'), 'staticPlaceHolder':pcCounterNum}
          # symTab.update({newVarScope: test})
          symTab.setdefault(newVarScope, test)
          pcCounterStr+=1
          # print(symTab)
  else:
    for key,value in node.dicto.items():
      # print(value)
      if value.get('type') is not None:
        # print(value.get('type'))
        if value.get('type') == "int" or value.get('type') == "boolean":
          newVarScope = key + "@" + node.name[len(node.name)-1]
          tempAddrs = "T" + str(pcCounterNum) + "XX"
          # symTab[pcCounterNum] = [tempAddrs, value.get('type'), pcCounterNum]
          test = {'tempAddrs':tempAddrs, 'symTableType':value.get('type'), 'staticPlaceHolder':pcCounterNum}
          # symTab.update({newVarScope: test})
          symTab.setdefault(newVarScope, test)
          pcCounterNum+=1
        if value.get('type') == "string":
          newVarScope = key + "@" + node.name[len(node.name)-1]
          tempAddrs = "S" + str(pcCounterStr) + "XX"
          # symTab[pcCounterStr] = [tempAddrs, value.get('type'), pcCounterStr]
          test = {'tempAddrs':tempAddrs, 'symTableType':value.get('type'), 'staticPlaceHolder':pcCounterNum}
          # symTab.update({newVarScope: test})
          symTab.setdefault(newVarScope, test)
          pcCounterStr+=1
    for children in node.children:
      symTreeExpand(children, depth + 1)
      symTab.clear()
  print(symTab)
  # return traversalResult



# def astTraversal(self, codeGen):
def expand(node, depth):
  global newVarScope, symTab, traversalResult, checkVarDecl, checkAdd, checkAssign,checkIf, checkPrint,checkWhile
  traversalResult=""
  if node.children is None or len(node.children) == 0:
    # traversalResult += "[" + node.name + "]"
    # traversalResult += "\n"
    # checking for vardecl, assignment, print, while, if
    # if codeGen.get()
    if checkVarDecl:
      # if symTree[node.name].get('type') == 'int':
      # print(node.name)
      if newVarScope[1] == "@":
        # print(symTab.get(newVarScope).get('symTableType'))
        # print(symTab)
        if symTab.get(newVarScope).get('symTableType') == "int" or symTab.get(newVarScope).get('symTableType') == "boolean":
          traversalResult+="A9 "
          traversalResult+="00 "
          traversalResult+="8D "
          traversalResult+=str(symTab.get(newVarScope).get('tempAddrs')) + " "
          # print(traversalResult)
      # print(node.name)
    if checkAssign:
      if newVarScope[1] == "@":
          traversalResult+="A9 "
          traversalResult+="00 "
          traversalResult+="8D "
          traversalResult+=str(symTab.get(newVarScope).get('tempAddrs')) + " "
    if checkPrint:
      if newVarScope[1] == "@":
        traversalResult+="AC "
        traversalResult+=str(symTab.get(newVarScope).get('tempAddrs')) + " "
        traversalResult+="A2 "
        traversalResult+="00 "
        traversalResult+="FF "
    if checkWhile:
      print("this is while")
    if checkIf:
      print("this is if")
    if checkAdd:
      print("this is ADD")

  else:
    # traversalResult += "<" + node.name + "> \n"
    if node.name == "VarDecl":
      checkVarDecl = True
    if node.name == "Assignment":
      checkAssign = True
    if node.name == "Print":
      checkPrint = True
    if node.name == "While":
      checkWhile = True
    if node.name == "If":
      checkIf = True
    if node.name == "ADD":
      checkAdd = True



    for children in node.children:
      expand(children, depth + 1)
  print(traversalResult)
  return traversalResult
  # print(traversalResult)