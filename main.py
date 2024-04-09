from Polynomial import Polynomial

##### Polynomial Rings ver 1.0 #####

####################################
#####       EXAMPLE USAGE      #####
####################################

'''

Polynomials over an infinite domain
p1 = 1 + x
p2 = 5 - x + x^2

p = p1 * p2 = 5 + 4x + x^3

p // p1 = p2 = 5 - x + x^2
'''
p1 = Polynomial([1,1])
print(p1)

p2 = Polynomial([5,-1,1])
print(p2)

p = p1 * p2
print(p)

print(p // p1)

print()
'''

Multiplying Two Polynomials in Z_10
p = 4 + 8x - 5x^2
q = 3 - 4x + 5x^2 + 2x^3

p * q = 2 + 8x + 3x^2 + 8x^3 + 1x^4

'''

p = Polynomial([4,8,-5], modulo=10)
q = Polynomial([3,-4,5,2], modulo=10)

print(p * q)

print()
'''

Factors of a Polynomial in a Modular Ring.

p = 1 + x^2 => should factor to (2+x)(3+x)

'''
p = Polynomial([1,0,1], modulo=5)
p.factor()