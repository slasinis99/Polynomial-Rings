from __future__ import annotations

# def find_units(degree: int, mod: int):
#     p1 = [0]*(degree+1)
#     p2 = [0]*(degree+1)
#     units = []
#     while p1 != [mod-1]*(1+degree) or p2 != [mod-1]*(1+degree):
#         increment_polynomials(p1,p2,mod)
#         p = poly_mult(p1,p2,mod)
#         #print(f'({print_poly(p1)})({print_poly(p2)}) = {print_poly(p)}')
#         if p[0] == 1 and sum(p) == 1:
#             units.append([p1.copy(), p2.copy()])
#     if len(units) == 0: print(f'No Unit Pairs found for degree={degree}, modulus={mod}.')
#     for i, pair in enumerate(units):
#         print('Unit Pair:')
#         print(f'\t{print_poly(pair[0])}, {print_poly(pair[1])}')
#     return units

# def find_solutions(degree: int, mod: int, product: list) -> list:
#     p1 = [0]*(degree+1)
#     p2 = [0]*(degree+1)
#     solutions = []
#     while p1 != [mod-1]*(1+degree) or p2 != [mod-1]*(1+degree):
#         increment_polynomials(p1,p2,mod)
#         #print(p1,p2)
#         if compare_polynomials(product, poly_mult(p1,p2,mod)):
#             solutions.append([p1.copy(),p2.copy()])
#             if any([i != 0 for i in p1]) and any([i != 0 for i in p2]):
#                 print(f'({print_poly(p1)})({print_poly(p2)}) = {print_poly(product)}')
#     if len(solutions) == 0: print(f'No Polynomial Solutions Found for degree {degree} for Z_{mod}.')
#     return solutions

# def compare_polynomials(p1: list, p2: list) -> bool:
#     if len(p2) > len(p1): p1, p2 = p2, p1
#     for i in range(len(p1)):
#         if i < len(p2):
#             if p1[i] != p2[i]: return False
#         else:
#             if p1[i] != 0: return False
#     return True

# #Polynomials should be in ascending order
# def poly_mult(p1: list, p2: list, mod: int):
#     #Create a new polynomial with appropriate size
#     p = [0]*(len(p1)+len(p2))
    
#     #Loop through each polynomial and cross multiply
#     for m, a in enumerate(p1):
#         for n, b in enumerate(p2):
#             p[m+n] += a*b

#     #Perform the modulus operator
#     for i in range(len(p)):
#         p[i] = p[i] % mod
    
#     return p

# def print_poly(p: list):
#     s = f''
#     for i in range(len(p)):
#         if p[i] != 0:
#             if s != '': s += ' + '
#             s += str(p[i])
#             if i > 0: s += f'x^{i}'
#     if s == '': s = '0'
#     return s
            
# def increment_polynomials(p1: list, p2: list, mod: int, key: list = [0,0]) -> None:
#     if key[0] == 0:
#         p1[key[1]] = (p1[key[1]]+1) % mod
#         if p1[key[1]] == 0:
#             if key[1] < len(p1)-1: increment_polynomials(p1,p2,mod,[key[0],key[1]+1])
#             else: increment_polynomials(p1,p2,mod,[1,0])
#     elif key[0] == 1:
#         p2[key[1]] = (p2[key[1]]+1) % mod
#         if p2[key[1]] == 0:
#             if key[1] < len(p2)-1: increment_polynomials(p1,p2,mod,[key[0],key[1]+1])
#             else: return


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
        #print(quo)
        #print(dend)
    
    return Polynomial(reversed(quo),True), Polynomial(reversed(dend),True)

def find_root(poly: Polynomial, mod: int = 0):
    return

# p1 = Polynomial([1,2,0,0,5,6])
# print(p1)
# p2 = Polynomial([4,2])
# print(p2)
# quo, rem = polynomial_divison(p1,p2)
# print(f"quo = {quo}, rem = {rem}")

# def q12(n: int):
#     p = Polynomial([0,0,0])
#     p.increment(n)
#     while(p._coefficients != [0]*3):
#         for i in range(0,n):
#             #print(f'{p} , x = {i} , {sum([((i**u)*j)%n for u,j in enumerate(p._coefficients)])}')
#             if sum([((i**u)*j)%n for u,j in enumerate(p._coefficients)])%n == 0 and p._coefficients[2] == 1:
#                 print(f'{p} , x = {i}')
#                 break
#         p.increment(n)
