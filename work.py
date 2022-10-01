'''TD = ["null", "+", "-", "*", "/", "(", ")", "{", "}", "[", "]", ";", "=",
       ":", ":=", "<", ">", "<>", "<=", ">=", ".", ",", "’", "^"]

TW = ["and", "begin", "bool", "do", "else", "end", "if", "false", "int", "not", "or", "program",
      "read", "then", "true", "var", "while", "write", "const", "repeat", "for", "to", "do"]


class Scanner():
    table_key_words = TW
    table_separators = TD

    def __init__(self):
        pass

    def get_lex(self, file, dict, one_sym):
        buf = []
        cs = 'H'
        d = 0
        if one_sym == '' or one_sym == ' ' or one_sym == '\n' or one_sym == '\r' or one_sym == '\t':
            pass
        elif one_sym in self.table_separators:
            if one_sym == ':':
                c = file.read(1)
                if c == '=':
                    return ":=", dict, ''
                else:
                    return one_sym, dict, c
            return one_sym, dict, ''
        else:
            buf.append(one_sym)
        while True:
            c = file.read(1)
            if cs == 'H':
                if c == ' ' or c == '\n' or c == '\r' or c == '\t':
                    pass
                elif c.isalpha():
                    buf.append(c)
                    cs = 'IDENT'
                elif c.isdigit():
                    d = int(c)
                    cs = 'NUMB'
                elif (c == '{'):
                    cs = 'COM'
                elif c == ':' or c == '<' or c == '>':
                    buf.append(c)
                    cs = 'ALE'
                elif c == '!':
                    buf.append(c)
                    cs = 'NEQ'
                else:
                    buf.append(c)
                    if "".join(buf) in self.table_separators:
                        return "".join(buf), dict, ''
                    else:
                        return "Error6", dict, one_sym
            elif cs == 'IDENT':
                if c.isalpha() or c.isdigit():
                    buf.append(c)
                else:
                    # c = file.read(1)
                    one_sym = c
                    if "".join(buf) in self.table_key_words:
                        pass
                    elif "".join(buf) in dict:
                        pass
                    else:
                        dict["".join(buf)] = ("ID", False)
                    return "".join(buf), dict, one_sym
            elif cs == 'NUMB':
                if c.isdigit():
                    d = d * 10 + int(c)
                else:
                    # c = file.read(1)
                    one_sym = c
                    return d, dict, one_sym
            elif cs == 'COM':
                if (c == '}'):
                    cs = 'H'
            elif c == '@' or c == '{':
                return "Error2", dict, ''
            elif cs == 'ALE':
                if c == '=':
                    buf.append(c)
                    return "".join(buf), dict, one_sym
                else:
                    # c = file.read(1)
                    one_sym = c
                    return "".join(buf), dict, ''
            else:
                if c == '=':
                    buf.append(c)
                    return "".join(buf), dict, '' '''

from scanner import Scanner
from parser_pascal import Parser

class Parser():
    mode = 1
    dict = {}
    buf = ""
    st_lex = []
    one_sym = ''
    poliz = []


    def __init__(self, mode):
        self.mode = mode

    def gl(self, f, dict):
        s = Scanner()
        self.buf, self.dict, self.one_sym = s.get_lex(f, dict, self.one_sym)

    def program(self, f):
        self.gl(f, self.dict)
        if self.buf == "program":
            pass
        else:
            raise Exception("Error: expect 'program'")
        self.gl(f, self.dict)
        if self.buf in self.dict:
            if self.dict[self.buf][0] == "ID":
                pass
            else:
                raise Exception("Error: expect name program")
        else:
            raise Exception("Error: expect name program")
        self.gl(f, self.dict)
        if self.buf == '(':
            pass
        else:
            raise Exception("Error: expect left bracket")
        self.gl(f, self.dict)
        while True:
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    pass
                else:
                    raise Exception("Error: expect arg program")
            else:
                raise Exception("Error: expect arg program")
            self.gl(f, self.dict)
            if self.buf == ',':
                self.gl(f, self.dict)
            elif self.buf == ')':
                self.gl(f, self.dict)
                if self.buf == ';':
                    return
                else:
                    raise Exception("Error: expect semicolon")
            else:
                raise Exception("Error: expect right bracket or comma")

    def block(self, f):
        if self.buf == "var":
            self.var(f)
        else:
            pass
        self.begin(f)
        if self.buf != ".":
            raise Exception("expect .")



    def var(self, f):
        tmp_var = []
        self.gl(f, self.dict)
        if self.buf == 'begin':
            return
        else:
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    tmp_var.append(self.buf)
                else:
                    raise Exception("Error: error name of variable")
            else:
                raise Exception("Error: expect name of variable")
            self.gl(f, self.dict)
            while self.buf == ',':
                self.gl(f, self.dict)
                if self.buf in self.dict:
                    if self.dict[self.buf][0] == "ID":
                        tmp_var.append(self.buf)
                    else:
                        raise Exception("Error: expect name of variable")
                else:
                    raise Exception("Error: error name of variable")
                self.gl(f, self.dict)
            if self.buf != ':':
                raise Exception("Error: expect \":\" ")
            else:
                self.gl(f, self.dict)
                if (self.buf == "integer" or self.buf == "bool"):
                    for i in tmp_var:
                        self.dict[i] = ("ID", False, self.buf)
                else:
                    raise Exception("Error: expect type of variables ")
                self.gl(f, self.dict)
                if self.buf == ';':
                    return self.var(f)
                else:
                    raise Exception("Error: expect \";\" ")

    def begin(self, f):
        self.gl(f, self.dict)
        self.operators(f)
        self.one_sym = ''
        while self.buf == ';':
            self.gl(f, self.dict)
            if self.buf == 'end':
                if self.one_sym == ".":
                    raise Exception("error")
                else:
                    break
            self.operators(f)
            if self.buf == 'end':
                break
            else:
                self.one_sym = ''
        if self.buf == 'end':
            self.gl(f, self.dict)
        else:
            raise Exception("unexpected:", self.buf)

    def operators(self, f):
        tmp = []
        if self.buf == "if":
            if self.mode == 1 or self.mode == 3:
                raise Exception("unexpected:", self.buf)
            self.condPascal(f)
        elif self.buf == "while":
            self.whilePascal(f)
        elif self.buf == "repeat":
            self.repeatPascal(f)
        elif self.buf == "for":
            self.forPascal(f)
        elif self.buf == "read":
            self.readPascal(f)
        elif self.buf == "write":
            self.writePascal(f)
        elif (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            self.checkID()
            self.poliz.append(("poliz_address", self.buf))
            return self.assignPascal(f)
        else:
            self.begin(f)

    def forPascal(self, f):
        self.gl(f, self.dict)
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            self.dict[self.buf] = ("ID", False, "integer")
            tmp = self.buf
            self.checkID()
            self.poliz.append(("poliz_address", self.buf))
            self.assignPascal(f)
            pl0 = len(self.poliz)
            self.poliz.append(("ID", tmp))
        else:
            raise Exception("expect ident")
        if self.buf == "to":
            self.gl(f, self.dict)
            self.poliz.append(("int", self.buf))
            self.poliz.append(("<", 0))
            pl1 = len(self.poliz)
            self.poliz.append(("null", 0))
            self.poliz.append(("poliz_fgo", 0))
            self.gl(f, self.dict)
            if self.buf == "do":
                self.gl(f, self.dict)
                self.operators(f)
                self.poliz.append(("poliz_address", tmp))
                self.poliz.append(("ID", tmp))
                self.poliz.append(("int", 1))
                self.poliz.append(("+", 0))
                self.poliz.append(("assign", 0))
                self.poliz.append(("poliz_label", pl0))
                self.poliz.append(("poliz_go", 0))
                self.poliz[pl1] = ("poliz_label", len(self.poliz))
            else:
                raise Exception("expect do")
        else:
            raise Exception("expect to")



    def repeatPascal(self, f):
        pl0 = len(self.poliz)
        self.gl(f, self.dict)
        self.operators(f)
        if self.buf == ";":
            self.gl(f, self.dict)
        if self.buf == "until":
            self.gl(f, self.dict)
            self.E(f)
            self.checkNot()
            self.eqBool()
            pl1 = len(self.poliz)
            self.poliz.append(("null", 0))
            self.poliz.append(("poliz_fgo", 0))
            self.poliz.append(("poliz_label", pl0))
            self.poliz.append(("poliz_go", 0))
            self.poliz[pl1] = (("poliz_label", len(self.poliz)))
        else:
            raise Exception("expect until")


    def whilePascal(self, f):
        pl0 = len(self.poliz)
        self.gl(f, self.dict)
        self.E(f)
        self.eqBool()
        pl1 = len(self.poliz)
        self.poliz.append(("null", 0))
        self.poliz.append(("poliz_fgo", 0))
        if self.buf == "do":
            self.gl(f, self.dict)
            self.operators(f)
            self.poliz.append(("poliz_label", pl0))
            self.poliz.append(("poliz_go", 0))
            self.poliz[pl1] = ("poliz_label", len(self.poliz))
        else:
            raise Exception("expect do")

    def condPascal(self, f):
        self.gl(f, self.dict)
        self.E(f)
        self.eqBool()
        pl2 = len(self.poliz)
        self.poliz.append(("null", 0))
        self.poliz.append(("poliz_fgo", 0))
        if self.buf == "then":
            self.gl(f, self.dict)
            self.operators(f)
            pl3 = len(self.poliz)
            self.poliz.append(("null", 0))
            self.poliz.append(("poliz_go", 0))
            self.poliz[pl2] = (("poliz_label", len(self.poliz)))
            if self.buf == "else":
                self.gl(f, self.dict)
                self.operators(f)
                self.poliz[pl3] = (("poliz_label", len(self.poliz)))
            else:
                raise Exception("expected else")
        else:
            raise Exception("expected then")



    def assignPascal(self, f):
        self.gl(f, self.dict)
        if self.buf == ":=":
            self.gl(f, self.dict)
            self.E(f)
            self.eqType()
            self.poliz.append(("assign", 0))
        return

    def E(self, f):
        self.E1(f)
        if (self.buf == "=") or (self.buf == "<=") or (self.buf == ">=") or (self.buf == "<") or (self.buf == ">") or (self.buf == "!="):
            self.st_lex.append(self.buf)
            self.gl(f, self.dict)
            self.E1(f)
            self.checkOp()

    def E1(self, f):
        self.T(f)
        if (self.buf == "+") or (self.buf == "-") or (self.buf == "or"):
            self.st_lex.append(self.buf)
            self.gl(f, self.dict)
            self.T(f)
            self.checkOp()

    def T(self, f):
        self.F(f)
        if (self.buf == "*") or (self.buf == "/") or (self.buf == "and"):
            self.st_lex.append(self.buf)
            self.gl(f, self.dict)
            self.F(f)
            self.checkOp()

    def F(self, f):
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            self.checkID()
            self.poliz.append(("ID", self.buf))
            self.gl(f, self.dict)
        elif (self.buf in self.dict) and (self.dict[self.buf][0] == "Const"):
            self.poliz.append(("const", self.buf))
            self.gl(f, self.dict)
        elif str(self.buf).isdigit():
            self.st_lex.append("int")
            self.poliz.append(("int", self.buf))
            self.gl(f, self.dict)
        elif self.buf == "true":
            self.st_lex.append("bool")
            self.poliz.append(("bool", 1))
            self.gl(f, self.dict)
        elif self.buf == "false":
            self.st_lex.append("bool")
            self.poliz.append(("bool", 0))
            self.gl(f, self.dict)
        elif self.buf == "not":
            self.gl(f, self.dict)
            self.F(f)
            self.checkNot()
        elif self.buf == "(":
            self.gl(f, self.dict)
            self.E(f)
            if self.buf == ")":
                self.gl(f, self.dict)
            else:
                raise Exception("expect \")\"")
        else:
            raise Exception("error")

    def checkNot(self):
        if self.st_lex == [] or self.st_lex[-1] != "bool":
            raise Exception("error, wrong type")
        else:
            self.poliz.append(("not", 0))

    def checkID(self):
        if (self.buf in self.dict):
            if (self.dict[self.buf][0] == "ID") and (len(self.dict[self.buf]) > 2):
                if self.dict[self.buf][2] == "integer":
                    self.st_lex.append("int")
                else:
                    self.st_lex.append("bool")
            elif (self.dict[self.buf][0] == "Const"):
                self.st_lex.append("const")
            else:
                raise Exception(self.buf + " not declared")
        else:
            raise Exception(self.buf + " not declared")

    def checkIDRead(self):
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID") and (len(self.dict[self.buf]) > 2):
            pass
        else:
            raise Exception(self.buf + " not declared")

    def checkOp(self):
        t = "int"
        r = "bool"
        fst_arg = self.st_lex[-1]
        self.st_lex.pop()
        op = self.st_lex[-1]
        self.st_lex.pop()
        snd_arg = self.st_lex[-1]
        self.st_lex.pop()
        if op == "+" or op == "-" or op == "*" or op == "/":
            r = "int"
        if op == "and" or op == "or":
            t = "bool"
        if (fst_arg == snd_arg) and (fst_arg == t):
            self.st_lex.append(r)
        else:
            raise Exception("wrong types are in operation")
        self.poliz.append((op, 0))
        return

    def eqType(self):
        fst_arg = self.st_lex[-1]
        self.st_lex.pop()
        if fst_arg != self.st_lex[-1]:
            raise Exception("wrong types are in operation :=")
        self.st_lex.pop()

    def eqBool(self):
        if self.st_lex[-1] != "bool":
            raise Exception("expression is not boolean")
        self.st_lex.pop()



    def readPascal(self, f):
        self.gl(f, self.dict)
        if self.buf == '(':
            self.gl(f, self.dict)
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    self.checkIDRead()
                    self.poliz.append(("poliz_address", self.buf))
                else:
                    raise Exception("Error: error name of variable")
            else:
                raise Exception("Error: error name of variable")
        self.gl(f, self.dict)
        if self.buf == ')':
            self.gl(f, self.dict)
            self.poliz.append(("read", 0))
            return
        else:
            raise Exception("expected: )")

    def writePascal(self, f):
        self.gl(f, self.dict)
        if self.buf == '(':
            self.gl(f, self.dict)
            self.E(f)
            if self.buf == ')':
                self.gl(f, self.dict)
                self.poliz.append(("write", 0))
                return
            else:
                raise Exception("expected: )")
        else:
            raise Exception("expected: (")

    def analyze(self, f):
        p = Parser(mode)
        p.program(f)
        p.gl(f, self.dict)
        p.block(f)
        #print(p.dict)
        #print(p.poliz)

'''class Executer():

    def __init__(self, pars):
        self.pars = pars

    def execute(self):
        index = 0
        args = []

        while index < len(self.pars.poliz):
            pc_el = self.pars.poliz[index]
            if pc_el[0] == "bool" or pc_el[0] == "int" or pc_el[0] == "poliz_address" or pc_el[0] == "poliz_label":
                args.append(pc_el[1])
            elif pc_el[0] == "ID":
                if (len(self.pars.dict[pc_el[1]]) > 3):
                    args.append((self.pars.dict[pc_el[1]])[3])
                else:
                    raise Exception("POLIZ: indefinite identifier")
            elif pc_el[0] == "not":
                i = args[-1]
                args.pop()
                args.append(not (i))
            elif pc_el[0] == "or":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i or j)
            elif pc_el[0] == "and":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i and j)
            elif pc_el[0] == "poliz_go":
                i = args[-1]
                args.pop()
                index = i - 1
            elif pc_el[0] == "poliz_fgo":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if (not j):
                    index = i - 1
            elif pc_el[0] == "write":
                j = args[-1]
                args.pop()
                print(j)
            elif pc_el[0] == "read":
                value = 0
                i = args[-1]
                args.pop()
                if (self.pars.dict[i])[2] == "integer":
                    while True:
                        print("Input int value for ", i)
                        value = input()
                        if value.isdigit():
                            break
                        else:
                            print("Error in input: expect int number")
                            continue
                else:
                    while True:
                        print("Input boolean value (true or false) for", i)
                        j = input()
                        if j != "true" and j != "false":
                            print("Error in input:true/false")
                            continue
                        if j == "false":
                            value = 0
                        else:
                            value = 1
                        break
                self.pars.dict[i] = ("ID", True, (self.pars.dict[i])[2], int(value))
            elif pc_el[0] == "+":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i + j)
            elif pc_el[0] == "*":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i * j)
            elif pc_el[0] == "-":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j - i)
            elif pc_el[0] == "/":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if i == 0:
                    raise Exception("POLIZ:divide by zero")
                else:
                    args.append(j / i)
            elif pc_el[0] == "=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j == i)
            elif pc_el[0] == "<":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j < i)
            elif pc_el[0] == ">":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j > i)
            elif pc_el[0] == "<=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j <= i)
            elif pc_el[0] == ">=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j >= i)
            elif pc_el[0] == "-":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j != i)
            elif pc_el[0] == "assign":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], i)
            else:
                raise Exception("POLIZ: unexpected elem")
            index += 1'''

'''class Interpretator():

    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def interpretation(self):
        with open(self.file) as f:
            p = Parser(self.mode)
            e = Executer(p)
            p.analyze(f)
            e.execute()
            return'''










'''try:
    print("Подмножества языка Паскаль:")
    print("1 – Язык линейных вычислений")
    print("2 – Язык условных вычислений")
    print("3 – Язык циклических вычислений")
    print("Выберите номер языка, на котором написана программа")
    mode = input()
    print("Введите название файла с программой")
    f = input()
    i = Interpretator(f, mode)
    i.interpretation()
    print("Работа анализатора заверешена успешно!")
except Exception as error:
    print(error)'''


