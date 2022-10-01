TD = ["null", "+", "-", "*", "/", "(", ")", "{", "}", "[", "]", ";", "=",
       ":", ":=", "<", ">", "<>", "<=", ">=", ".", ",", "’", "^"]

TW = ["and", "begin", "bool", "do", "else", "end", "if", "false", "int", "not", "or", "program",
      "read", "then", "true", "var", "while", "write", "const", "repeat", "for", "to", "do", "integer", "of", "array"]


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
                    return "".join(buf), dict, ''