import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RESULTS = './results.csv'


def main():
	csv = pd.read_csv(RESULTS)
	subjects = np.array(csv.columns)
	no_multitask = np.array(csv.iloc[0])
	multitask = np.array(csv.iloc[1])

	idx = np.argsort(no_multitask)
	print(np.mean(no_multitask[idx[0:11]]))
	print(np.mean(multitask[idx[0:11]]))


if __name__ == '__main__':
	main()