from interpretator import Interpretator


try:
    print("Подмножества языка Паскаль:")
    print("1 – Язык линейных вычислений")
    print("2 – Язык условных вычислений")
    print("3 – Язык циклических вычислений")
    '''while 1:
        print("Выберите номер языка, на котором написана программа")
        mode = int(input())
        if mode > 3 or mode < 1:
            print("Номер языка должен быть в отрезке [1, 3]")
        else:
            break
    print("Введите название файла с программой")
    f = input()'''
    i = Interpretator('test.txt', 2)
    i.interpretation()
    print("Работа анализатора заверешена успешно!")
except Exception as error:
    print(error)
except FileNotFoundError:
    print("The file is not exist")