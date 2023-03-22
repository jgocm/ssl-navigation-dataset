import cv2
import math
import numpy as np

class ParticleVision:
    '''
    Class for simulating embedded vision module
    '''
    def __init__(self,
                 vertical_lines_nr = 1,
                 FOV = 64):
        
        self.FOV = FOV
        self.vertical_lines_nr = vertical_lines_nr

    def limit_angle_degrees(self, angle):
        while angle>180:
            angle -= 2*180
        while angle<-180:
            angle += 2*180
        return angle
    
    def get_robot_to_positive_goal_vector(self, x, y, field):
        goal_x, goal_y = field.x_max - field.boundary_width, 0
        return goal_x - x, goal_y - y

    def get_robot_to_negative_goal_vector(self, x, y, field):
        goal_x, goal_y = field.x_min + field.boundary_width, 0
        return goal_x - x, goal_y - y

    def is_positive_goal_in_fov(self, x, y, w, field):
        x, y = self.get_robot_to_positive_goal_vector(x, y, field)
        local_angle = self.limit_angle_degrees(np.rad2deg(np.arctan2(y, x)) - w)
        if np.abs(local_angle)>self.FOV/2:
            return False
        else: 
            return True

    def is_negative_goal_in_fov(self, x, y, w, field):
        x, y = self.get_robot_to_negative_goal_vector(x, y, field)
        local_angle = self.limit_angle_degrees(np.rad2deg(np.arctan2(y, x)) - w)
        if np.abs(local_angle)>self.FOV/2:
            return False
        else: 
            return True

    def track_positive_goal_center(self, x, y, w, field):
        x, y = self.get_robot_to_positive_goal_vector(x, y, field)
        distance = np.sqrt(x**2 + y**2)
        local_angle = self.limit_angle_degrees(np.rad2deg(np.arctan2(y, x)) - w)
        if np.abs(local_angle)>30: has_goal = 0
        else: has_goal = 1

        return has_goal, distance, local_angle

    def track_negative_goal_center(self, x, y, w, field):
        x, y = self.get_robot_to_negative_goal_vector(x, y, field)
        distance = np.sqrt(x**2 + y**2)
        local_angle = np.rad2deg(np.arctan2(y, x)) - w
        if np.abs(local_angle)>30: has_goal = 0
        else: has_goal = 1

        return has_goal, distance, local_angle

if __name__ == "__main__":
    from Entities import Field

    field = Field()

    robot_x, robot_y, robot_w = 1, 2, -23

    vision = ParticleVision(vertical_lines_nr=1)
    
    has_goal, distance, local_angle = vision.track_positive_goal_center(robot_x, robot_y, robot_w, field)
    print(has_goal, distance, local_angle)
