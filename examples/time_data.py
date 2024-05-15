import numpy as np
import pyviz3d.visualizer as viz
import json
import sys
from datetime import datetime, timedelta
import math


# def read_time_data(file_path):
#     # Load the JSON data from the file
#     with open(file_path, 'r') as file:
#         data = json.load(file)

#     first_timestamp = data["Entries"][0]["Timestamp"]
#     first_time = datetime.strptime(first_timestamp, "%Y-%m-%d %H:%M:%S:%f")
#     time_step = 0
#     time_position_array = []
#     time_color_array = []
#     time_normals_array = []
#     steps = 0
#     # Iterate through the entries
#     for entry in data["Entries"]:
#         steps += 1
        
#         timestamp = entry["Timestamp"]
#         position_rotation = entry["Position_rotation"]

#         # Calculate the time difference from the first timestamp
#         current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S:%f")
#         time_diff = current_time - first_time

#         # Calculate milliseconds
#         milliseconds = time_diff.seconds * 1000 + time_diff.microseconds // 1000

#         formatted_time = str(timedelta(seconds=time_diff.seconds, milliseconds=milliseconds))
#         position_array = np.empty((0, 3), dtype=np.float32) 
#         # Iterate through the anchors
#         points_len = 0
#         for anchor_name, anchor_data in position_rotation.items():
#             if 'PositionX' in anchor_data and 'PositionY' in anchor_data and 'PositionZ' in anchor_data:
#                 points_len += 1
#                 x = anchor_data["PositionX"]
#                 y = anchor_data["PositionY"]
#                 z = anchor_data["PositionZ"]

#                 point = np.array([x, y, z], dtype=np.float32)  # Create a point array
#                 position_array = np.append(position_array, [point], axis=0)  # Append the point to the array
#         if position_array.size != 0:
#             time_step += 1
#             point_colors = (np.random.random(size=[points_len, 3]) * 255)
#             time_color_array.append(point_colors.astype(np.uint8))

#             time_normals_array.append(np.ones(position_array.shape, dtype=np.float32))
            
#             time_position_array.append(position_array.astype(np.float32))
#     return np.array(time_position_array), np.array(time_color_array), np.array(time_normals_array)
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
    time_diffs = []  # List to store time differences

    # Iterate through the entries
    for i, entry in enumerate(data["Entries"]):
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
            
        if i > 0:  # Calculate time difference from second entry onwards
            prev_timestamp = data["Entries"][i-1]["Timestamp"]
            prev_time = datetime.strptime(prev_timestamp, "%Y-%m-%d %H:%M:%S:%f")
            time_diff = current_time - prev_time
            time_diffs.append(time_diff.total_seconds())  # Append time difference in seconds

    # Calculate frequency of updates
    if time_diffs:
        mean_frequency = 1 / np.mean(time_diffs)  # Mean frequency in Hz
    else:
        mean_frequency = 0  # No updates

    return np.array(time_position_array), np.array(time_color_array), np.array(time_normals_array), np.round(mean_frequency)


def read_line_time_data(file_path, lines):
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
    time_diffs = []  # List to store time differences

    # Iterate through the entries
    for i, entry in enumerate(data["Entries"]):
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

        time_lines = []
        for line in lines:
            start = position_rotation[line[0]]
            end = position_rotation[line[1]]
            time_lines.append([start["PositionX"], start["PositionY"], start["PositionZ"]])
            time_lines.append([end["PositionX"], end["PositionY"], end["PositionZ"]])
            
            points_len += 1
        position_array = np.array(time_lines)
        if position_array.size != 0:
            time_step += 1
            point_colors = (np.random.random(size=[points_len, 3]) * 255)
            point_colors[:] = [255, 0, 0]
            time_color_array.append(point_colors.astype(np.uint8))
            time_position_array.append(position_array.astype(np.float32))
            
        if i > 0:  # Calculate time difference from second entry onwards
            prev_timestamp = data["Entries"][i-1]["Timestamp"]
            prev_time = datetime.strptime(prev_timestamp, "%Y-%m-%d %H:%M:%S:%f")
            time_diff = current_time - prev_time
            time_diffs.append(time_diff.total_seconds())  # Append time difference in seconds

    # Calculate frequency of updates
    if time_diffs:
        mean_frequency = 1 / np.mean(time_diffs)  # Mean frequency in Hz
    else:
        mean_frequency = 0  # No updates

    return np.array(time_position_array), np.array(time_color_array), np.round(mean_frequency)

def main():

    # First, we set up a visualizer
    v = viz.Visualizer()
    
    file_path = "day_save_on_quit/2024-05-13 16:11:36[BuildingBlock] Hand Tracking right (OVRHand)_hand_data.json"
    time_position_array, time_color_array, time_normals_array, frequency = read_time_data(file_path)
    point_size = 20
    lines = [["FullBody_Start", "FullBody_SpineLower"],["FullBody_SpineLower","FullBody_SpineMiddle"],["FullBody_SpineMiddle","FullBody_SpineUpper"],["FullBody_SpineUpper","Hand_Thumb3"],["Hand_Index1","FullBody_Head"],["FullBody_Head","Hand_Index3"],["Hand_Middle1","FullBody_LeftArmUpper"],["FullBody_LeftArmUpper","Body_LeftArmLower"],["Body_LeftHandWristTwist","Body_RightShoulder"],["Body_RightShoulder","Body_RightScapula"],["Hand_Pinky0","Body_RightArmLower"],["Body_RightArmLower","FullBody_RightHandWristTwist"],["FullBody_RightHandWristTwist","Hand_Pinky3"]]
    print(time_position_array.shape)
    v.add_time_points("right_hand", time_position_array, time_color_array.shape, point_size=point_size,normals=time_normals_array,colors=time_color_array, visible=True,frequency=frequency)
    line_position_array, line_color_array ,frequency= read_line_time_data(file_path,lines)
    v.add_time_lines("right_line", line_position_array, line_color_array.shape, point_size=point_size, colors=line_color_array, visible=True,frequency=frequency)
   

    file_path = "day_save_on_quit/2024-05-13 16:11:36nd Tracking leftHand Tracking left (OVRHand)_hand_data.json"
    time_position_array, time_color_array, time_normals_array, frequency = read_time_data(file_path)
    point_size = 20
    print(time_position_array.shape)
    v.add_time_points("left_hand", time_position_array, time_color_array.shape, point_size=point_size,normals=time_normals_array,colors=time_color_array, visible=True,frequency=frequency)
    line_position_array, line_color_array ,frequency= read_line_time_data(file_path,lines)
    v.add_time_lines("left_line", line_position_array, line_color_array.shape, point_size=point_size, colors=line_color_array, visible=True,frequency=frequency)


    [{'text': ['this', 'drawer', 'opens', 'up', 'to', 'a', 'safe'], 'start': 12.539, 'end': 14.841}, {'text': ['when', 'the', 'button', 'is', 'pushed,', 'the', 'TV', 'is', 'turned', 'on'], 'start': 52.361, 'end': 55.606}]
    v.add_time_labels('Labels',
                 ['this drawer opens up to a safe' ,'when the button is pushed,the TV is turned on '],
                 [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])],
                 [np.array([255.0, 0.0, 0.0]), np.array([0.0, 255.0, 0.0])],
                 [np.array([0.539, 14.841]), np.array([20.361, 23.606])],
                 visible=True)
    
    v.save('time_points')


if __name__ == '__main__':
    main()








