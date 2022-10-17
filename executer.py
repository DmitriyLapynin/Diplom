
class Executer():

    def __init__(self, pars):
        self.pars = pars

    def execute(self):
        index = 0
        key = False
        args = []
        ind_arr = 0
        array = []
        while index < len(self.pars.poliz):
            pc_el = self.pars.poliz[index]
            if pc_el[0] == "bool" or pc_el[0] == "int" or pc_el[0] == "poliz_address" or pc_el[0] == "poliz_label":
                args.append(pc_el[1])
                if pc_el[1] in self.pars.dict and self.pars.dict[pc_el[1]][2] == "array":
                    key = True
                '''if len(pc_el) > 2:
                                    if type(pc_el[2]) is str:
                                        if self.pars.dict[pc_el[2]][1]:
                                            pc_el = (pc_el[0], pc_el[1], self.pars.dict[pc_el[2]][3])
                                            if pc_el[2] in range(self.pars.dict[pc_el[1]][4], self.pars.dict[pc_el[1]][5] + 1):
                                                pass
                                            else:
                                                raise Exception("Error: not in range of array")
                                        else:
                                            raise Exception("POLIZ: undefined elem")
                                    ind_arr = pc_el[2]
                                args.append(pc_el[1])'''
            elif pc_el[0] == "ID":
                '''if (self.pars.dict[pc_el[1]])[2] == "array":
                    if type(pc_el[2]) is str:
                        if self.pars.dict[pc_el[2]][1]:
                            pc_el = (pc_el[0], pc_el[1], self.pars.dict[pc_el[2]][3])
                            if pc_el[2] in range(self.pars.dict[pc_el[1]][4], self.pars.dict[pc_el[1]][5] + 1):
                                pass
                            else:
                                raise Exception("Error: not in range of array")
                        else:
                            raise Exception("POLIZ: undefined elem")
                    ind_arr = pc_el[2]
                    if ((self.pars.dict[pc_el[1]])[6])[ind_arr - 1] != "no":
                        args.append((self.pars.dict[pc_el[1]])[6][ind_arr - 1])
                    else:
                        raise Exception("POLIZ: indefinite identifier")'''
                if pc_el[1] in self.pars.dict and self.pars.dict[pc_el[1]][2] == "array":
                    key = True
                    args.append(pc_el[1])
                elif (len(self.pars.dict[pc_el[1]]) > 3):
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
                if key:
                    key = False
                    ind_arr = args[-1]
                    args.pop()
                    j = args[-1]
                    args.pop()
                    array = self.pars.dict[j][6]
                    if ind_arr < (self.pars.dict[j])[4] or ind_arr > (self.pars.dict[j])[5]:
                        raise Exception("Error: not in range of array")
                    else:
                        if array[ind_arr - 1] == "no":
                            raise Exception("POLIZ: indefinite identifier")
                        else:
                            print(array[ind_arr - 1])
                else:
                    j = args[-1]
                    args.pop()
                    print(j)
            elif pc_el[0] == "read":
                value = 0
                i = args[-1]
                args.pop()
                if key:
                    ind_arr = i
                    key = False
                    i = args[-1]
                    args.pop()
                if (self.pars.dict[i])[2] == "array":
                    if (self.pars.dict[i])[3] == "integer":
                        while True:
                            print("Input int value for " + i + '[' + str(ind_arr) + ']')
                            value = input()
                            if value.isdigit():
                                break
                            else:
                                print("Error in input: expect int number")
                                continue
                    else:
                        while True:
                            print("Input boolean value (true or false) for" + i + '[' + str(ind_arr) + ']')
                            j = input()
                            if j != "true" and j != "false":
                                print("Error in input:true/false")
                                continue
                            if j == "false":
                                value = 0
                            else:
                                value = 1
                            break
                    array = self.pars.dict[i][6]
                    if ind_arr < (self.pars.dict[i])[4] or ind_arr > (self.pars.dict[i])[5]:
                        raise Exception("Error: not in range of array")
                    else:
                        array[ind_arr - 1] = int(value)
                        self.pars.dict[i] = ("ID", True, (self.pars.dict[i])[2], (self.pars.dict[i])[3], (self.pars.dict[i])[4], (self.pars.dict[i])[5], array)
                else:
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
                if key:
                    print("asd")
                    key = False
                    ind_arr = j
                    j = args[-1]
                    args.pop()
                    args.append(self.pars.dict[j][6][ind_arr - 1] > i)
                else:
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
                '''if self.pars.dict[j][2] == "array":
                    array = self.pars.dict[j][6]
                    if type(pc_el[2]) is str:
                        if self.pars.dict[pc_el[2]][1]:
                            pc_el = (pc_el[0], pc_el[1], self.pars.dict[pc_el[2]][3])
                            if pc_el[2] in range(self.pars.dict[j][4], self.pars.dict[j][5] + 1):
                                pass
                            else:
                                raise Exception("Error: not in range of array")
                        else:
                            raise Exception("POLIZ: undefined elem")
                    array[pc_el[2] - 1] = i
                    self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], (self.pars.dict[j])[3], (self.pars.dict[j])[4], (self.pars.dict[j])[5], array)
                else:
                    self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], i)'''
                if key:
                    ind_arr = j
                    j = args[-1]
                    args.pop()
                    key = False
                    if self.pars.dict[j][2] == "array":
                        array = self.pars.dict[j][6]
                        '''if type(pc_el[2]) is str:
                            if self.pars.dict[pc_el[2]][1]:
                                pc_el = (pc_el[0], pc_el[1], self.pars.dict[pc_el[2]][3])
                                if pc_el[2] in range(self.pars.dict[j][4], self.pars.dict[j][5] + 1):
                                    pass
                                else:
                                    raise Exception("Error: not in range of array")
                            else:
                                raise Exception("POLIZ: undefined elem")'''
                        if ind_arr < (self.pars.dict[j])[4] or ind_arr > (self.pars.dict[j])[5]:
                            raise Exception("Error: not in range of array")
                        else:
                            array[ind_arr - 1] = i
                            self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], (self.pars.dict[j])[3], (self.pars.dict[j])[4], (self.pars.dict[j])[5], array)
                else:
                    self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], i)

            else:
                raise Exception("POLIZ: unexpected elem")
            index += 1