import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.figure(figsize=(16, 9))
x_binom = np.arange(0, 11)
y = stats.binom.pmf(x_binom, 10, 0.6)
plt.plot(x_binom, y, 'o-', label=f'B({10}, {0.6})')
plt.title('Binomial Distribution')
plt.legend()
plt.grid(True)
plt.show()