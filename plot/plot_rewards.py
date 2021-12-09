import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RESULTS = '../results/results_bert.csv'
REWARDS_DATA = './data/multitask_thompson/rewards.npy'

def main():
	csv = pd.read_csv(RESULTS)
	subjects = np.array(sorted(list(csv.columns)))

	rewards = np.load(REWARDS_DATA) * 100
	idx = np.argsort(rewards)
	print(subjects[idx])
	print(rewards[idx])
	# print(rewards)

	# plt.rcParams.update({'font.size': 8})
	# plt.bar(x=np.arange(len(subjects)), height=rewards)
	# plt.xticks(np.arange(len(subjects)), subjects, rotation='vertical')
	# plt.xlabel("Task")
	# plt.ylabel("Reward")
	# plt.title("Task reward for Thompson sampling schedule")
	# plt.tight_layout()
	# # plt.show()
	# plt.savefig('./figures/multitask_thompson_rewards.png')

if __name__ == '__main__':
	main()