import operator
import collections


class Polynomial(tuple):
    def __new__(cls, obj=None):
        if not obj:
            return super().__new__(cls)
        elif isinstance(obj, collections.abc.Mapping):
            if not obj:
                return cls()
            return cls(obj.get(i, 0) for i in range(max(obj), -1, -1))

        obj = list(obj)
        while obj[0] == 0:
            obj.pop(0)
            if not obj:
                return cls()
        return super().__new__(cls, obj)

    def todict(self):
        return {e: c for e, c in enumerate(reversed(self)) if c}

    def __add__(self, other):
        together = collections.Counter(self.todict()) + \
                   collections.Counter(other.todict())

        cls = type(self)
        return cls(together)

    def __mul__(self, other):
        total = [0] * (len(self) + len(other) - 1)
        for i, val1 in self.todict().items():
            for j, val2 in other.todict().items():
                total[i + j] += val1 * val2

        cls = type(self)
        return cls(reversed(total))

    def __str__(self):
        """ This is a mess """
        l = {e: ('{:+}'.format(c)[0] + ' ', abs(c)) for
             e, c in self.todict().items()}
        if not l:
            return ''

        largest = l[max(l)]
        largest = largest[0][0] if largest[0][0] is '-' else '', largest[1]
        l[max(l)] = largest

        return ' '.join('{}{}{}{}'.format(
            c[0],
            c[1],
            'x' if e > 0 else '',
            ('^' + str(e)) if e > 1 else '')
                       for e, c in sorted(
                           l.items(),
                           key=operator.itemgetter(0),
                           reverse=True)
                      )

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, super().__repr__())
