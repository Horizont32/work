import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from sympy import solvers, symbols


x = [0, 1, 4, 5, 50]
y = [0, 4, 7, 9, 1010]
g = [0, 4, 7, 123, 124]


x1 = np.linspace(x[0], x[-1], 10000)
ke = interp1d(x,y)
ye = interp1d(x,g)
print(ke(5))
# print(ke(101000))
ue = solvers.solve(ke(x)-ye(x), x)
solvers.solve(ke(x)-ue(x), x)
print(ue)
plt.plot(x, y)
plt.plot(x, g)
plt.show()