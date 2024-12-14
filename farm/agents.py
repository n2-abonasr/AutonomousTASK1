import mesa
import random

NUMBER_OF_CELLS = 50
BUSY = 0
FREE = 1
UNDONE = 0
DONE = 1
MAX_STORAGE = 3  # Maximum storage capacity for the robot
RECHARGE_THRESHOLD = 20  # Battery level at which the robot goes to recharge
RECHARGE_STEP_THRESHOLD = 80  # Step count at which the robot goes to recharge

class Tree(mesa.Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = None  # Add state attribute

class Water(mesa.Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = None  # Add state attribute

class Strawberry(mesa.Agent):
    def __init__(self, id, pos, model, init_state=UNDONE):
        super().__init__(id, model)
        self.state = UNDONE
        self.x, self.y = pos

class RechargeStation(mesa.Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.x, self.y = pos

class PickerRobot(mesa.Agent):
    def __init__(self, id, pos, model, init_state=FREE):
        super().__init__(id, model)
        self.x, self.y = pos
        self.next_x, self.next_y = pos  # Initialize next_x and next_y with the current position
        self.state = init_state
        self.payload = []
        self.battery = 100  # Battery level
        self.speed = 1  # Normal speed
        self.water_speed = 0.5  # Speed when moving through water
        self.storage = 0  # Current storage
        self.target = None  # Target strawberry
        self.steps = 0  # Step counter
        self.direction = (1, 0)  # Initial direction (right)
        self.column = 0  # Current column group
        self.recharging = False  # Flag to indicate if the robot is recharging

    @property
    def isBusy(self):
        return self.state == BUSY
    
    def pick(self):
        if isinstance(self.target, Strawberry) and self.target.state == UNDONE:
            self.target.state = DONE  # Update the strawberry's state
            self.storage += 1
            self.state = BUSY


    def step(self):
        if self.battery > 0:
            if self.steps >= RECHARGE_STEP_THRESHOLD or self.recharging:
                self.go_to_recharge()
            else:
                action = getattr(self, self.make_decision())
                action()
                self.battery -= 1  # Deplete battery over time
                self.steps += 1  # Increment step counter

    def make_decision(self):
        action = "wait"
        if self.battery <= RECHARGE_THRESHOLD:
            action = "go_to_recharge"
        elif self.state == FREE:
            if self.storage >= MAX_STORAGE:
                action = "return_to_base"
            else:
                if self.target is None or self.target.state == DONE:
                    self.target = self.find_nearest_strawberry()
                next_position = self.get_next_position()
                if self.is_strawberry(next_position):
                    action = "pick"
                else:
                    action = "move_fw"
        else:
            if self.pos and self.pos[0] == 0:
                action = "drop_off"
            else:
                action = "move_left"
        return action

    def is_strawberry(self, pos):
        return any(isinstance(agent, Strawberry) for agent in self.model.grid.get_cell_list_contents(pos))

    def find_nearest_strawberry(self):
        strawberries = [a for a in self.model.schedule.agents if isinstance(a, Strawberry) and a.state == UNDONE]
        if strawberries:
            return min(strawberries, key=lambda s: abs(s.x - self.x) + abs(s.y - self.y))
        return None

    def get_next_position(self):
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            if abs(dx) > abs(dy):
                next_x = self.x + (1 if dx > 0 else -1)
                next_y = self.y
            else:
                next_x = self.x
                next_y = self.y + (1 if dy > 0 else -1)
        else:
            next_x, next_y = self.x, self.y

        # Add some randomness to the movement
        if random.random() < 0.1:  # 10% chance to move randomly
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                next_x = self.x + dx
                next_y = self.y + dy
                if 0 <= next_x < self.model.grid.width and 0 <= next_y < self.model.grid.height:
                    if not any(isinstance(agent, Tree) for agent in self.model.grid.get_cell_list_contents((next_x, next_y))):
                        return (next_x, next_y)

        if 0 <= next_x < self.model.grid.width and 0 <= next_y < self.model.grid.height:
            if not any(isinstance(agent, Tree) for agent in self.model.grid.get_cell_list_contents((next_x, next_y))):
                return (next_x, next_y)
        return (self.x, self.y)

    def move(self):
        if self.next_x is not None and self.next_y is not None:
            if 0 <= self.next_x < self.model.grid.width and 0 <= self.next_y < self.model.grid.height:
                if self.model.grid.is_cell_empty((self.next_x, self.next_y)):
                    self.model.grid.move_agent(self, (self.next_x, self.next_y))

    def move_left(self):
        self.next_x = self.x - 1
        self.next_y = self.y
        if 0 <= self.next_x < self.model.grid.width and 0 <= self.next_y < self.model.grid.height:
            self.move()

    def move_payload(self):
        strawberry = [a for a in self.model.schedule.agents if isinstance(a, Strawberry) and a.unique_id == self.payload]
        if len(strawberry) > 0:
            self.model.grid.move_agent(strawberry[0], (self.x, self.y))

    def wait(self):
        self.next_x = self.x
        self.next_y = self.y

    def move_fw(self):
        self.next_x, self.next_y = self.get_next_position()
        if self.next_x < self.model.grid.width and self.next_y < self.model.grid.height:
            if any(isinstance(agent, Water) for agent in self.model.grid.get_cell_list_contents((self.next_x, self.next_y))):
                self.speed = self.water_speed  # Reduce speed when moving through water
            else:
                self.speed = 1  # Normal speed on land
            self.move()

    def move_bw(self):
        self.next_x, self.next_y = self.get_next_position()
        if self.next_x >= 0 and self.next_y >= 0:
            if any(isinstance(agent, Water) for agent in self.model.grid.get_cell_list_contents((self.next_x, self.next_y))):
                self.speed = self.water_speed  # Reduce speed when moving through water
            else:
                self.speed = 1  # Normal speed on land
            self.move()
        self.move_payload()

    def pick(self):
        self.state = BUSY
        nbs = [nb for nb in self.model.grid.get_neighbors((self.x, self.y), False)]
        for i in range(len(nbs)):
            if isinstance(nbs[i], Strawberry):
                strawberry = nbs[0]
                self.payload = strawberry.unique_id
                self.storage += 1  # Increase storage
                if strawberry.x is not None and strawberry.y is not None:
                    self.model.grid.remove_agent(strawberry)  # Remove the picked strawberry
                if self.storage >= MAX_STORAGE:
                    self.return_to_base()  # Return to base after picking 3 strawberries

    def drop_off(self):
        self.state = FREE
        self.payload = None
        self.storage = 0  # Reset storage
        self.next_x, self.next_y = self.get_next_position()
        self.move()

    def return_to_base(self):
        # Logic to return to base station
        self.next_x, self.next_y = 0, self.y  # Move straight to the left
        self.move()

    def go_to_recharge(self):
        # Logic to go to recharge station
        recharge_station = [a for a in self.model.schedule.agents if isinstance(a, RechargeStation)][0]
        if self.x > recharge_station.x:
            self.next_x = self.x - 1
        elif self.x < recharge_station.x:
            self.next_x = self.x + 1
        else:
            self.next_x = self.x

        if self.y > recharge_station.y:
            self.next_y = self.y - 1
        elif self.y < recharge_station.y:
            self.next_y = self.y + 1
        else:
            self.next_y = self.y

        self.move()
        if self.x == recharge_station.x and self.y == recharge_station.y:
            self.recharging = True
            self.battery = 100  # Recharge battery
            self.steps = 0  # Reset step counter
            self.recharging = False

    def advance(self):
        self.x = self.next_x
        self.y = self.next_y

class ExplorerDrone(mesa.Agent):
    def __init__(self, id, pos, model, strawberry):
        super().__init__(id, model)
        self.x, self.y = pos
        self.strawberry = strawberry
        self.state = None  # Add state attribute

    def step(self):
        # Move randomly within a 6-block radius
        dx = self.random.randint(-1, 1)
        dy = self.random.randint(-1, 1)
        new_x = self.strawberry.x + dx
        new_y = self.strawberry.y + dy

        if abs(new_x - self.strawberry.x) <= 6 and abs(new_y - self.strawberry.y) <= 6:
            if 0 <= new_x < self.model.grid.width and 0 <= new_y < self.model.grid.height:
                self.model.grid.move_agent(self, (new_x, new_y))
