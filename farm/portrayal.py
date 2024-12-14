from farm.agents import PickerRobot, Strawberry, ExplorerDrone, Tree, Water

def farm_portrayal(agent):
    if isinstance(agent, PickerRobot):
        return robot_portrayal(agent)
    elif isinstance(agent, Strawberry):
        return strawberry_portrayal(agent)
    elif isinstance(agent, ExplorerDrone):
        return drone_portrayal(agent)
    elif isinstance(agent, Tree):
        return tree_portrayal(agent)
    elif isinstance(agent, Water):
        return water_portrayal(agent)

def robot_portrayal(robot):
    return {
        "Shape": "arrowHead",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": robot.x,
        "y": robot.y,
        "scale": 2,
        "heading_x": -1 if robot.isBusy else 1,
        "heading_y": 0,
        "Color": "red" if robot.isBusy else "green",
    }

def strawberry_portrayal(strawberry):
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": strawberry.x,
        "y": strawberry.y,
        "Color": "pink",
    }

def drone_portrayal(drone):
    return {
        "Shape": "circle",
        "r": 1,
        "Filled": "true",
        "Layer": 1,
        "x": drone.x,
        "y": drone.y,
        "Color": "yellow",
    }

def tree_portrayal(tree):
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": tree.x,
        "y": tree.y,
        "Color": "green",
    }

def water_portrayal(water):
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": water.x,
        "y": water.y,
        "Color": "blue",
    }