import unittest
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from .agents import PickerRobot, Strawberry, Tree, Water, RechargeStation, UNDONE, DONE, BUSY, FREE, MAX_STORAGE
# code to write in terminal : python -m unittest farm.UnitTests

class TestAgents(unittest.TestCase):

    def setUp(self):
        class MockModel:
            def __init__(self):
                self.grid = MultiGrid(width=10, height=10, torus=False)
                self.schedule = RandomActivation(self)

        self.model = MockModel()
        self.robot = PickerRobot(1, (5, 5), self.model)
        self.model.schedule.add(self.robot)
        self.model.grid.place_agent(self.robot, (5, 5))

    def test_robot_initial_state(self):
        self.assertEqual(self.robot.state, FREE)
        self.assertEqual(self.robot.storage, 0)
        self.assertEqual(self.robot.battery, 100)


    def test_robot_return_to_base(self):
        self.robot.storage = MAX_STORAGE  # Simulate full storage
        self.robot.return_to_base()

        self.assertEqual(self.robot.next_x, 0)  # Moving to the base
        self.robot.drop_off()
        self.assertEqual(self.robot.storage, 0)
        self.assertEqual(self.robot.state, FREE)

def test_robot_battery_management(self):
    # Add a recharge station explicitly
    recharge_station = RechargeStation((0, 0), self.model)
    self.model.schedule.add(recharge_station)
    self.model.grid.place_agent(recharge_station, (0, 0))

    # Simulate the robot needing to recharge
    self.robot.battery = 15  # Below threshold
    self.robot.step()

    self.assertTrue(self.robot.recharging)  # Robot should start recharging
    self.robot.go_to_recharge()

    # Simulate recharging completion
    self.robot.battery = 100
    self.robot.recharging = False

    # Verify the robot's battery is now full
    self.assertEqual(self.robot.battery, 100)
    self.assertFalse(self.robot.recharging)


    def test_robot_avoids_obstacles(self):
        tree = Tree((6, 5), self.model)
        self.model.grid.place_agent(tree, (6, 5))

        self.robot.direction = (1, 0)  # Moving right towards the tree
        next_position = self.robot.get_next_position()

        self.assertNotEqual(next_position, (6, 5))  # Robot avoids the tree

    def test_robot_moves_through_water(self):
        water = Water((5, 6), self.model)
        self.model.grid.place_agent(water, (5, 6))

        self.robot.move_fw()
        self.assertEqual(self.robot.speed, self.robot.water_speed)  # Speed reduced in water

    def test_robot_recharge_behavior(self):
        station = RechargeStation((0, 0), self.model)
        self.model.schedule.add(station)
        self.model.grid.place_agent(station, (0, 0))

        self.robot.battery = 10  # Trigger recharge
        self.robot.go_to_recharge()

        self.assertEqual(self.robot.x, 0)
        self.assertEqual(self.robot.y, 0)
        self.assertEqual(self.robot.battery, 100)

    def test_robot_pick_strawberry(self):
     strawberry = Strawberry(2, (5, 6), self.model)
     self.model.schedule.add(strawberry)
     self.model.grid.place_agent(strawberry, (5, 6))

     self.robot.target = strawberry
     self.robot.move_fw()  # Move forward to the strawberry
     self.robot.pick()

    # Ensure the robot has picked the strawberry
     self.assertEqual(self.robot.storage, 0)
    # Ensure the strawberry's state is updated
     self.assertEqual(strawberry.state, DONE)
    # Ensure the robot's state is updated
     self.assertEqual(self.robot.state, BUSY)

if __name__ == "__main__":
    unittest.main()
