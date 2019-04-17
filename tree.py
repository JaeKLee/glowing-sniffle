import printstmt
class Node:
  def __init__(self, inputName):
    self.name = inputName
    self.children = []
    self.parent = None

traversalResult = ""

class Tree: 
  def __init__(self):
    self.root = None
    self.cur = None # Node object

  def addNodeDef(self, name, kind):
    node = Node(name)
    if (self.root is None) or not self.root:
      self.root = node
    else:
      node.parent = self.cur
      self.cur.children.append(node)
    if kind == "branch":
      self.cur = node

  # Note that we're done with this branch of the tree...
  def endChildren(self):
    # ... by moving "up" to our parent node (if possible).
    # if self.cur.parent is not None and self.cur.parent.name is not None:
    if self.cur.parent is not None and self.cur.parent.name is not None:
      self.cur = self.cur.parent
    else:
      print("error in tree")

  def toString(self):
    # global traversalResult
    # traversalResult = ""
    def expand(node, depth):
      global traversalResult # infinite loop
      # traversalResult = ""
      i = 0
      while i < depth:
        traversalResult+="-"
        i+=1
      # print(type(traversalResult) is tuple)
      # if not node.children or len(node.children) == 0:
      if not node.children or len(node.children) == 0:
        traversalResult += "[" + node.name + "]"
        traversalResult += "\n"
      else:
        traversalResult += "<" + node.name + "> \n"
        i = 0
        while i < len(node.children):
          expand(node.children[i], depth + 1)
          # print(node.children[i])
          i+=1
          return traversalResult
    expand(self.root, 0)
    return traversalResult
  # print(traversalResult)
