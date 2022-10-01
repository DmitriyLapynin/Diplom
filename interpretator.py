from parser_pascal import Parser
from executer import Executer


class Interpretator():

    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def interpretation(self):
        with open(self.file) as f:
            p = Parser(self.mode)
            e = Executer(p)
            p.analyze(f)
            e.execute()
            return