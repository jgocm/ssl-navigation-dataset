from libs.Utils.particle_vision import ParticleVision
from libs.Utils.entities import Field
from libs.Utils import utils
import os

def main(scenario = 'sqr', lap = 1):
    cwd = os.getcwd()

    # PATH TO LOG DATA
    path = cwd + f'/data/{scenario}_0{lap}'

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

    utils.get_dataset_characteristcs(path = path)

if __name__ == "__main__":

    # CHOOSE SCENARIO
    scenario = 'igs'
    lap = 3
    #main(scenario, lap)