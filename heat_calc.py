import numpy.linalg as np
import math
import sympy.solvers as sp

root = np.solve([math.pi*10**2/4, -1], [0,0])
print(root)