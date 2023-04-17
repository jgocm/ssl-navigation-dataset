# Import libraries
import csv
import numpy as np

class FieldReader:
    def __init__(self, 
                 path):
        self.path = path
        self.field_data = {}

    def read_file(self):
        with open(self.path, 'r') as f:
            for line in f:
                key, value = line.strip().split(': ')
                self.field_data[key] = float(value)

    def get_field_data(self):
        if not self.field_data:
            self.read_file()
        return self.field_data

class LogReader:
    def __init__(self, 
                 path, 
                 degrees = False,
                 is_raw = True):
        self.path = path
        self.frames = []
        self.odometry = []
        self.position = []
        self.speed = []
        self.goal_in_fov = []
        self.has_goal = []
        self.goal_bounding_box = []
        self.timestamps = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    self.frames.append(int(row[0]))
                    self.robotId = row[1]
                    if degrees:
                        self.odometry.append([float(row[2]), float(row[3]), np.rad2deg(float(row[4]))])
                    else:
                        self.odometry.append([float(row[2]), float(row[3]), float(row[4])])

                    if degrees:
                        self.position.append([float(row[5]), float(row[6]), np.rad2deg(float(row[7]))])
                    else:
                        self.position.append([float(row[5]), float(row[6]), float(row[7])])
                    self.speed.append([float(row[8]), float(row[9]), float(row[10])])
                    if not is_raw:
                        self.goal_in_fov.append(True if row[11]=='True' else False)
                        self.has_goal.append(True if row[12]=='True' else False)
                        self.goal_bounding_box.append([float(row[13]), float(row[14]), float(row[15]), float(row[16])])
                        self.timestamps.append(float(row[17]))      
                    else:
                        self.has_goal.append(True if row[11]=='True' else False)
                        self.goal_bounding_box.append([float(row[12]), float(row[13]), float(row[14]), float(row[15])])
                        self.timestamps.append(float(row[16]))
                    line_count += 1

    def get_odometry(self):
        return np.array(self.odometry)
    
    def get_odometry_2d(self):
        return np.array(self.odometry)[:,0:2]

    def get_odometry_vectors(self):
        odm = self.get_odometry()
        return np.array([odm[:, 0] + np.cos(odm[:, 2]), odm[:, 1] + np.sin(odm[:, 2])]).T

    def get_position(self):
        return np.array(self.position)

    def get_position_2d(self):
        return np.array(self.position)[:,0:2]
    
    def get_speed(self):
        return np.array(self.speed)

    def get_speed_2d(self):
        return np.array(self.speed)[:,0:2]
    
    def get_position_vectors(self):
        vis = self.get_position()
        return np.array([vis[:, 0] + np.cos(vis[:, 2]), vis[:, 1] + np.sin(vis[:, 2])]).T

    def get_first_frame(self):
        return self.frames[0]

    def get_frames(self):
        return np.array(self.frames)
    
    def get_timestamps(self):
        return np.array(self.timestamps)
    
    def get_has_goals(self):
        return np.array(self.has_goal)
    
    def get_goals(self):
        return np.array(self.goal_bounding_box)

    def get_path(self):
        return self.path

    def get_steps(self):
        '''
        Result: pckt_count[n] == sum(steps[:n+1]) + pckt_count[0]
        '''
        steps = []
        for i in range (0, len(self.get_frames())):
            step = i
            steps.append(step)
        return np.array(steps)

    def limit_angle(self, angle):
        while angle>np.pi:
            angle -= 2*np.pi
        while angle<-np.pi:
            angle += 2*np.pi
        return angle

    def get_odometry_movement(self, degrees=False, local=False):
        '''
        Result: odometry[n] == sum(odometry_movement[:n+1]) + odometry[0]
        '''
        odometry_movement = [[0,0,0]]
        odometry = self.get_odometry()
        for i in range(1,len(odometry)):
            movement = list(odometry[i] - odometry[i-1])
            movement[2] = self.limit_angle(movement[2])
            if degrees: movement[2] = np.degrees(movement[2])
            odometry_movement.append(movement)
        return np.array(odometry_movement)

    def get_position_movement(self, degrees=False):
        '''
        Result: position[n] == sum(position_movement[:n+1]) + position[0]
        '''
        position_movement = [[0,0,0]]
        position = self.get_position()
        for i in range(1,len(position)):
            movement = list(position[i] - position[i-1])
            movement[2] = self.limit_angle(movement[2])
            if degrees: movement[2] = np.degrees(movement[2])
            position_movement.append(movement)
        return np.array(position_movement)
    
    def rotate_to_local(self, global_x, global_y, robot_w):
        local_x = global_x*np.cos(robot_w) + global_y*np.sin(robot_w)
        local_y = -global_x*np.sin(robot_w) + global_y*np.cos(robot_w)
        return local_x, local_y

    def get_timesteps(self):
        '''
        Result: timestamps[n] == timesteps[:n+1] + timestamps[0]
        '''
        timesteps = [0]
        timestamps = self.get_timestamps()
        for i in range(1,len(timestamps)):
            # import pdb;pdb.set_trace()
            timestep = timestamps[i] - timestamps[i-1]
            timesteps.append(timestep)
        return np.array(timesteps)
    
    def get_timesteps_average(self):
        timesteps = self.get_timesteps()
        return np.mean(timesteps)
        
def test_odometry_movements_reader(data):
    odometry_movements = data.get_odometry_movement(degrees=True)
    for i in range(1, len(odometry_movements)):
        movement = odometry_movements[i]
        if movement[2]>0: 
            print(movement[2], data.frames[i])    

def test_has_goal_reader(data):
    frames = data.get_frames()
    has_goals = data.get_has_goals()
    for (has_goal, frame_nr) in zip(has_goals, frames):
        print(has_goal, frame_nr)

def test_field_reader(path):
    from libs.Utils.entities import Field

    field_info = FieldReader(path)

    # Get the field data as a dictionary
    data_dict = field_info.get_field_data()

    # Create Field object from text file
    field = Field().set_field_dimensions_from_txt(data_dict)

    # Print dimensions for debug
    field.print_dimensions()

def test_log_reader(path):
    quadrado_nr = 15
    data = LogReader(path)

    #test_odometry_movements_reader(data)
    test_has_goal_reader(data)

if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    path = '/home/rc-blackout/ssl-navigation-dataset/configs/field_dimensions.txt'
    test_field_reader(path)





