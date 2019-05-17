
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
    # print(self.cur.parent.name)
    # print(self.cur.parent)
    if self.cur.parent is not None and self.cur.parent.name is not None:
      self.cur = self.cur.parent
    # else:
    #   print("error in tree")

  # print(traversalResult + "printing traversal")
  def toString(self):
    global traversalResult
    traversalResult = ""
    def expand(node, depth):
      global traversalResult
      # traversalResult = "in expand"
      i = 0
      while i < depth:
        traversalResult+="-"
        i+=1
      # print(type(traversalResult) is tuple)
      # if not node.children or len(node.children) == 0:
      if node.children is None or len(node.children) == 0:
        traversalResult += "[" + node.name + "]"
        traversalResult += "\n"
      else:
        traversalResult += "<" + node.name + "> \n"
      # j = 0
        for children in node.children:
          # expand(node.children[j], depth + 1)
          expand(children, depth + 1)
          # node.children=[]
          # print(children.name)
        # j+=1
        # return traversalResult
      # node.name = ""
      node.children = []
      # node.parent = None  
      # node.children = None
    expand(self.root, 0)
    return traversalResult
    # traversalResult=""
    # return expand(self.root, 0)
  # print(traversalResult + "printing traversal")

# traversalResult = ""