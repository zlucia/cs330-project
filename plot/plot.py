import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RESULTS = '../results/results.csv'


def plotter(subjects, data):
	plt.rcParams.update({'font.size': 8})
	fig, ax = plt.subplots(figsize=(7, 10))
	y_pos = np.arange(len(subjects)) * 2
	no_multitask = ax.barh(y_pos + 0.25, data[0], height=0.5, align='center', color="#7aa0c4")
	multitask_uniform = ax.barh(y_pos - 0.25, data[1], height=0.5, align='center', color="#8bcd50")
	ax.set_xlim(0, 1.0)
	ax.set_ylim(-1, 114)
	ax.set_yticks(y_pos)
	ax.set_yticklabels(subjects, fontsize=6)
	# ax.invert_yaxis()
	plt.vlines(0.25, ymin=-1, ymax=114, colors="#ca82e1", linewidth=1)
	plt.legend([no_multitask, multitask_uniform], ['Indepedent', 'Multitask (uniform)'], title="Training Schedule", fontsize=8)
	plt.tight_layout()
	plt.savefig('./figures/baselines.png')
	# plt.show()


def main():
	csv = pd.read_csv(RESULTS)
	subjects = np.array(csv.columns)
	no_multitask = np.array(csv.iloc[0])
	multitask = np.array(csv.iloc[1])

	idx = np.argsort(no_multitask)
	plotter(subjects[idx], [no_multitask[idx], multitask[idx]])

if __name__ == '__main__':
	main()