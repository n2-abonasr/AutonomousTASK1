from pydoc import doc
import mesa
import numpy as np
from farm.agents import PickerRobot, ExplorerDrone, Strawberry, Tree, Water, RechargeStation
from .agents import DONE, FREE, BUSY

class farm(mesa.Model):
    def __init__(self, n_robots=2, n_strawberries=20, n_drones=2, width=50, height=50, seed=123):
        self.tick = 0
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.n_robots = n_robots
        self.n_strawberries = n_strawberries
        self.n_drones = n_drones
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        y_s = []
        for n in range(self.n_robots):
            heading = (1, 0)
            x = 1
            y = 1
            while True:
                y = self.random.randint(1, height - 1)
                if self.grid.is_cell_empty((x, y)):
                    break
            y_s.append(y)
            pr = PickerRobot(n, (x, y), self)
            self.schedule.add(pr)
            self.grid.place_agent(pr, (x, y))

        for n in range(self.n_strawberries):
            x = 1
            y = 1
            while True:
                x = self.random.randint(2, 6)  # Place strawberries in the first 5 blocks beside the robots
                y = self.random.choice(y_s)
                if self.grid.is_cell_empty((x, y)):
                    break
            s = Strawberry(n + self.n_robots, (x, y), self)
            self.schedule.add(s)
            self.grid.place_agent(s, (x, y))

        # Add trees in rows of 3
        for x in range(3, width, 3):
            for y in range(0, height, 3):
                while not self.grid.is_cell_empty((x, y)):
                    y += 1
                    if y >= height:
                        y = 0
                        x += 3
                tree = Tree((x, y), self)
                self.schedule.add(tree)
                self.grid.place_agent(tree, (x, y))

        # Add river in the 7th line of blocks from the left
        for y in range(height):
            while not self.grid.is_cell_empty((7, y)):
                y += 1
                if y >= height:
                    y = 0
            water = Water((7, y), self)
            self.schedule.add(water)
            self.grid.place_agent(water, (7, y))

        # Add recharge station
        recharge_station = RechargeStation((0, 0), self)  # Place recharge station at bottom left corner
        self.schedule.add(recharge_station)
        self.grid.place_agent(recharge_station, (0, 0))

        # Add drones
        for n in range(self.n_drones):
            strawberry = self.random.choice([a for a in self.schedule.agents if isinstance(a, Strawberry)])
            x = strawberry.x + self.random.randint(-1, 1)
            y = strawberry.y + self.random.randint(-1, 1)
            while not self.grid.is_cell_empty((x, y)):
                x = strawberry.x + self.random.randint(-1, 1)
                y = strawberry.y + self.random.randint(-1, 1)
            drone = ExplorerDrone(n + self.n_robots + self.n_strawberries, (x, y), self, strawberry)
            self.schedule.add(drone)
            self.grid.place_agent(drone, (x, y))

        self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={"pending_strawberries": self.pending_strawberries},
            agent_reporters={"state": lambda a: getattr(a, 'state', None)}
        )

    def pending_strawberries(self):
        return len([a for a in self.schedule.agents if isinstance(a, Strawberry) and a.state != DONE])

    def step(self):
        self.tick += 1
        if len([a for a in self.schedule.agents if isinstance(a, Strawberry) and a.state != DONE]) > 0:
            self.schedule.step()
        else:
            self.running = False
        self.datacollector.collect(self)
