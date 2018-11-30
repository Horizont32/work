import numpy as np
import math
import sympy
from scipy.interpolate import interp1d
from scipy.optimize import fsolve

def f(xy):
   x, y = xy
   x = [float(x) for x in range(0, 50)]
   y = [float(y ** 0.5) for y in range(0, 50)]
   g = [float((g + 12) ** 0.3 + 15) for g in range(0, 50)]
   f1 = interp1d(x, y, kind='cubic')
   f2 = interp1d(x, g, kind='cubic')
   z = np.array([f1, f2])
   return z

print(fsolve(f, [1.0, 2.0]))

