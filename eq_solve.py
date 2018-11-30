import numpy as numpy
import math
import sympy
import scipy.interpolate as int
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

x = [5, 10, 85, 89]
y = [-7, 5, 6, 19]
g = [13, 3, -5, 4]

inted = int.interp1d(x, y, kind='cubic', fill_value='extrapolate')
inted2 = int.interp1d(x, g, kind='cubic', fill_value='extrapolate')


def findIntersection(fun1, fun2, x0):
    return fsolve(lambda kek: fun1(kek) - fun2(kek), x0)


result = findIntersection(inted,numpy.cos,0.0)
result2 = findIntersection(inted,inted2,0.0)
print(result, result2)
print(inted2(result2), inted(result2))
x = numpy.linspace(0, 100, 100000)
plt.plot(x, inted2(x), x, inted(x))
plt.plot(result2, inted2(result2), 'ro')
plt.plot(x, numpy.cos(x), result, numpy.cos(result), 'ro')
plt.show()