class CsvReader:
  def __init__(self, filepath: str):
    self.filepath = filepath

  def read(self):
    with open(self.filepath, ...) as f:
      yield ...
    