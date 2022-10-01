
class Executer():

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
            index += 1