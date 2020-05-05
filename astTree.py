
class Node:
  def __init__(self, inputName):
    self.name = inputName
    self.children = []
    self.parent = None

class Tree: 
  def __init__(self):
    self.root = None
    self.cur = None # Node object

  def addNodeDef(self, name, kind):
    node = Node(name)
    # Check to see if it needs to be the root node.
    if (self.root is None) or not self.root:
      # We are the root node.
      self.root = node
    else:
      # We are the children.
      # Make our parent the CURrent node...
      node.parent = self.cur
      # ... and add ourselves (via the unfrotunately-named
      # "push" function) to the children array of the current node.
      self.cur.children.append(node)
    if kind == "branch":
      self.cur = node

  # Note that we're done with this branch of the tree...
  def endChildren(self):
    # ... by moving "up" to our parent node (if possible).
    # if self.cur.parent is not None and self.cur.parent.name is not None:
    if self.cur.parent is not None and self.cur.parent.name is not None:
      self.cur = self.cur.parent


  def toString(self):
    traversalResult = ""
    def expand(node, depth):
      nonlocal traversalResult
      i = 0
      while i < depth:
        traversalResult+="-"
        i+=1
      if node.children is None or len(node.children) == 0:
        traversalResult += "[" + node.name + "]"
        traversalResult += "\n"
      else:
        traversalResult += "<" + node.name + "> \n"
        for children in node.children:
          expand(children, depth + 1)
    expand(self.root, 0)
    return traversalResult
