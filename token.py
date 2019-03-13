class Token:
  def __init__(self, tokenKind, tokenValue, lineNumber):
    self.kind = tokenKind
    self.value = tokenValue
    self.lineNum = lineNumber
