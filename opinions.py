# Naive implementation of the opinion game. For now, agents are totally connected.
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np
import random

ALPHA = .01 #TEMPORARY, in the future ALPHA should be able to be passed by the user & varied. Recall alpha measures learning rate.
def potential_prime(diff):
    '''
    Tent function potential, tip at .5
    '''
    if(diff < .5):
        return 1
    elif(diff > .5):
        return -1
    else:
        return 0


class OpinionAgent(Agent):
    '''
    An agent has an opinion, and is inlfuenced by other agent's opinions based off a potential energy function. For now, initial opinion of an agent is random
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model) # sets self.model
        self.opinion = np.random.rand() #From 0 to 1
        self.nextOpinion = None
    
    def step(self):
        '''
        Calculates next opinion based off of all other agent's opinions. Models a totally connected graph.
        o_i^(t+1) = o_i^t + sum(j = 1 to k, (- alpha / 2) * potential'(|diff|) * diff/ |diff| is the formula for the  next opinion from the paper. 
        '''
        # self.model.schedule.agents is a list containing all other agents.
        self.nextOpinion = self.opinion
        
        # This calculates the next opinion based off the formula
        for other in self.model.schedule.agents[:]:
            difference = self.opinion - other.opinion
            if difference == 0: #Don't calculate for the same node. Unsure what to do if there are other nodes of the same opinion, probably doesn't matter at this point
                pass;
            else:
                self.nextOpinion += ((-1) * ALPHA / 2) * potential_prime(abs(difference)) * (difference / abs(difference))

        # Clamp function
        if self.nextOpinion > 1:
            self.nextOpinion = 1
        elif self.nextOpinion < 0:
            self.nextOpinion = 0
        

    def advance(self):
        self.opinion = self.nextOpinion
        self.nextOpinion = None

class OpinionModel(Model):
    '''A model with some number of agents'''
    def __init__(self, N):
        self.num_agents = N
        self.schedule = SimultaneousActivation(self)
        #Create agents
        for i in range(self.num_agents):
            a = OpinionAgent(i, self)
            self.schedule.add(a)
        self.datacollector = DataCollector(
                agent_reporters = {"Opinion": lambda a: a.opinion}
        )
    def step(self):
        '''Advance the model one step'''
        self.datacollector.collect(self)
        self.schedule.step()
