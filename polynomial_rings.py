from __future__ import annotations

class Polynomial():

    def __init__(self, coefficients: list, truncate: bool = False):
        self._coefficients = [i for i in coefficients]
        if truncate:
            while self._coefficients[len(self._coefficients)-1] == 0:
                self._coefficients.pop(len(self._coefficients)-1)
        self._degree = len(self._coefficients)-1

    def __str__(self):
        s = ''
        for i, coefficient in enumerate(reversed(self._coefficients)):
            if coefficient != 0:
                if s == '' and i == len(self._coefficients)-1: s += f'{coefficient}'
                elif s == '': s += f'{coefficient}x^{len(self._coefficients)-1-i}'
                elif i < len(self._coefficients)-1: s += f' + {coefficient}x^{len(self._coefficients)-1-i}'
                else: s += f' + {coefficient}'
        return s
    
    def equals(self, p: Polynomial) -> bool:
        p1 = self._coefficients
        p2 = p._coefficients
        if len(p1) < len(p2):
            p1, p2 = p2, p1
        for i in range(len(p1)):
            if i < len(p2):
                if p1[i] != p2[i]: return False
            else:
                if p1[i] != 0: return False
        return True
    
    def increment(self, mod: int, key: list = [0]):
        self._coefficients[key[0]] = (self._coefficients[key[0]]+1) % mod
        if self._coefficients[key[0]] == 0: 
            if key[0] < len(self._coefficients)-1:
                self.increment(mod,[key[0]+1])
            else:
                for i in range(len(self._coefficients)):
                    self._coefficients[i] = 0
    
    def copy(self) -> Polynomial:
        new = Polynomial(self._coefficients.copy())

def _product(p1: Polynomial, p2: Polynomial, mod: int = 0) -> Polynomial:
    p = [0]*(len(p1._coefficients)+len(p2._coefficients))

    p1c = p1._coefficients
    p2c = p2._coefficients

    for m, a in enumerate(p1c):
        for n, b in enumerate(p2c):
            p[m+n] += a*b
    if mod != 0:
        for i in range(len(p)):
            p[i] = p[i] % mod
    
    return Polynomial(p)

def polynomial_multiplication(polynomials: list, mod: int = 0):
    if len(polynomials) < 2: raise ValueError('too few polyomials!')
    #Multiply the first two polynomial
    p = _product(polynomials[0],polynomials[1],mod)

    #Now multiply the rest
    for i in range(2,len(polynomials)):
        p = _product(p, polynomials[i],mod)

    return p

def find_solutions(polynomial: Polynomial, mod: int = 0, degree: int = -1) -> list:
    pairs = []
    if degree == -1:
        deg = polynomial._degree
    else: deg = degree

    p1 = Polynomial([0]*(deg+1))
    p2 = Polynomial([0]*(deg+1))

    p1.increment(mod)
    while p1._coefficients != [0]*(deg+1) or p2._coefficients != [0]*(deg+1):
        # print(f'Testing : ({p1})({p2})')
        if polynomial.equals(polynomial_multiplication([p1,p2],mod)):
            pairs.append([p1.copy(), p2.copy()])
            print(f'({p1})({p2}) = {polynomial_multiplication([p1,p2],mod)}')
        p1.increment(mod)
        if p1._coefficients == [0]*(deg+1):
            p2.increment(mod)
        
    return pairs

def polynomial_divison(dividend: Polynomial, divisor: Polynomial) -> Polynomial:
    dend = dividend._coefficients.copy()
    div = divisor._coefficients.copy()
    dend.reverse()
    div.reverse()

    slot = 0
    quo = [0]*(len(dend)-len(div)+1)
    while slot <= len(dividend._coefficients) - len(divisor._coefficients):
        coef = dend[slot] / div[0]
        quo.append(coef)
        for i in range(len(divisor._coefficients)):
            dend[slot+i] -= div[i]*coef
        slot += 1
    
    return Polynomial(reversed(quo),True), Polynomial(reversed(dend),True)

def find_root(poly: Polynomial, mod: int = 0):
    pass

def main():
    p1 = Polynomial([1]*21)
    p2 = Polynomial([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
    p3 = Polynomial([1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0])
    p4 = Polynomial([1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1])
    p6 = Polynomial([1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0])
    print(polynomial_multiplication([p1,p2,p3,p4,p6]))

if __name__ == '__main__':
    main()