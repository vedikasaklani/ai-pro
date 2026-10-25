"""Synthetic agents and measurable tasks."""
from dataclasses import dataclass
import math
import random
from allocation import Bid

STRATEGIES = ("naive", "mechanism_aware", "mixed")
# Bid shading under pay-as-bid; VCG and proportional fairness get truthful bids.
FIRST_PRICE_SHADE = 0.8
# After a cut-off call, an aware agent retries with a request this much larger.
RETRY_GROWTH = 1.5


@dataclass(frozen=True)
class Task:
    estimate: int  # what the agent knows before running (like a historical average)
    tokens: int    # what the task really consumes; hidden until it runs
    value: float

    @property
    def rate(self) -> float:
        return self.value / self.estimate


class Agent:
    def __init__(self, agent_id: str, tasks: list[Task], strategy: str, margin: float = 1.0):
        self.agent_id = agent_id
        self.tasks = list(tasks)
        self.strategy = strategy
        self.margin = margin
        self.boost = 1.0
        self.completed_value = 0.0
        self.completed_tasks = 0
        self.wasted_tokens = 0
        self.declined = 0
        self.cut_off = 0

    @property
    def remaining_tokens(self) -> int:
        """Estimated demand: the only token figure an agent or operator can see."""
        return sum(t.estimate for t in self.tasks)

    def bid(self, mechanism: str) -> Bid:
        if not self.tasks:
            return Bid(0, 0)
        if self.strategy == "naive":
            # Ignores the rule: asks for its whole backlog and inflates its value signal.
            return Bid(self.remaining_tokens, 2 * max(t.rate for t in self.tasks))
        # Aware: asks for one task plus a safety margin, and bids that task's value per the rule.
        head = self.tasks[0]
        shade = FIRST_PRICE_SHADE if mechanism == "priority_auction" else 1.0
        return Bid(math.ceil(head.estimate * self.margin * self.boost), head.rate * shade)

    def consume(self, granted: int, requested: int) -> int:
        """Run tasks on a grant; return the tokens handed back to the shared pool.

        A call that runs out of tokens is cut off: everything it used is wasted and the task stays queued.
        """
        if self.strategy == "mechanism_aware":
            if not self.tasks or granted < requested:
                self.declined += bool(granted)
                return granted  # never start a call it was not funded to finish
            task = self.tasks[0]
            if task.tokens > granted:
                self.wasted_tokens += granted
                self.cut_off += 1
                self.boost *= RETRY_GROWTH
                return 0
            self.tasks.pop(0)
            self.completed_value += task.value
            self.completed_tasks += 1
            self.boost = 1.0
            return granted - task.tokens
        left = granted
        while self.tasks and left >= self.tasks[0].tokens:
            task = self.tasks.pop(0)
            left -= task.tokens
            self.completed_value += task.value
            self.completed_tasks += 1
        if self.tasks and left:
            self.wasted_tokens += left  # starts the next task anyway and gets cut off
            self.cut_off += 1
            return 0
        return left


def make_agents(count: int, task_count: int, strategy: str, seed: int = 0, noise: float = 0.0) -> list[Agent]:
    """Same seed gives the same tasks for every strategy, so comparisons are paired.

    Real cost = estimate x uniform(1 - noise, 1 + noise). Aware agents reserve for the 95th
    percentile of that error, as they would from usage history; billing is per token used, so
    an oversized reservation costs nothing once the unused part is refunded.
    """
    rng = random.Random(seed)
    cost_rng = random.Random(f"cost-{seed}")  # separate stream: estimates and values match across noise levels
    agents = []
    for i in range(count):
        tasks = []
        for _ in range(task_count):
            estimate = rng.randint(50, 300)
            value = round(estimate * rng.uniform(0.5, 3.0), 2)
            tasks.append(Task(estimate, round(estimate * cost_rng.uniform(1 - noise, 1 + noise)), value))
        # "mixed": one greedy agent among aware ones, the budget-hog case from the brief.
        agent_strategy = ("naive" if i == 0 else "mechanism_aware") if strategy == "mixed" else strategy
        agents.append(Agent(f"agent_{i+1}", tasks, agent_strategy, margin=1 + 0.9 * noise))
    return agents
