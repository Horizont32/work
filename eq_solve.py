import numpy as numpy
import math
import sympy
import scipy.interpolate as int
from scipy.optimize import fsolve
import matplotlib.pyplot as plt





D17 = [3.4, 3.56, 3.66, 3.75]
D4 = [1.57, 1.7, 1.93, 2.08]
D8 = [1.61, 1.71, 1.89, 2.01]
R17 = [234.66, 248.1, 260.9, 295]
R4 = [230.6, 260.9, 289.8, 301]
R8 = [236.7, 267.32, 289.8, 303]

inted17 = int.interp1d(R17, D17, kind='cubic', fill_value='extrapolate')
inted4 = int.interp1d(R4, D4, kind='cubic', fill_value='extrapolate')
inted8 = int.interp1d(R8, D8, kind='cubic', fill_value='extrapolate')


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