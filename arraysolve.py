import numpy as np

m1 = np.array([[2., 5.], [1., -10.]])
n1 = np.array([1., 0.])
np.linalg.solve(m1, n1)
print(np.linalg.solve(m1, n1))