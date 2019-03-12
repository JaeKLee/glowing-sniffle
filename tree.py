#-----------------------------------------
# tree.py
#
# By Alan G. Labouseur, based on the 2009
# work by Michael Ardizzone and Tim Smith.
# Edited by Jae Kyoung Lee (LJ)
#-----------------------------------------

def tree(self):
  self.root = None
  self.cur = []

  def addNode(self, name, kind):
    
    if (self.root is None) or not self.root:
      self.root = node
    else:
      node.parent = self.cur
      self.cur.children.push(node)
    if kind == "branch":
      self.cur = node

def endChildren(self):
  if self.cur.parent is not None and self.cur.parent.name is not None:
    self.cur = self.cur.parent
  else:
    print("error in tree")

def toString(self):
  traversalResult = ""
  def expand(node, depth):
    i = 0
    for i in depth:
      traversalResult+="-"
      i+=1
    if not node.children or node.children.length == 0:
      traversalResult += "[" , node.name , "]"
      traversalResult += "\n"
    else:
      traversalResult += "<" , node.name , "> \n"
      i = 0
      while i < len(node.children):
        expand(node.children[i], depth + 1)
  expand(self.root, 0)
  return traversalResult


