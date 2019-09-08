import timeit
import random
from decimal import Decimal
from prettytable import PrettyTable


def expression(x, y, operator, typeval):
    if typeval == 'int':
        a = int(x * 100)
        b = int(y * 100)
    elif typeval == 'float':
        a = x * 100
        b = y * 100
    elif typeval == 'str':
        if operator == '+':
            a = str(round(x * 100, 3))
            b = str(round(y * 100, 3))
        elif operator == '*':
            a = str(round(x * 100, 3))
            b = int(y * 100)
    return timeit.timeit('a' + operator + 'b', globals=locals(), number=10 ** 6) / 10 ** 6


def create_table():
    res = []
    random.seed(1234)
    x = random.random()
    y = random.random()
    int_add = 1 / expression(x, y, '+', 'int')
    for typeval in ['int', 'float', 'str']:
        for operator in '+-*/':
            if typeval == 'str' and operator in '-/':
                continue
            if typeval == 'int' and operator == '+':
                current_expr = int_add
            else:
                current_expr = 1 / expression(x, y, operator, typeval)
            percent = round(100 * current_expr / int_add)
            bar = 'X' * round(40 * current_expr / int_add)
            res.append([operator, typeval, '%6e' % Decimal(current_expr), bar, str(percent) + '%'])
    return res


pt = PrettyTable()
pt.field_names = ['operator', 'operand type', 'times in one second', 'diagram', 'percent']
pt.align['diagram'] = 'l'
for row in create_table():
    pt.add_row(row)
print(pt)
