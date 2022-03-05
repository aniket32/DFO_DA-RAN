import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
fig, ax = plt.subplots()
ax.scatter([1,2, 1.5], [2, 1, 1.5])
cir = plt.Circle((1.5, 1.5), 0.07, color='r',fill=False)
ax.set_aspect('equal', adjustable='datalim')
ax.add_patch(cir)
plt.show()