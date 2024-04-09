from __future__ import annotations

class FieldMismatch(Exception):
    pass

class DivisionException(Exception):
    pass

class Polynomial():
    def __init__(self, coefficients: list, truncate: bool = False, modulo: int = 0) -> None:
        self._cf = [i for i in coefficients]
        if truncate:
            while self._cf[-1] == 0:
                self._cf.pop(-1)
        self._d = len(self._cf) -1
        self.mod = modulo
        self.__simp__()
    
    def __str__(self) -> str:
        if all([c == 0 for c in self._cf]):
            return '0'
        cf_width = 0
        exp_width = 0
        s = ''
        count = 0
        for i in range(len(self._cf)):
            if len(str(self._cf[i])) > cf_width:
                cf_width = len(str(self._cf[i]))
            if len(str(i)) > exp_width:
                exp_width = len(str(i))
            if self._cf[i] != 0:
                count += 1
        for i, c in enumerate(self._cf):
            if c != 0:
                if i == 0:
                    s += f'{c}'
                else:
                    s += f'{c: >{cf_width}}x^{i: <{exp_width}}'
                if count > 1:
                    s += f' + '
                    count -= 1
        return s
    
    def __iter__(self):
        for c in self._cf:
            yield c

    def __len__(self):
        return len(self._cf)

    def __simp__(self):
        if self.mod == 0:
            return
        for i in range(len(self._cf)):
            self._cf[i] = self._cf[i] % self.mod
        return
    
    def __add__(self, p: Polynomial) -> Polynomial:
        p1 = self
        p2 = p
        if p1.mod != p2.mod:
            raise FieldMismatch()
        if len(p2) > len(p1):
            p1, p2 = p2, p1
        new_c = [0]*len(p1)
        for i in range(len(p1)):
            if i < len(p2):
                new_c[i] = p1._cf[i] + p2._cf[i]
            else:
                new_c[i] = p1._cf[i]
        r =  Polynomial(new_c, modulo=p1.mod, truncate=True)
        r.__simp__()
        return r
    
    def __mul__(self, p: Polynomial):
        if self.mod != p.mod:
            raise FieldMismatch()
        new_c = [0]*(len(self._cf) + len(p._cf))
        for m, a in enumerate(self._cf):
            for n, b in enumerate(p._cf):
                new_c[n+m] += a*b
        r = Polynomial(new_c, modulo=self.mod, truncate=True)
        r.__simp__()
        return r
    
    def __floordiv__(self, p: Polynomial) -> Polynomial:
        return (self / p)[0]
    
    def __truediv__(self, p: Polynomial) -> Polynomial | Remainder:
        dividend = list(reversed(self._cf))
        divisor = list(reversed(p._cf))
        slot = 0
        quo = []
        while slot <= len(dividend) - len(divisor):
            coef = dividend[slot] / divisor[0]
            quo.append(coef)
            for i in range(len(divisor)):
                dividend[slot+i] -= divisor[i]*coef
            slot += 1
        return [Polynomial(reversed(quo), modulo=self.mod), Remainder(Polynomial(reversed(dividend), modulo=self.mod), p)]

    def __getitem__(self, s):
        if isinstance(s, int):
            c = [0]*len(self._cf)
            c[s] = 1
            return Polynomial(c, True, modulo=self.mod)
        elif isinstance(s, slice):
            if s.start is None: start = 0
            else: start = s.start
            if s.stop is None: stop = -1
            else: stop = s.stop
            if s.step is None: step = 1
            else: step = s.step
            c = [0]*len(self._cf)
            for i in range(start, stop, step):
                c[i] = self._cf[i]
            return Polynomial(c, True, modulo=self.mod)
    
    def __increment__(self, i: int = 0) -> None:
        self._cf[i] = (self._cf[i]+1) % self.mod
        if self._cf[i] == 0:
            if i < len(self._cf) - 1:
                self.__increment__(i+1)
            else:
                self._cf = [0]*len(self._cf)
    
    def __call__(self, x: float) -> float:
        s = sum([c * x**i for i, c in enumerate(self._cf)])
        if self.mod == 0:
            return s
        return s % self.mod
    
    def copy(self) -> Polynomial:
        return Polynomial(self._cf.copy(), modulo=self.mod)

    def factor(self) -> list[Polynomial]:
        if self.mod == 0:
            pass
        factor_list = []
        lb = 0
        ub = self.mod - 1
        wp = self.copy()
        fp = None
        while True:
            for x in range(lb, ub, 1):
                if wp(x) < 1e-15:
                    fp = Polynomial([-x, 1], modulo=self.mod)
                    break
            if fp is None:
                break
            factor_list.append(fp)
            wp = wp // fp
            for i in range(len(wp._cf)):
                wp._cf[i] = int(wp._cf[i])
            if len(wp) == 2:
                factor_list.append(wp)
                break
            fp = None
        s = f'{self} = '
        for f in factor_list:
            s += f'({f})'
        print(s)
        return factor_list


class Remainder():
    def __init__(self, numerator: Polynomial, denominator: Polynomial) -> None:
        self.n = numerator
        self.d = denominator

    def __str__(self) -> str:
        return f'{self.n} / {self.d}'
