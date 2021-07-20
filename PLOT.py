import numpy  as np
import matplotlib.pyplot as plt
data = np.loadtxt('test_data.txt')


x = data
plt.plot(x,'r--')
plt.show()