import time
import itertools

template = """
def inner(it, timer{init}):
    def empty():
        t0=timer()
        for i in it:
            continue
        t1=timer()
        return t1-t0
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
        src = template.format(stmt=expr, init="")
        code = compile(src, 'dummy', 'exec')
        exec(code, global_ns, local_ns)
        self.inner = local_ns['inner']

    def timeit(self, number=10 ** 6):
        it = itertools.repeat(None, number)
        timing = self.inner(it, self.timer)
        return timing/number

    def repeat(self, repeat=10):
        r = []
        for _ in range(repeat):
            r.append(self.timeit())
        return r


a = 1
b = 2
print(Timer('a+b', globals()).timeit())
