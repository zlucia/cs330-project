import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RESULTS = './results.csv'


def main():
	csv = pd.read_csv(RESULTS)
	subjects = np.array(csv.columns)
	no_multitask = np.array(csv.iloc[0])
	multitask_uniform = np.array(csv.iloc[1])
	multitask_eps = np.array(csv.iloc[2])
	multitask_eps_mti = np.array(csv.iloc[3])

	idx = np.argsort(no_multitask)[0:1]
	print(np.mean(no_multitask[idx]))
	
	idx = np.argsort(multitask_uniform)[0:1]
	print(np.mean(multitask_uniform[idx]))

	idx = np.argsort(multitask_eps)[0:1]
	# print(np.mean(multitask_eps[idx]))

	idx = np.argsort(multitask_eps_mti)[0:1]
	print(np.mean(multitask_eps_mti[idx]))

	print()

	idx = np.argsort(no_multitask)[0:6]
	print(np.mean(no_multitask[idx]))
	print(np.mean(multitask_uniform[idx]))
	# print(np.mean(multitask_eps[idx]))
	print(np.mean(multitask_eps_mti[idx]))

	print()

	idx = np.argsort(no_multitask)[0:6]
	print(np.mean(no_multitask[idx]))
	
	idx = np.argsort(multitask_uniform)[0:6]
	print(np.mean(multitask_uniform[idx]))

	idx = np.argsort(multitask_eps)[0:6]
	# print(np.mean(multitask_eps[idx]))

	idx = np.argsort(multitask_eps_mti)[0:6]
	print(np.mean(multitask_eps_mti[idx]))

	print()

	idx = np.argsort(no_multitask)[0:11]
	print(np.mean(no_multitask[idx]))
	
	idx = np.argsort(multitask_uniform)[0:11]
	print(np.mean(multitask_uniform[idx]))

	idx = np.argsort(multitask_eps)[0:11]
	# print(np.mean(multitask_eps[idx]))

	idx = np.argsort(multitask_eps_mti)[0:11]
	print(np.mean(multitask_eps_mti[idx]))


if __name__ == '__main__':
	main()