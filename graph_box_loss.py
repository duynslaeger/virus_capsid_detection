import pandas as pd
from matplotlib import pyplot as plt



results = pd.read_csv("results/results_small_pretraind.csv")
# print(results)

# print(type(results))

epochs = (results.iloc[:,0]).to_list()

train_loss = (results.iloc[:,1]).to_list()
val_loss = (results.iloc[:,9]).to_list()

plt.plot(epochs, train_loss, label='Training')
plt.plot(epochs, val_loss, label='Validation')
plt.legend()
plt.xlabel("epochs")
plt.ylabel("Box loss")
plt.show()

# print(epochs)