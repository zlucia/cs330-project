import abc
import numexpr
import numpy as np

from typing import Union, Optional, Dict


class BaseMultiTaskSampler(metaclass=abc.ABCMeta):
    def __init__(self, task_dict: dict, rng: Union[int, np.random.RandomState, None]):
        self.task_dict = task_dict
        if isinstance(rng, int) or rng is None:
            rng = np.random.RandomState(rng)
        self.rng = rng

    def pop(self):
        raise NotImplementedError()

    def iter(self):
        yield self.pop()

    def name(self):
        raise NotImplementedError()


class UniformMultiTaskSampler(BaseMultiTaskSampler):
    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState, None],
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        # Fixed order list of task names
        self.task_names = sorted(list(task_dict.keys()))
        self.actions_cnt = np.array([0.0] * len(self.task_names))
        self.selected_tasks = []

    def pop(self):
        i = self.rng.choice(len(self.task_names))
        self.selected_tasks.append(i)
        self.actions_cnt[i] += 1
        task_name = self.task_names[i]
        return i, task_name, self.task_dict[task_name]
    
    def get_selected_tasks(self):
        return self.selected_tasks

    def get_actions_cnt(self):
        return self.actions_cnt
    
    def name(self):
        return "UniformMultiTaskSampler"


class ProportionalMultiTaskSampler(BaseMultiTaskSampler):
    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState],
        task_to_num_examples_dict: dict,
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        assert task_dict.keys() == task_to_num_examples_dict.keys()
        self.task_to_examples_dict = task_to_num_examples_dict
        self.task_names = list(task_to_num_examples_dict.keys())
        self.task_num_examples = np.array([task_to_num_examples_dict[k] for k in self.task_names])
        self.task_p = self.task_num_examples / self.task_num_examples.sum()

    def pop(self):
        task_name = self.rng.choice(self.task_names, p=self.task_p)
        return task_name, self.task_dict[task_name]

    def name(self):
        return "ProportionalMultiTaskSampler"


class SpecifiedProbMultiTaskSampler(BaseMultiTaskSampler):
    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState],
        task_to_unweighted_probs: dict,
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        assert task_dict.keys() == task_to_unweighted_probs.keys()
        self.task_to_unweighted_probs = task_to_unweighted_probs
        self.task_names = list(task_to_unweighted_probs.keys())
        self.unweighted_probs_arr = np.array([task_to_unweighted_probs[k] for k in self.task_names])
        self.task_p = self.unweighted_probs_arr / self.unweighted_probs_arr.sum()

    def pop(self):
        task_name = self.rng.choice(self.task_names, p=self.task_p)
        return task_name, self.task_dict[task_name]

    def name(self):
        return "SpecifiedProbMultiTaskSampler"

class EpsilonGreedyMultiTaskSampler(BaseMultiTaskSampler):
    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState, None],
        epsilon: float = 0.3,
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        # Fixed order list of task names
        self.task_names = sorted(list(task_dict.keys()))
        self.epsilon = epsilon
        self.rewards = np.array([0.0] * len(self.task_names))
        self.actions_cnt = np.array([0.0] * len(self.task_names))
        self.selected_tasks = []
    
    def pop(self):
        if self.rng.random() <= self.epsilon:
            i = self.rng.choice(len(self.task_names))
        else:
            i = np.argmax(self.rewards)
        self.selected_tasks.append(i)
        task_name = self.task_names[i]
        return i, task_name, self.task_dict[task_name]
    
    def record_reward(self, reward: float, reward_idx: int):
        n = self.actions_cnt[reward_idx]
        # Moving average
        self.rewards[reward_idx] = (n * self.rewards[reward_idx] + reward) / (n + 1)
        self.actions_cnt[reward_idx] += 1
    
    def get_selected_tasks(self):
        return self.selected_tasks

    def get_rewards(self):
        return self.rewards
    
    def get_actions_cnt(self):
        return self.actions_cnt

    def name(self):
        return "EpsilonGreedyMultiTaskSampler"


class UCBMultiTaskSampler(BaseMultiTaskSampler):
    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState, None],
        c: float,
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        self.task_names = sorted(list(task_dict.keys()))
        # Weight on the UCB term
        self.c = c
        self.rewards = np.array([0.0] * len(self.task_names))
        self.actions_cnt = np.array([0.0] * len(self.task_names))
        self.t = 1
        self.selected_tasks = []
    
    def pop(self):
        # If all of the arms have been pulled at least once
        if np.count_nonzero(self.actions_cnt) == len(self.task_names):
            augmented = self.rewards + self.c * np.sqrt(np.log(self.t) / self.actions_cnt)
            i = np.argmax(augmented)
        else:
            i = np.argmax(np.array(self.rewards) == 0)
        self.selected_tasks.append(i)
        self.t += 1
        task_name = self.task_names[i]
        return i, task_name, self.task_dict[task_name]
    
    def record_reward(self, reward: float, reward_idx: int):
        # Number of times the task at task_names[reward_idx] has been chosen
        n = self.actions_cnt[reward_idx]
        # Moving average
        self.rewards[reward_idx] = (n * self.rewards[reward_idx] + reward) / (n + 1)
        self.actions_cnt[reward_idx] += 1
    
    def get_selected_tasks(self):
        return self.selected_tasks

    def get_rewards(self):
        return self.rewards
    
    def get_actions_cnt(self):
        return self.actions_cnt

    def name(self):
        return "UCBMultiTaskSampler"


class ThompsonSamplingMultiTaskSampler(BaseMultiTaskSampler):
    """Thompson Sampling with a Gaussian prior"""
    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState, None]
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        self.task_names = sorted(list(task_dict.keys()))

        # Gaussian prior, initialize with N(0, 1)
        self.mu = np.array([0.0] * len(self.task_names))
        self.var = np.array([1.0] * len(self.task_names))

        self.actions_cnt = np.array([0] * len(self.task_names))
        self.selected_tasks = []
    
    def pop(self):
        samples = np.array([self.rng.normal(loc=self.mu[i], scale=np.sqrt(self.var[i])) for i in range(len(self.task_names))])
        i = np.argmax(samples)
        self.selected_tasks.append(i)
        task_name = self.task_names[i]
        return i, task_name, self.task_dict[task_name]
    
    def record_reward(self, reward:float, reward_idx: int):
        # Gaussian prior
        # Number of times the task at task_names[reward_idx] has been chosen
        n = self.actions_cnt[reward_idx]
        self.mu[reward_idx] = (n * self.mu[reward_idx] + reward) / (n + 1)
        self.var[reward_idx] = 1 / (n + 1)
        self.actions_cnt[reward_idx] += 1
    
    def get_selected_tasks(self):
        return self.selected_tasks

    def get_rewards(self):
        return self.mu
    
    def get_actions_cnt(self):
        return self.actions_cnt

    def name(self):
        return "ThompsonSamplingMultiTaskSampler"


class TemperatureMultiTaskSampler(BaseMultiTaskSampler):
    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState],
        task_to_num_examples_dict: dict,
        temperature: float,
        examples_cap: Optional[int],
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        assert task_dict.keys() == task_to_num_examples_dict.keys()
        self.task_to_num_examples_dict = task_to_num_examples_dict
        self.temperature = temperature
        self.examples_cap = examples_cap
        self.task_names = list(task_to_num_examples_dict.keys())
        self.task_num_examples = np.array([task_to_num_examples_dict[k] for k in self.task_names])
        raw_n = self.task_num_examples.clip(max=examples_cap) ** (1 / self.temperature)
        self.task_p = raw_n / raw_n.sum()

    def pop(self):
        task_name = self.rng.choice(self.task_names, p=self.task_p)
        return task_name, self.task_dict[task_name]

    def name(self):
        return "TemperatureMultiTaskSampler"


class TimeDependentProbMultiTaskSampler(BaseMultiTaskSampler):
    """Multi-task Sampler with different task sampling probabilities over time

    We describe the individual unnormalized probabilities using numexpr expressions,
    using t as the variable, e.g.:
    * 1             (constant)
    * 2 * t         (linear)
    * 1/sqrt(t)     (inverse square-root)

    These are computed for all tasks for each time step, and then normalized to sum to 1.

    Attributes:
        task_dict: Dictionary of tasks
        rng: Random seed, or NumPy RandomState for sampling
        task_to_unnormalized_prob_funcs_dict: map from task names to strings, which are
                                              numexpr expressions
        max_steps: Maximum number of steps allows (in the case where some functions
                   are not valid after a given t.
    """

    def __init__(
        self,
        task_dict: dict,
        rng: Union[int, np.random.RandomState],
        task_to_unnormalized_prob_funcs_dict: dict,
        max_steps: Optional[int] = None,
    ):
        super().__init__(task_dict=task_dict, rng=rng)
        assert task_dict.keys() == task_to_unnormalized_prob_funcs_dict.keys()
        self.task_to_unnormalized_prob_funcs_dict = task_to_unnormalized_prob_funcs_dict
        self.max_steps = max_steps

        self.task_names = list(task_to_unnormalized_prob_funcs_dict.keys())
        self.steps = 0

    def pop(self):
        if self.max_steps is not None and self.steps >= self.max_steps:
            raise IndexError(f"steps ({self.steps}) > max_steps ({self.max_steps})")
        task_name = self.rng.choice(self.task_names, p=self.get_task_p(self.steps))
        self.steps += 1
        return task_name, self.task_dict[task_name]

    def get_task_p(self, steps=None) -> np.ndarray:
        p_ls = np.empty(len(self.task_names))

        # t is the variable in the numexpr expression
        t = steps if steps is not None else self.steps

        for i, task_name in enumerate(self.task_names):
            p_ls[i] = numexpr.evaluate(
                self.task_to_unnormalized_prob_funcs_dict[task_name], local_dict={"t": t},
            )
        p_ls /= p_ls.sum()
        return p_ls

    def reset_counter(self):
        self.steps = 0

    def name(self):
        return "TimeDependentProbMultiTaskSampler"


def create_task_sampler(
    sampler_config: dict, task_dict: dict, task_to_num_examples_dict: dict, rng=None
) -> BaseMultiTaskSampler:
    """Perform basic config validation, then instantiate and return the specified multitask sampler.

    Args:
        sampler_config (Dict): map containing sample config options.
        task_dict (Dict[str, Task]): map from task name to task instance.
        task_to_num_examples_dict (Dict[str, int]): map task names to counts of training examples.
        rng (Union[int, np.random.RandomState, None]): random state to seed sampler.

    Raises:
        KeyError if invalid sampler type argument is provided in the sampler config.

    Returns:
        Subclass of BaseMultiTaskSampler.

    """
    sampler_type = sampler_config["sampler_type"]
    if sampler_type == "UniformMultiTaskSampler":
        assert len(sampler_config) == 1
        return UniformMultiTaskSampler(task_dict=task_dict, rng=rng)
    elif sampler_type == "ProportionalMultiTaskSampler":
        assert len(sampler_config) == 1
        return ProportionalMultiTaskSampler(
            task_dict=task_dict, rng=rng, task_to_num_examples_dict=task_to_num_examples_dict,
        )
    elif sampler_type == "SpecifiedProbMultiTaskSampler":
        assert len(sampler_config) == 2
        return SpecifiedProbMultiTaskSampler(
            task_dict=task_dict,
            rng=rng,
            task_to_unweighted_probs=sampler_config["task_to_unweighted_probs"],
        )
    elif sampler_type == "EpsilonGreedyMultiTaskSampler":
        assert len(sampler_config) == 2
        return EpsilonGreedyMultiTaskSampler(
            task_dict=task_dict,
            rng=rng,
            epsilon=sampler_config["epsilon"],
        )
    elif sampler_type == "UCBMultiTaskSampler":
        assert len(sampler_config) == 2
        return UCBMultiTaskSampler(
            task_dict=task_dict,
            rng=rng,
            c=sampler_config["c"],
        )
    elif sampler_type == "ThompsonSamplingMultiTaskSampler":
        assert len(sampler_config) == 1
        return ThompsonSamplingMultiTaskSampler(
            task_dict=task_dict,
            rng=rng,
        )
    elif sampler_type == "TemperatureMultiTaskSampler":
        assert len(sampler_config) == 3
        return TemperatureMultiTaskSampler(
            task_dict=task_dict,
            rng=rng,
            task_to_num_examples_dict=task_to_num_examples_dict,
            temperature=sampler_config["temperature"],
            examples_cap=sampler_config["examples_cap"],
        )
    elif sampler_type == "TimeDependentProbMultiTaskSampler":
        assert len(sampler_config) == 3
        return TimeDependentProbMultiTaskSampler(
            task_dict=task_dict,
            rng=rng,
            task_to_unnormalized_prob_funcs_dict=sampler_config[
                "task_to_unnormalized_prob_funcs_dict"
            ],
            max_steps=sampler_config["max_steps"],
        )
    else:
        raise KeyError(sampler_type)


class BaseMetricAggregator(metaclass=abc.ABCMeta):
    def aggregate(self, major_metrics_dict: Dict[str, float]):
        raise NotImplementedError()


class EqualMetricAggregator(BaseMetricAggregator):
    def aggregate(self, major_metrics_dict: Dict[str, float]):
        return np.mean([x for x in major_metrics_dict.values()])


class WeightedMetricAggregator(BaseMetricAggregator):
    def __init__(self, weights_dict: Dict[str, float]):
        self.weights_dict = weights_dict
        self.total_weights = sum([x for x in weights_dict.values()])

    def aggregate(self, major_metrics_dict: Dict[str, float]):
        return (
            np.sum(
                [x * self.weights_dict[task_name] for task_name, x in major_metrics_dict.items()]
            )
            / self.total_weights
        )


def create_metric_aggregator(metric_aggregator_config: Dict) -> BaseMetricAggregator:
    """Perform basic config validation, then instantiate and return the specified metric aggregator.

    Args:
        metric_aggregator_config (Dict): map containing metric aggregation options.

    Returns:
        Subclass of BaseMetricAggregator.

    """
    metric_aggregator_type = metric_aggregator_config["metric_aggregator_type"]
    if metric_aggregator_type == "EqualMetricAggregator":
        assert len(metric_aggregator_config) == 1
        return EqualMetricAggregator()
    elif metric_aggregator_type == "WeightedMetricAggregator":
        assert len(metric_aggregator_config) == 2
        return WeightedMetricAggregator(weights_dict=metric_aggregator_config["weights_dict"])
    else:
        raise KeyError(metric_aggregator_type)


def compute_aggregate_major_metrics_from_results_dict(metrics_aggregator, results_dict):
    major_metrics_dict = {
        task_name: results["metrics"].major for task_name, results in results_dict.items()
    }
    return metrics_aggregator.aggregate(major_metrics_dict=major_metrics_dict)


def get_metrics_dict_from_results_dict(results_dict):
    return {task_name: results["metrics"].to_dict() for task_name, results in results_dict.items()}
