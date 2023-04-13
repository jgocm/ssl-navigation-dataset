from src.Utils.particle_vision import ParticleVision
from src.Utils.entities import Field
from src.Utils import utils
import os

if __name__ == "__main__":
    cwd = os.getcwd()

    # CONFIG SCENARIO
    scenario = 'rnd'
    round = '02'

    # PATH TO LOG DATA
    path = cwd + f'/data/{scenario}_{round}'

    # CONFIGURE FIELD DIMENSIONS
    field = Field(boundary_width = 0.3)
    field.set_field_limits(x_min = -0.3,
                           x_max = 4.2,
                           y_min = -3,
                           y_max = 3)
    
    # SIMULATE ROBOT VISION
    embedded_vision = ParticleVision(FOV = 64)

    utils.process_data(path = path, 
                       field = field,
                       embedded_vision = embedded_vision,
                       debug = False)