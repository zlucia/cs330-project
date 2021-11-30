import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RESULTS = '../results/results.csv'


def plotter(subjects, data):
	plt.rcParams.update({'font.size': 8})
	fig, ax = plt.subplots(figsize=(5, 5))
	y_pos = np.arange(len(subjects))
	no_multitask = ax.barh(y_pos, data[0], height=0.25, align='center', color="#7aa0c4")
	# no_multitask = ax.barh(y_pos + 0.25, data[0], height=0.25, align='center', color="#7aa0c4")
	# multitask_uniform = ax.barh(y_pos, data[1], height=0.25, align='center', color="#8bcd50")
	# multitask_eps = ax.barh(y_pos - 0.25, data[2], height=0.25, align='center', color="#745ea6")
	ax.set_xlim(0, 0.5)
	ax.set_ylim(-1, 57)
	# ax.set_ylim(-1, 6)
	ax.set_yticks(y_pos)
	ax.set_yticklabels(subjects, fontsize=6)
	ax.set_xlabel("Accuracy")
	ax.set_ylabel("Subject")
	plt.vlines(0.25, ymin=-1, ymax=57, colors="#ca82e1", linewidth=1)
	# plt.vlines(0.25, ymin=-1, ymax=6, colors="#ca82e1", linewidth=1)
	plt.legend([no_multitask], ['Independent training'], title="Training Schedule", fontsize=6)
	# plt.legend([no_multitask, multitask_uniform, multitask_eps], ['Independent training', 'Multitask (uniform)', 'Multitask (epsilon-greedy)'], title="Training Schedule", fontsize=6)
	plt.tight_layout()
	# plt.savefig('./figures/baseline.png')
	# plt.show()


def main():
	csv = pd.read_csv(RESULTS)
	subjects = np.array(csv.columns)
	no_multitask = np.array(csv.iloc[0])
	multitask_uniform = np.array(csv.iloc[1])
	multitask_eps = np.array(csv.iloc[2])

	idx = np.argsort(no_multitask)
	plotter(subjects[idx], [no_multitask[idx]])

	# idx = np.argsort(no_multitask)[0:6]
	# plotter(subjects[idx], [no_multitask[idx], multitask_uniform[idx], multitask_eps[idx]])


if __name__ == '__main__':
	main()