from mesa import Agent, Model
from mesa.time import StagedActivation
from mesa.datacollection import DataCollector
import numpy as np
import random

class OpinionAgent(Agent):
    """ An agent with random initial opinion."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = np.random.rand()
        self.didInteract = False

    def reset(self):
        self.didInteract = False

    def step(self):
        if self.didInteract:
            return

        self.didInteract = True

        indices = list(range(self.model.num_agents))
        random.shuffle(indices)

        for i in indices:
            other_agent = self.model.schedule.agents[i]
            if other_agent.unique_id == self.unique_id:
                continue
            if other_agent.didInteract:
                continue
            break
        else:
            # nobody to interact with. :-(
            self.didInteract = True
            return

        delt = self.opinion - other_agent.opinion
        adelt = np.abs(delt)

        new_opinion = self.opinion - (adelt/100.0) * (adelt/delt)
        new_other = other_agent.opinion + (adelt/100.0) * (adelt/delt)

        self.opinion = new_opinion
        other_agent.opinion = new_other

class OpinionModel(Model):
    """A model with some number of agents."""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = StagedActivation(self, stage_list=["reset","step"], shuffle=True)
        # Create agents
        for i in range(self.num_agents):
            a = OpinionAgent(i, self)
            self.schedule.add(a)
        
        self.datacollector = DataCollector(
            agent_reporters = {"Opinion": lambda a: a.opinion}
        )

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()