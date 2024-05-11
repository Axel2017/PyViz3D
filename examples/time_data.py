import numpy as np
import pyviz3d.visualizer as viz
import json
import sys
from datetime import datetime, timedelta
import math


def read_time_data(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    first_timestamp = data["Entries"][0]["Timestamp"]
    first_time = datetime.strptime(first_timestamp, "%Y-%m-%d %H:%M:%S:%f")
    time_step = 0
    time_position_array = []
    time_color_array = []
    time_normals_array = []
    steps = 0
    # Iterate through the entries
    for entry in data["Entries"]:
        steps += 1
        
        timestamp = entry["Timestamp"]
        position_rotation = entry["Position_rotation"]

        # Calculate the time difference from the first timestamp
        current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S:%f")
        time_diff = current_time - first_time

        # Calculate milliseconds
        milliseconds = time_diff.seconds * 1000 + time_diff.microseconds // 1000

        formatted_time = str(timedelta(seconds=time_diff.seconds, milliseconds=milliseconds))
        position_array = np.empty((0, 3), dtype=np.float32) 
        # Iterate through the anchors
        points_len = 0
        for anchor_name, anchor_data in position_rotation.items():
            if 'PositionX' in anchor_data and 'PositionY' in anchor_data and 'PositionZ' in anchor_data:
                points_len += 1
                x = anchor_data["PositionX"]
                y = anchor_data["PositionY"]
                z = anchor_data["PositionZ"]

                point = np.array([x, y, z], dtype=np.float32)  # Create a point array
                position_array = np.append(position_array, [point], axis=0)  # Append the point to the array
        if position_array.size != 0:
            time_step += 1
            point_colors = (np.random.random(size=[points_len, 3]) * 255)
            time_color_array.append(point_colors.astype(np.uint8))

            time_normals_array.append(np.ones(position_array.shape, dtype=np.float32))
            
            time_position_array.append(position_array.astype(np.float32))
    return np.array(time_position_array), np.array(time_color_array), np.array(time_normals_array)


def read_line_time_data(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    first_timestamp = data["Entries"][0]["Timestamp"]
    first_time = datetime.strptime(first_timestamp, "%Y-%m-%d %H:%M:%S:%f")
    time_step = 0
    time_position_array = []
    time_color_array = []
    time_normals_array = []
    steps = 0
    # Iterate through the entries
    for entry in data["Entries"]:
        steps += 1
        
        timestamp = entry["Timestamp"]
        position_rotation = entry["Position_rotation"]

        # Calculate the time difference from the first timestamp
        current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S:%f")
        time_diff = current_time - first_time

        # Calculate milliseconds
        milliseconds = time_diff.seconds * 1000 + time_diff.microseconds // 1000

        formatted_time = str(timedelta(seconds=time_diff.seconds, milliseconds=milliseconds))
        position_array = np.empty((0, 3), dtype=np.float32) 
        # Iterate through the anchors
        points_len = 0
        start = position_rotation["FullBody_Start"]
        end = position_rotation["FullBody_SpineLower"]
        position_array = np.append(position_array,
                                   [[start["PositionX"], start["PositionY"], start["PositionZ"]],
                                    [end["PositionX"], end["PositionY"], end["PositionZ"]]],
                                    axis=0)
        points_len += 1
        if position_array.size != 0:
            time_step += 1
            point_colors = (np.random.random(size=[points_len, 3]) * 255)
            time_color_array.append(point_colors.astype(np.uint8))
            time_position_array.append(position_array.astype(np.float32))
    return np.array(time_position_array), np.array(time_color_array)

def main():

    # First, we set up a visualizer
    v = viz.Visualizer()
    file_path = "2024-05-09 13:39:27[BuildingBlock] Hand Tracking right (OVRHand)_hand_data.json"
    time_position_array, time_color_array, time_normals_array = read_time_data(file_path)
    point_size = 20


    v.add_time_points("hand", time_position_array, time_color_array.shape, point_size=point_size,normals=time_normals_array,colors=time_color_array, visible=True)

    file_path = "2024-05-09 13:25:43nd Tracking leftHand Tracking left (OVRHand)_hand_data.json"
    time_position_array, time_color_array, time_normals_array = read_time_data(file_path)
    point_size = 20
    v.add_time_points("lefthand", time_position_array, time_color_array.shape, point_size=point_size,normals=time_normals_array,colors=time_color_array, visible=True)

    # line_position_array, line_color_array = read_line_time_data(file_path)
    # v.add_time_lines("line", line_position_array, line_color_array.shape, point_size=point_size, colors=line_color_array, visible=True)
    
    v.save('time_points')


if __name__ == '__main__':
    main()








