import numpy as np
import pyviz3d.visualizer as viz
import json
import sys
from datetime import datetime, timedelta
import math
import os

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
def read_time_data(file_path,color=np.array([255, 0, 0])):
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
            # point_colors = (np.random.random(size=[points_len, 3]) * 255)
            point_colors = np.tile(color, (points_len, 1))
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


def read_line_time_data(file_path, lines,color=np.array([255, 0, 0])):
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
            # point_colors = (np.random.random(size=[points_len, 3]) * 255)
            point_colors = np.tile(color, (points_len, 1))
            # point_colors[:] = [255, 0, 0]
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

def find_file(directory, filename_pattern):
    """
    Finds the full path of a file with the given filename pattern
    in the specified directory and its subdirectories.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if filename_pattern in file:
                return os.path.join(root, file)
            
def read_transform(path):
    with open(path, 'r') as file:
        data = json.load(file)
    translation = np.array([data['pos']['x'],- data['pos']['y']-0.6, data['pos']['z']])
    rotation = np.array([data['rot']['x'], data['rot']['w'], data['rot']['z'], data['rot']['y']])
    return translation, rotation

def main():
    #setup
    directory = "axel_room" 
    #hands #points
    right_hand_path = find_file(directory, "righthand.json")
    left_hand_path = find_file(directory, "lefthand.json")
    hand_point_size = 20
    #lines
    hand_lines = [["FullBody_Start", "FullBody_SpineLower"],
                  ["FullBody_SpineLower","FullBody_SpineMiddle"],
                  ["FullBody_SpineMiddle","FullBody_SpineUpper"],
                  ["FullBody_SpineUpper","Hand_Thumb3"],
                  ["Hand_Index1","FullBody_Head"],
                  ["FullBody_Head","Hand_Index3"],
                  ["Hand_Middle1","FullBody_LeftArmUpper"],
                  ["FullBody_LeftArmUpper","Body_LeftArmLower"],
                  ["Body_LeftHandWristTwist","Body_RightShoulder"],
                  ["Body_RightShoulder","Body_RightScapula"],
                  ["Hand_Pinky0","Body_RightArmLower"],
                  ["Body_RightArmLower","FullBody_RightHandWristTwist"],
                  ["FullBody_RightHandWristTwist","Hand_Pinky3"]]
    
    #head
    head_path = find_file(directory, "camera_position.json")
    head_point_size = 40
    
    #body #points
    body_path = find_file(directory, "bodypose.json")
    body_point_size = 20
    #lines
    body_lines = [
    ["0", "1"],
    ["0", "4"],
    ["1", "2"],
    ["2", "3"],
    ["3", "7"],
    ["4", "5"],
    ["5", "6"],
    ["6", "8"],
    ["9", "10"],
    ["11", "12"],
    ["11", "13"],
    ["11", "23"],
    ["12", "14"],
    ["12", "24"],
    ["13", "15"],
    ["14", "16"],
    ["15", "17"],
    ["15", "19"],
    ["15", "21"],
    ["16", "18"],
    ["16", "20"],
    ["16", "22"],
    ["17", "19"],
    ["18", "20"],
    ["23", "24"],
    ["23", "25"],
    ["24", "26"],
    ["25", "27"],
    ["26", "28"],
    ["27", "29"],
    ["27", "31"],
    ["28", "30"],
    ["28", "32"],
    ["29", "31"],
    ["30", "32"],
]
    
    #audio/text
    audio_path = find_file(directory, "audio_text.json")
    # room
    room_path = find_file(directory, "output.obj")
    room_transform_path = find_file(directory, "iPhoneMesh.json")
    # First, we set up a visualizer
    v = viz.Visualizer(up=np.array([0,-1,0]))

    
    
    #points
    #right hand
    if right_hand_path != None:
        color = np.array([255, 0, 0])
        time_position_array, time_color_array, time_normals_array, frequency = read_time_data(right_hand_path,color)
        v.add_time_points("right_hand", time_position_array, time_color_array.shape, point_size=hand_point_size,normals=time_normals_array,colors=time_color_array, visible=True,frequency=frequency)
        # line_position_array, line_color_array ,frequency= read_line_time_data(right_hand_path,hand_lines)
        # v.add_time_lines("right_line", line_position_array, line_color_array.shape, point_size=hand_point_size, colors=line_color_array, visible=True,frequency=frequency)
    
    #left hand
    if left_hand_path != None:
        color = np.array([0, 0, 255])
        time_position_array, time_color_array, time_normals_array, frequency = read_time_data(left_hand_path,color)
        v.add_time_points("left_hand", time_position_array, time_color_array.shape, point_size=hand_point_size,normals=time_normals_array,colors=time_color_array, visible=True,frequency=frequency)
        # line_position_array, line_color_array ,frequency= read_line_time_data(left_hand_path,hand_lines)
        # v.add_time_lines("left_line", line_position_array, line_color_array.shape, point_size=hand_point_size, colors=line_color_array, visible=True,frequency=frequency)

    #head
    if head_path != None:
        color = np.array([0, 255, 0])
        time_position_array, time_color_array, time_normals_array, frequency = read_time_data(head_path,color)
        v.add_time_points("camera", time_position_array, time_color_array.shape, point_size=head_point_size,normals=time_normals_array,colors=time_color_array, visible=True,frequency=frequency)

    #body
    if body_path != None:
        color = np.array([255, 255, 0])
        time_position_array, time_color_array, time_normals_array, frequency = read_time_data(body_path,color)
        v.add_time_points("body", time_position_array, time_color_array.shape, point_size=body_point_size,normals=time_normals_array,colors=time_color_array, visible=True,frequency=frequency)
        line_position_array, line_color_array ,frequency= read_line_time_data(body_path,body_lines)
        v.add_time_lines("body_line", line_position_array, line_color_array.shape, point_size=body_point_size, colors=line_color_array, visible=True,frequency=frequency)
    
    #audio/text
    if audio_path != None:
        with open(audio_path, 'r') as file:
            data = json.load(file)
        filtered_text = [item["text"] for item in data]
        filtered_start_end = [np.array([item["start"], item["end"]]) for item in data]
        colors = [np.array([255.0, 0.0, 0.0])]  # Example colors
        colors *= len(filtered_text)
        pos = [np.array([0, 0, 0])]
        pos *= len(filtered_text)

        v.add_time_labels('Speech',
                    filtered_text,
                    pos,
                    colors,
                    filtered_start_end,
                    visible=True)
   
    
    #room
    if room_path != None and room_transform_path != None:
        room_translate, room_rotation = read_transform(room_transform_path)
        v.add_mesh('Room',
                path=room_path,
                translation=room_translate,
                rotation=room_rotation,
                visible=True)
    
    
    v.save('time_points')


if __name__ == '__main__':
    main()








