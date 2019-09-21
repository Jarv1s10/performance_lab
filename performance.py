import random
from decimal import Decimal
from prettytable import PrettyTable
import time
import itertools
import math

template = """
def inner(it, timer):
    def empty():
        t00=timer()
        for i in it:
            continue
        t01=timer()
        return t01-t00
    t0 = timer()
    for i in it:
        {stmt}
    t1 = timer()
    return t1 - t0 - empty()
    """


class Timer:
    def __init__(self, expr, globals):
        self.timer = time.perf_counter
        local_ns = {}
        global_ns = globals
        src = template.format(stmt=expr)
        code = compile(src, 'dummy', 'exec')
        exec(code, global_ns, local_ns)
        self.inner = local_ns['inner']

    def numtime(self, number=10 ** 6):
        it = itertools.repeat(None, number)
        timing = self.inner(it, self.timer)
        return timing

    def mintime(self, repeat=5, number=10 ** 6):
        return min([self.numtime(number) for _ in range(repeat)]) / number


def timeit(expr, glbls, number):
    return Timer(expr, glbls).mintime(number=number)


def expression(x, y, operator, typeval):
    iterations = 0
    if typeval == 'int':
        a = int(x * 100)
        b = int(y * 100)
        iterations = 10 ** 6
    elif typeval == 'float':
        a = x * 100
        b = y * 100
        iterations = 10 ** 6
    elif typeval == 'str':
        iterations = 10 ** 3
        if operator == '+':
            a = str(round(x * 1000))
            b = str(round(y * 1000))
        elif operator == '*':
            a = str(round(x * 1000))
            b = int(y * 100)
    return timeit('a' + operator + 'b', locals(), iterations)


def create_table():
    res = []
    x = random.random()
    y = random.random()
    int_add = 1 / expression(x, y, '+', 'int')
    types = {'int': '+-*/', 'float': '+-*/', 'str': '+*'}
    for typeval in types.keys():
        for operator in types[typeval]:
            if typeval == 'int' and operator == '+':
                current_expr = int_add
            else:
                current_expr = 1 / expression(x, y, operator, typeval)
            percent = round(100 * current_expr / int_add)
            bar = 'X' * math.floor(0.4 * percent)
            res.append([operator, typeval, '%6e' % Decimal(current_expr), bar, str(percent) + '%'])
    return res


pt = PrettyTable()
pt.field_names = ['operator', 'operand type', 'times in one second', 'diagram', 'percent']
pt.align['diagram'] = 'l'
for row in create_table():
    pt.add_row(row)
print(pt)


