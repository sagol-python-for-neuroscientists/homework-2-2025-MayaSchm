from enum import Enum
from collections import namedtuple
from itertools import zip_longest

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))

def resolve_meeting(agent1: Agent, agent2: Agent) -> tuple:
    if agent1.category == Condition.CURE and agent2.category in (Condition.SICK, Condition.DYING):
        agent2 = Agent(agent2.name, Condition(agent2.category.value - 1))
    elif agent2.category == Condition.CURE and agent1.category in (Condition.SICK, Condition.DYING):
        agent1 = Agent(agent1.name, Condition(agent1.category.value - 1))
    elif agent1.category == Condition.SICK and agent2.category == Condition.DYING:
        agent1 = Agent(agent1.name, Condition.DYING)
        agent2 = Agent(agent2.name, Condition.DEAD)
    elif agent2.category == Condition.SICK and agent1.category == Condition.DYING:
        agent2 = Agent(agent2.name, Condition.DYING)
        agent1 = Agent(agent1.name, Condition.DEAD)
    elif agent1.category == agent2.category == Condition.DYING:
        agent1 = Agent(agent1.name, Condition.DEAD)
        agent2 = Agent(agent2.name, Condition.DEAD)

    return agent1, agent2

def meetup(agent_listing: tuple) -> list:
    active_agents = [agent for agent in agent_listing if agent.category not in (Condition.HEALTHY, Condition.DEAD)]
    inactive_agents = [agent for agent in agent_listing if agent.category in (Condition.HEALTHY, Condition.DEAD)]

    updated_agents = []

    for agent1, agent2 in zip_longest(active_agents[::2], active_agents[1::2]):
        if agent2 is None:
            updated_agents.append(agent1)
        else:
            updated_agents.extend(resolve_meeting(agent1, agent2))

    updated_agents.extend(inactive_agents)

    return updated_agents 