import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

RESULTS = './results_bert.csv'

def main():
	csv = pd.read_csv(RESULTS)
	subjects = np.array(csv.columns)
	no_multitask = np.array(csv.iloc[0])
	multitask_uniform = np.array(csv.iloc[1])
	multitask_eps = np.array(csv.iloc[2])
	multitask_ucb = np.array(csv.iloc[3])
	multitask_thomp = np.array(csv.iloc[4])

	idx = np.argsort(no_multitask)[0:6]
	print(subjects[idx])
	print(no_multitask[idx])

	print(np.mean(no_multitask[idx]))
	print(np.mean(multitask_uniform[idx]))
	print(np.mean(multitask_eps[idx]))
	print(np.mean(multitask_ucb[idx]))
	print(np.mean(multitask_thomp[idx]))


if __name__ == '__main__':
	main()