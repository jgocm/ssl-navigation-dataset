from src.Reader.Reader import Read
import cv2
import csv

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

def process_data(path, field, embedded_vision, debug = False):

    log_path = path + '/embedded/logs/raw.csv'
    data = Read(log_path, True, True)

    robot_positions = data.get_position()
    goal_detections = data.get_has_goals()
    frames = data.get_frames()

    goal_in_fov = []
    navigation_not_started = []

    for (frame_nr, robot_position, goal_detection) in zip(frames, robot_positions, goal_detections):
        robot_x, robot_y, robot_w = robot_position

        goal_in_fov.append(embedded_vision.is_positive_goal_in_fov(robot_x,
                                                                   robot_y,
                                                                   robot_w,
                                                                   field))
        
        if robot_x==0 and robot_y==0 and robot_w==0:
            navigation_not_started.append(frame_nr)

        print(f"frame_nr: {frame_nr} | has goal: {goal_in_fov[-1]} | detected goal: {goal_detection}")

        # DEBUG SCREEN
        if debug:
            WINDOW_NAME = "DEBUG SCREEN"
            img_path = path + f'/embedded/cam/frames/{frame_nr}.jpg'
            img = cv2.imread(img_path)
            cv2.imshow(WINDOW_NAME, img)
            if goal_in_fov[-1] or goal_detection:
                key = cv2.waitKey(-1) & 0xFF
                if key == ord('q'):
                    break
        
    add_column_to_csv(source_file_path = path + '/embedded/logs/raw.csv',
                      dest_file_path = path + '/embedded/logs/processed.csv',
                      column_index = 11, 
                      list = goal_in_fov, 
                      title = 'GOAL IN FOV')
    
    del_rows_from_csv(source_file_path = path + '/embedded/logs/processed.csv',
                      dest_file_path = path + '/embedded/logs/processed.csv',
                      rows_index_list = navigation_not_started)
