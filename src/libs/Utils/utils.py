from libs.Reader.reader import LogReader
import numpy as np
import cv2
import csv

def del_column_from_csv(source_file_path, dest_file_path, column_index):
    # Open the CSV file and create a csv.reader object
    with open(source_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Create a list of rows
        rows = []
        for row in csv_reader:
            rows.append(row)

    # Remove the column you want to delete from each row
    for row in rows:
        del row[column_index]

    # Open the CSV file in write mode and create a csv.writer object
    with open(dest_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the modified rows to the CSV file
        for row in rows:
            csv_writer.writerow(row)

def add_column_to_csv(source_file_path, dest_file_path, column_index, list, title):
    # Open the CSV file and create a csv.reader object
    with open(source_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Create a list of rows
        rows = []
        for row in csv_reader:
            rows.append(row)

    # Insert new column data to each row
    rows[0].insert(column_index, title)
    for (row, value) in zip(rows[1:], list):
        row.insert(column_index, value)

    # Open the CSV file in write mode and create a csv.writer object
    with open(dest_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the modified rows to the CSV file
        for row in rows:
            csv_writer.writerow(row)

def del_rows_from_csv(source_file_path, dest_file_path, rows_index_list):
    # Open the CSV file and create a csv.reader object
    with open(source_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Create a list of rows
        rows = []
        for row in csv_reader:
            rows.append(row)

    # Remove the row you want to delete
    offset = 0
    for index in rows_index_list:
        del rows[index-offset]
        offset+=1

    # Open the CSV file in write mode and create a csv.writer object
    with open(dest_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the modified rows to the CSV file
        for row in rows:
            csv_writer.writerow(row)

def get_dataset_characteristcs(path):
    log_path = path + '/logs/processed.csv'

    data = Read(log_path, False, False)

    robot_speeds = data.get_speed()
    timestamps = data.get_timestamps()

    avg_robot_vtrans = 0
    avg_robot_vrot = 0
    for robot_speed in robot_speeds:
        robot_vx, robot_vy, robot_vw = robot_speed
        avg_robot_vtrans += np.sqrt(robot_vx**2 + robot_vy**2)
        avg_robot_vrot += np.abs(robot_vw)

    avg_robot_vtrans = avg_robot_vtrans/len(robot_speeds)
    avg_robot_vrot = avg_robot_vrot/len(robot_speeds)
    time_duration = timestamps[-1] - timestamps[0]
    print(time_duration, avg_robot_vtrans, avg_robot_vrot)
        

def process_data(path, field, embedded_vision, debug = False):
    SMALL_VALUE = 0.001

    log_path = path + '/logs/raw.csv'

    data = Read(log_path, True, True)

    robot_speeds = data.get_speed()
    robot_positions = data.get_position()
    goal_detections = data.get_has_goals()
    frames = data.get_frames()

    goal_in_fov = []
    navigation_not_started = []
    navigation_has_finished = []

    for (frame_nr, robot_position, robot_speed, goal_detection) in zip(frames, robot_positions, robot_speeds, goal_detections):
        robot_x, robot_y, robot_w = robot_position
        robot_vx, robot_vy, robot_vw = robot_speed

        goal_in_fov.append(embedded_vision.is_positive_goal_in_fov(robot_x,
                                                                   robot_y,
                                                                   robot_w,
                                                                   field))
        
        if abs(robot_vx)<SMALL_VALUE and abs(robot_vy)<SMALL_VALUE and abs(robot_vw)<SMALL_VALUE and frame_nr<0.3*len(frames):
            navigation_not_started = list(range(1, frame_nr+1))

        if abs(robot_vx)<SMALL_VALUE and abs(robot_vy)<SMALL_VALUE and abs(robot_vw)<SMALL_VALUE and frame_nr>0.5*len(frames):
            first_navigation_has_finished = frame_nr-navigation_not_started[-1]
            navigation_has_finished = list(range(first_navigation_has_finished, len(frames)-navigation_not_started[-1]+1))

        print(f"frame_nr: {frame_nr} | has goal: {goal_in_fov[-1]} | detected goal: {goal_detection}")

        # DEBUG SCREEN
        if debug:
            WINDOW_NAME = "DEBUG SCREEN"
            img_path = path + f'/cam/frames/{frame_nr}.jpg'
            img = cv2.imread(img_path)
            cv2.imshow(WINDOW_NAME, img)
            if goal_in_fov[-1] or goal_detection:
                key = cv2.waitKey(-1) & 0xFF
                if key == ord('q'):
                    break

    add_column_to_csv(source_file_path = path + '/logs/raw.csv',
                      dest_file_path = path + '/logs/processed.csv',
                      column_index = 11, 
                      list = goal_in_fov, 
                      title = 'GOAL IN FOV')
    
    del_rows_from_csv(source_file_path = path + '/logs/processed.csv',
                      dest_file_path = path + '/logs/processed.csv',
                      rows_index_list = navigation_not_started)
    
    del_rows_from_csv(source_file_path = path + '/logs/processed.csv',
                    dest_file_path = path + '/logs/processed.csv',
                    rows_index_list = navigation_has_finished)

