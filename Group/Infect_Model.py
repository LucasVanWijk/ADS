from mesa import Model
from parallel import SimultaneousActivation
from mesa.space import MultiGrid
from Infect_Agents import Infect_Agent, Work, Recreation
from mesa.datacollection import DataCollector
import datetime
import random


def compute_infected(model):
    return sum([1 if agent.infected else 0 for agent in model.schedule.agents ])


class BaseModel(Model):
    """A model with some number of agents."""
    def __init__(self, healthy_N, sick_N, width, height, work_n, rec_n, infect_chanse=0.2, seed=41, min_per_step=10,  ini_date=datetime.datetime(2020, 1, 1, 00, 00)):
        self.parallel_amount = 16
        self.healthy_agents = healthy_N
        self.sick_agent = sick_N
        self.min_per_step = min_per_step
        self.ini_date = ini_date
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.date = ini_date
        self.work = []
        self.recreation = []
        self.infect_chanse = infect_chanse
        random.seed(seed)

        # build work
        for i in range(work_n):
            w, h = random.randrange(0, width), random.randrange(0, height)
            work = Work(i, self)
            self.grid.place_agent(work, (w, h))
            self.work.append((w, h))

        # build recreations
        for i in range(rec_n):
            w, h = random.randrange(0, width), random.randrange(0, height)
            recreation = Recreation(i, self)
            self.grid.place_agent(recreation, (w, h))
            self.recreation.append((w, h))

        # infected agent
        for i in range(self.sick_agent):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Infect_Agent(i, self, (x,y), infected=True)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (x, y))

        # Create healthy agents
        for i in range(self.sick_agent,self.sick_agent+ self.healthy_agents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Infect_Agent(i, self, (x,y), infected=False)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (x, y))
        
        self.datacollector = DataCollector(
            model_reporters={"infected": compute_infected})
            
    def step(self):
        #time = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.time)
        self.date = self.ini_date + datetime.timedelta(minutes= self.min_per_step * self.schedule.steps)
        self.datacollector.collect(self)
        self.schedule.step()