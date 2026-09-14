import numpy as np

n_row = 10
n_col = 10
n_samples = n_row * n_col

x1, x2, x3 = np.zeros(n_samples), np.zeros(n_samples), np.zeros(n_samples)
x1_min, x1_max = 0.05, 0.25

for i in range(n_samples):
    row = int(i / n_col)
    col = i - row * n_col
    x1[i] = row * (x1_max - x1_min) / n_row + x1_min
    
    x2_min = 0.05
    x2_max = 0.6 - 2 * x1[i] - 0.05
    x2[i] =  col * (x2_max - x2_min) / n_col + x2_min
    
    x3[i] = 1.5 - 5 * x1[i] - 2.5 * x2[i]

print(f"\nX1 Array")
print(x1)
print(f"\nX2 Array")
print(x2)
print(f"\nX3 Array")
print(x3)