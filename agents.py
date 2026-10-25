"""Synthetic agents and measurable tasks."""
from dataclasses import dataclass
from allocation import Bid


@dataclass(frozen=True)
class Task:
    tokens: int
    value: float


class Agent:
    def __init__(self, agent_id: str, tasks: list[Task], strategy: str):
        self.agent_id = agent_id
        self.tasks = list(tasks)
        self.strategy = strategy
        self.completed_value = 0.0
        self.completed_tasks = 0

    @property
    def remaining_tokens(self) -> int:
        return sum(t.tokens for t in self.tasks)

    def bid(self, mechanism: str) -> Bid:
        demand = self.remaining_tokens
        if not demand:
            return Bid(0, 0)
        value_rate = sum(t.value / t.tokens for t in self.tasks) / len(self.tasks)
        if self.strategy == "naive":
            return Bid(demand, max(1.0, value_rate * 2))
        # The aware strategy requests task-sized work and changes its signal by rule.
        request = min(demand, self.tasks[0].tokens)
        multiplier = {"proportional_fair": 1.0, "priority_auction": 1.25, "vcg": 1.0}[mechanism]
        return Bid(request, value_rate * multiplier)

    def consume(self, tokens: int) -> None:
        left = tokens
        while self.tasks and left >= self.tasks[0].tokens:
            task = self.tasks.pop(0)
            left -= task.tokens
            self.completed_value += task.value
            self.completed_tasks += 1


def make_agents(count: int, task_count: int, strategy: str) -> list[Agent]:
    agents = []
    for i in range(count):
        tasks = [Task(tokens=10 + ((i + j) % 3) * 5, value=10.0 + ((i * 3 + j * 2) % 9)) for j in range(task_count)]
        agents.append(Agent(f"agent_{i+1}", tasks, strategy))
    return agents
