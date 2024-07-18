import os
import cv2

def pixel_per_metric(cam_dist): # nonsense results
    ppm = ((0.0944*(cam_dist**2)) - (5.5989*cam_dist) + 105.16)
    return ppm

def convert_to_cm(cam_dist):
    cm = ((0.0003*(cam_dist**2)) + (0.7504*cam_dist) + 0.2809)
    return cm

def draw_scale(frame, crop_value, height, width, color=(255, 0, 0)):
    mid_x = width / 2
    croped_value_rasio = mid_x * (crop_value / 100) 
    start_x = int(mid_x - croped_value_rasio)
    end_x = int(mid_x + croped_value_rasio)

    # Scale range points
    start_point = (start_x, 0)
    end_point = (end_x, height)

    # Display 
    cv2.rectangle(frame, start_point, end_point, color=color)
    # return frame

def midpoint(point1, point2):
        # Checking null values
        if point1.count(0) > 1:
            return point2
        if point2.count(0) > 1:
            return point1
        
        # Calculate the midpoint
        x_1, y_1 = point1[0], point1[1]
        x_2, y_2 = point2[0], point2[1]
        mid_x = (x_1 + x_2) / 2
        mid_y = (y_1 + y_2) / 2
        return [int(mid_x), int(mid_y)]

def count_files_in_directory(directory):
    try:
        # Get the list of all files and directories in the specified directory
        files_and_dirs = os.listdir(directory)
        
        # Filter out only the files
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory, f))]
        
        # Return the count of files
        return len(files)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0