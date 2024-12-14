import mesa
from farm.model import farm
from .portrayal import farm_portrayal
from .agents import NUMBER_OF_CELLS

SIZE_OF_CANVAS_IN_PIXELS_X = 400
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "height": NUMBER_OF_CELLS,
    "width": NUMBER_OF_CELLS,
    "n_robots": mesa.visualization.Slider(
        'number of robots',
        2,
        1,
        10,
        1,
        "choose how many robots to include in the simulation"
    ),
    "n_strawberries": mesa.visualization.Slider(
        'number of strawberries',
        5,
        1,
        20,
        1,
        "choose how many strawberries to include in the simulation",
    ),
    "n_drones": mesa.visualization.Slider(
        'number of drones',
        2,
        1,
        5,
        1,
        "choose how many drones to include in the simulation",
    )
}

grid = mesa.visualization.CanvasGrid(farm_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)

server = mesa.visualization.ModularServer(
    farm, [grid], "farm ", simulation_params
)