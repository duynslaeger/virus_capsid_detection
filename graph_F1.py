import pandas as pd
from matplotlib import pyplot as plt

def f1(precision, recall):
	# res = 2 * (precision*recall)/(precision + recall)
	# num = [a * b for a, b in zip(precision, recall)]
	# denom = precision + recall
	# fract = [a / b for a, b in zip(num, denom)]
	# res = [2*x for x in fract]
	res = [2*(a*b)/(a+b) for a,b in zip(precision, recall)]
	return res


results_scratch = pd.read_csv("../results_small_from_scratch.csv")
results_pretrained = pd.read_csv("../results_small_pretraind.csv")
# print(results)

# print(type(results))

epochs = (results_scratch.iloc[:,0]).to_list()

precision_scratch = (results_scratch.iloc[:,5]).to_list()
recall_scratch = (results_scratch.iloc[:,6]).to_list()
f1_scratch = f1(precision_scratch, recall_scratch)

precision_pretrained = (results_pretrained.iloc[:,5]).to_list()
recall_pretrained = (results_pretrained.iloc[:,6]).to_list()
f1_pretrained = f1(precision_pretrained, recall_pretrained)

plt.plot(epochs, f1_pretrained, label='Pre-trained model')
plt.plot(epochs, f1_scratch, label='From scratch model')
plt.legend()
plt.xlabel("epochs")
plt.ylabel("F1 score")
plt.show()

print(f1_pretrained[-1])
print(f1_scratch[-1])

# print(epochs)