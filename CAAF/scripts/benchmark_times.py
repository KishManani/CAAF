'''
Runs model to benchmark times
'''

import time
import matplotlib.pyplot as plt
import CAAF.model as model

heart = model.Heart(row_size=200,
                    col_size=200,
                    prob_con=0.15,
                    prob_def=0.05,
                    refractory_period=50,
                    prob_not_fire=0.05)

start_time = time.time()
heart.update(num_iters=10000, plot=False)
duration = time.time() - start_time
print('Time: {0} s'.format(duration))

fig,ax = plt.subplots(figsize=[10,10])
ax.plot(heart.num_active_cells)
fig.show()
fig.savefig('num_active_cells.png')



