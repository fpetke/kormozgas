import mesa
import numpy as np

class CircularMotionModel(mesa.Model):
    def __init__(self,
        space_size = 10.,
        padding = 2.,
        circle_radius = 1.,
        period = 200,
        velocity_vector: bool = False,
        projection_x: bool = False,
        projection_y: bool = False,
    ) -> None:
        super().__init__()
        self.space_size = space_size
        self.padding = padding
        self.space = mesa.space.ContinuousSpace(space_size, space_size, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.circle_radius = circle_radius
        self.omega = 2 * np.pi / period
        self.projection_x = projection_x
        self.projection_y = projection_y

        pos = self.get_coordinates(0.)
        self.agent = MovingAgent(self.next_id(), self, pos)
        self.space.place_agent(self.agent, pos)
        self.schedule.add(self.agent)

        if velocity_vector:
            self.space.place_agent(VectorAgent(self.next_id(), self, self.agent, pos), pos)
        for i in range(len(pos)):
            pos_projection = np.array([space_size-padding/2, padding/2])
            pos_projection[i] = pos[i]
            self.space.place_agent(ProjectionAgent(self.next_id(), self, self.agent, pos_projection), pos_projection)

        pos_background = np.array([(self.space_size - self.padding)/2, (self.space_size + self.padding)/2])
        portrayal = {
            'Shape': 'circle',
            'r': circle_radius,
            'Color': '#b4b8b5',
            'Filled': False,
            'Layer': 0
        }
        self.space.place_agent(BackgroundAgent(self.next_id(), self, pos_background, portrayal), pos_background)

        pos_background = np.array([(self.space_size - self.padding)/2, (self.space_size + self.padding)/2])
        portrayal = {
            'Shape': 'circle',
            'r': space_size/200,
            'Color': '#b4b8b5',
            'Filled': True,
            'Layer': 0
        }
        self.space.place_agent(BackgroundAgent(self.next_id(), self, pos_background, portrayal), pos_background)

        pos_background = np.array([(space_size-padding)/2, padding/2])
        portrayal = {
            'Shape': 'rect',
            'w': circle_radius*2,
            'h': padding/4,
            'Color': '#b4b8b5',
            'Filled': True,
            'Layer': 0
        }
        self.space.place_agent(BackgroundAgent(self.next_id(), self, pos_background, portrayal), pos_background)

        pos_background = np.array([space_size-padding/2, (space_size+padding)/2])
        portrayal = {
            'Shape': 'rect',
            'w': padding/4,
            'h': circle_radius*2,
            'Color': '#b4b8b5',
            'Filled': True,
            'Layer': 0
        }
        self.space.place_agent(BackgroundAgent(self.next_id(), self, pos_background, portrayal), pos_background)

        datacollector = {}
        if projection_x:
            datacollector['x koordináta'] = (lambda m: m.agent.pos[0]-(m.space_size-m.padding)/2)
        if projection_y:
            datacollector['y koordináta'] = (lambda m: m.agent.pos[1]-(m.space_size+m.padding)/2)
        self.datacollector = mesa.DataCollector(datacollector)

        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self):
        while True:
            self.step()

    def get_coordinates(self, angle):
        return np.array([np.cos(angle), np.sin(angle)]) * self.circle_radius + np.array([(self.space_size-self.padding)/2, (self.space_size+self.padding)/2])

class MovingAgent(mesa.Agent):
    angle = None
    vector_angle = None
    vector = None
    projections = None

    def __init__(self, unique_id: int, model: CircularMotionModel, pos) -> None:
        super().__init__(unique_id, model)
        self.pos = pos
        self.angle = 0.
        self.projections = []
        self.vector_angle = np.pi/2

    def get_step_angle(self, pos):
        heading = self.model.space.get_heading(self.pos, pos)
        return np.arctan2(heading[1], heading[0])

    def step(self):
        self.angle += self.model.omega
        if self.angle >= 2*np.pi:
            self.angle -= 2*np.pi

        pos = self.model.get_coordinates(self.angle)
        self.vector_angle = self.get_step_angle(pos)

        self.model.space.move_agent(self, pos)
        if self.vector:
            self.model.space.move_agent(self.vector, pos)
        for i in range(len(self.projections)):
            pos_projection = np.copy(self.projections[i].pos)
            pos_projection[i] = pos[i]
            self.model.space.move_agent(self.projections[i], pos_projection)

            self.projections[i].projecting_agent.length = np.linalg.norm(pos_projection - pos)
            pos_projecting_agent = pos_projection + (-1 if self.projections[i].direction_of_projection == 1 else 1) * np.ones(2) * self.projections[i].projecting_agent.length / 2
            pos_projecting_agent[self.projections[i].direction_of_projection] = pos[self.projections[i].direction_of_projection]
            self.model.space.move_agent(self.projections[i].projecting_agent, pos_projecting_agent)

class ProjectionAgent(mesa.Agent):
    agent = None
    projecting_agent = None
    direction_of_projection = None

    def __init__(self, unique_id: int, model: CircularMotionModel, agent: MovingAgent, pos) -> None:
        super().__init__(unique_id, model)
        self.agent = agent
        self.pos = pos
        self.direction_of_projection = len(agent.projections)
        agent.projections.append(self)

        pos_projecting_agent = pos + (-1 if self.direction_of_projection == 1 else 1) * np.ones(2) * np.linalg.norm(pos - agent.pos) / 2
        pos_projecting_agent[self.direction_of_projection] = pos[self.direction_of_projection]
        self.projecting_agent = ProjectingAgent(model.next_id(), model, self.direction_of_projection, np.linalg.norm(pos - agent.pos))
        self.model.space.place_agent(self.projecting_agent, pos_projecting_agent)

class ProjectingAgent(mesa.Agent):
    direction_of_projection = None
    length = None

    def __init__(self, unique_id: int, model: CircularMotionModel, direction_of_projection, length) -> None:
        super().__init__(unique_id, model)
        self.direction_of_projection = direction_of_projection
        self.length = length

class VectorAgent(mesa.Agent):
    agent = None

    def __init__(self, unique_id: int, model: CircularMotionModel, agent: MovingAgent, pos) -> None:
        super().__init__(unique_id, model)
        self.agent = agent
        self.pos = pos
        agent.vector = self

class BackgroundAgent(mesa.Agent):
    def __init__(self, unique_id: int, model: CircularMotionModel, pos, portrayal) -> None:
        super().__init__(unique_id, model)
        self.pos = pos
        self.portrayal = portrayal
