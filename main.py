from math import *

first_num = int(input('Введіть перше число:'))
second_num = int(input('Введіть друге число:'))
dija = input('Введіть бажану дію:')
k = 0
while k == 0:
    k + 1
    if dija == '+':
        print('Відповідь:', first_num + second_num)
    elif dija == '-':
        print('Відповідь:', first_num - second_num)
    elif dija == '*':
        print('Відповідь:', first_num * second_num)
    elif dija == '/':
        print('Відповідь:', first_num / second_num)
        if second_num < 0:
            print('На 0 ділити не можна!!!')
    else:
        print('Невірна умова, спробуйте ще:')


input()