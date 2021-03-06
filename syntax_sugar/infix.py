from functools import partial, reduce
from itertools import product, islice
from .util import flip
from .composable import compose

class infix(partial):
    def __truediv__(self, right):
        return self(right)

    def __rtruediv__(self, left):
        return infix(self.func, left)

is_a = of = infix(isinstance)
contains = infix(lambda lst, item: item in lst)
pair = infix(lambda a, b: (a, b))
join = infix(lambda lst, s: s.join(lst))
hasattr = infix(hasattr)
fmap = infix(flip(map))
ffilter = infix(flip(filter))
freduce = infix(flip(reduce))
take = infix(compose(list, islice))

INF = float('inf')

class To:
    def __init__(self, start, end):
        if start == INF: 
            raise TypeError('Cannot start range from infinity')

        valid_char = lambda c: c /of/ str and len(c) == 1
        valid_integer = lambda i: i /of/ int or i == INF

        if valid_integer(start) and valid_integer(end):
            self.type = 'number'
        elif valid_char(start) and valid_char(end):
            self.type = 'char'
        else:
            raise TypeError('Unknown range: %s to %s' % (start, end))

        self.start = start
        self.curr = self.start
        self.step = 1 if end > start else -1
        self.end = end

    def __mul__(self, rhs):
        return product(self, rhs)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.step == 0 or not self.step /is_a/ int:
            raise TypeError('Interval must be an integer different from 0')
        def next_number():
            too_big = self.step > 0 and self.curr > self.end
            too_small = self.step < 0 and self.curr < self.end

            if too_big or too_small: raise StopIteration

            ret = self.curr
            self.curr += self.step
            return ret

        def next_char():
            too_big = self.step > 0 and ord(self.curr) > ord(self.end)
            too_small = self.step < 0 and ord(self.curr) < ord(self.end)

            if too_big or too_small: raise StopIteration
            
            ret = self.curr
            self.curr = chr(ord(self.curr) + self.step)
            return ret
            
        if self.type == 'number':
            return next_number()
        elif self.type == 'char':
            return next_char()
        else:
            raise StopIteration
    
    def __str__(self):
        if self.type == 'number':
            return super(To, self).__str__()
        elif self.type == 'char':
            return ''.join(self)
        else:
            raise NotImplementedError

@infix
def to(start, end):
    return To(start, end)

__all__ = [
    'infix',
    'of',
    'is_a',
    'contains',
    'pair',
    'join',
    'to',
    'INF',
    'hasattr',
    'fmap',
    'freduce',
    'ffilter',
    'take',
]
