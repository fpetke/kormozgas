import mesa
from source.model import CircularMotionModel, MovingAgent, VectorAgent, ProjectionAgent, ProjectingAgent, BackgroundAgent
from source.ContinuousCanvasModule import ContinuousCanvasModule
import numpy as np

SPACE_SIZE = 3
PADDING = .5
CANVAS_SIZE = 500

MIN_RADIUS = .2
MAX_RADIUS = 1.

MIN_PERIOD = 100
MAX_PERIOD = 1000

def portrayal_method(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is MovingAgent:
        portrayal['Shape'] = 'circle'
        portrayal['r'] = PADDING/8
        portrayal['Color'] = '#e41a1c'
        portrayal['Filled'] = True
        portrayal['Layer'] = 2
    elif type(agent) is VectorAgent:
        portrayal['Shape'] = 'arrow'
        portrayal['Color'] = 'black'
        portrayal['angle'] = agent.agent.vector_angle
        portrayal['h'] = .25 * agent.model.omega * agent.model.circle_radius / (2 * np.pi * MAX_RADIUS) * MIN_PERIOD + .1
        portrayal['Layer'] = 3
        portrayal['Filled'] = True
    elif type(agent) is ProjectionAgent and ((agent.direction_of_projection == 0 and agent.model.projection_x) or (agent.direction_of_projection == 1 and agent.model.projection_y)):
        portrayal['Shape'] = 'circle'
        portrayal['r'] = PADDING/8
        portrayal['Color'] = '#4daf4a' if agent.direction_of_projection == 0 else '#377eb8'
        portrayal['Filled'] = True
        portrayal['Layer'] = 2
    elif type(agent) is ProjectingAgent and ((agent.direction_of_projection == 0 and agent.model.projection_x) or (agent.direction_of_projection == 1 and agent.model.projection_y)):
        portrayal['Shape'] = 'rect'
        portrayal['w'] = SPACE_SIZE/1000 if agent.direction_of_projection == 0 else agent.length
        portrayal['h'] = SPACE_SIZE/1000 if agent.direction_of_projection == 1 else agent.length
        portrayal['Color'] = 'black'
        portrayal['Filled'] = True
        portrayal['Layer'] = 1
    elif type(agent) is BackgroundAgent:
        if agent.portrayal['Shape'] == 'rect' and ((agent.portrayal['w'] > agent.portrayal['h'] and agent.model.projection_x) or (agent.portrayal['w'] < agent.portrayal['h'] and agent.model.projection_y)):
            portrayal = agent.portrayal
        elif agent.portrayal['Shape'] == 'circle':
            portrayal = agent.portrayal

    return portrayal

canvas_element = ContinuousCanvasModule(portrayal_method, SPACE_SIZE, SPACE_SIZE, CANVAS_SIZE, CANVAS_SIZE)
chart = mesa.visualization.ChartModule([{'Label': 'x koordináta', 'Color': '#4daf4a'}, {'Label': 'y koordináta', 'Color': '#377eb8'}])

def text_element(model):
    return 'Szögsebesség: {:.5f} rad/időlépés<br>Kerületi sebesség: {:.5f} egység/időlépés'.format(model.omega, model.omega * model.circle_radius)

model_params = {
    'space_size': SPACE_SIZE,
    'padding': PADDING,
    'circle_radius': mesa.visualization.Slider('Körpálya sugara (egységekben)', MAX_RADIUS, MIN_RADIUS, MAX_RADIUS, MAX_RADIUS/100),
    'period': mesa.visualization.Slider('Periódus (időlépésekben)', MIN_PERIOD, MIN_PERIOD, MAX_PERIOD, 1),
    'velocity_vector': mesa.visualization.Checkbox('Sebesség-vektor', False),
    'projection_x': mesa.visualization.Checkbox('x irányú vetület', False),
    'projection_y': mesa.visualization.Checkbox('y irányú vetület', False)
}

server = mesa.visualization.ModularServer(CircularMotionModel, [text_element, canvas_element, chart], 'Körmozgás', model_params)
server.port = 8521
