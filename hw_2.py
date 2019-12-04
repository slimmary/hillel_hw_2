def foo_input_float(msg):
    i = 5
    while i != 0:
        try:
            return float(input(f'введите {msg}'))
        except ValueError:
            i -= 1
            print(f'{msg} это не число, введите, число. у вас осталось {i} попыток')


operations = {'+': lambda a, b: a+b,
              '-': lambda a, b: a-b,
              '*': lambda a, b: a*b,
              '/': lambda a, b: a/b if b != 0 else print('извините, деление на ноль не возможно')
              }

# # 1. input a input b input op -> result
a = foo_input_float('первое число')
b = foo_input_float('второе число')

i = 5
while i != 0:
    oper = input('введите желаемую операцию - + / или *')  # проверяем что бы ввели мат.операцию, с кол-вом попыток продолжаем
    if oper not in ('+', '-', '/', '*'):
        i -= 1
        print(f'извините, вы ввели не математическую операцию, повторите ввод. у вас осталось {i} попыток')
    else:
        i = 0
        res = operations[oper](a,b)
        print(f'{a} {oper} {b} = {res}')

# # 2. #1 +  скобки

a = foo_input_float('первое число')
b = foo_input_float('второе число')
i = 5
while i != 0:
    oper = input('введите желаемую операцию - + / или *')  # проверяем что бы ввели мат.операцию, с кол-вом попыток продолжаем
    if oper not in ('+', '-', '/', '*'):
        i -= 1
        print(f'извините, вы ввели не математическую операцию, повторите ввод. у вас осталось {i} попыток') # проверяем что бы ввели мат.операцию, с кол-вом попыток продолжаем
    oper2 = input('введите желаемую операцию - + / или * которая полседует за скобками')  # тут так же проверяем что бы это была мат. операция
    if oper2 not in ('+', '-', '/', '*'):
        i -= 1
        print(f'извините, вы ввели не математическую операцию, начните заново у вас осталось {i} попыток')
    else:
        i = 0
        e = foo_input_float('третье число')
        res = operations[oper](a,b)
        res_all = operations[oper2](res,e)
        print(f'({a} {oper} {b}) {oper2} {e} = {res_all}')


