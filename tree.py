def tree():
  self.root = None
  self.cur = []

  def addNode(name, kind):
    node = [
      name: name,
      children: [],
      parent: []
    ]