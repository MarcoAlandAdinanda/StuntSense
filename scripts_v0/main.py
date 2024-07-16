import cv2
import os
import string
import csv
import tkinter as tk
import serial_communication as com
import categorize as cat
from tkinter import ttk
from PIL import Image, ImageTk
from utils import *
from detector import Detector
from math import dist

class StuntSenseApp(tk.Tk):
    def __init__(self):
        """
            Initialize App frame, widgets, webacam, and model
        """
        # Init App
        super().__init__()

        self.file_counter = 34
        self.resources_path = "../resources/" # PATH MASIH SERING TROUBLE, GUNAKAN FULL PATH
        self.file_name = "foto"+str(self.file_counter)+".png"

        self.title('Stuntsense GUI')
        
        ## Main frame ##
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ## Left frame for video feed and scale button ##
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Display webcam
        self.image_label = ttk.Label(self.left_frame)
        self.image_label.pack(pady=5)
        
        # Scale button
        self.scale_crop = tk.Scale(self.left_frame, orient=tk.HORIZONTAL, label='Crop image')
        self.scale_crop.set(0)
        self.scale_crop.pack(pady=0)

        ## Right frame for input, buttons, and ouptuts ##
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Input mode
        self.mode_input = ttk.Entry(self.right_frame)
        self.mode_input.insert(0, "Input Mode")
        self.mode_input.pack(pady=5)

        # Input name
        self.name_input = ttk.Entry(self.right_frame)
        self.name_input.insert(0, "Input Name")
        self.name_input.pack(pady=5)

        # Input gender
        self.gender_input = ttk.Entry(self.right_frame)
        self.gender_input.insert(0, "Input Gender")
        self.gender_input.pack(pady=5)

        # Input age
        self.age_input = ttk.Entry(self.right_frame)
        self.age_input.insert(0, "Input Age")
        self.age_input.pack(pady=5)

        # Take pic
        self.capture_button = ttk.Button(self.right_frame, text='Take Picture', command=self.take_picture)
        self.capture_button.pack(pady=5)

        # Start process
        self.start_button = ttk.Button(self.right_frame, text='Start Process', command=self.start_process)
        self.start_button.pack(pady=5)

        # Terminal output
        self.output_text = tk.Text(self.right_frame, state='disabled', height=10)
        self.output_text.pack(pady=5)

        # Result output
        self.result_label = ttk.Label(self.right_frame)
        self.result_label.pack()

        # Update webcam #
        self.capture = cv2.VideoCapture(0)  # Use 0 for the default camera
        self.update_frame()

        ## Define Model ##
        self.model = Detector()

    def update_frame(self):
        """
            To update frame and display scale-based cropping. 
        """
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Input image shape
            height, width, _ = frame.shape
            
            # scale-based cropping
            crop_value = self.scale_crop.get()
            if crop_value != 0:
                draw_scale(frame, crop_value, height, width)

            # send image to tkinter frame
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)
        self.after(30, self.update_frame)

    def take_picture(self):
        """
            To take image from webcam frame and display the keypoints & bbox
        """
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            while os.path.isfile(self.resources_path + self.file_name):
                self.file_counter += 1
                self.file_name = "foto"+str(self.file_counter)+".png"
            
            # scale-based cropping
            crop_value = self.scale_crop.get()
            
            # model predict the image after cropping
            self.keypoints, self.bbox = self.model.predict(frame, crop_value, height, width)
                
            # save the model output img 
            cv2.imwrite(os.path.join(self.resources_path, self.file_name), frame)
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, 'Picture taken and saved to folder resources!\n')
            
            # display image in tkinter frame
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.result_label.imgtk = imgtk
            self.result_label.configure(image=imgtk)

            # Read Sensor
            # stuntsense_com = com.SerialCommunication('/dev/ttyACM0')
            # serial_msg = stuntsense_com.read_serial()
            # self.cam_dist = int(serial_msg[0].strip())
            # self.cam_roll = float(serial_msg[1].strip())
            # self.cam_pitch = float(serial_msg[2].strip())

            # display sensor outputs
            self.output_text.insert(tk.END, str("Distance: "))
            self.output_text.insert(tk.END, str(self.cam_dist) + "\n")
            self.output_text.insert(tk.END, str("Roll Angle: "))
            self.output_text.insert(tk.END, str(self.cam_roll) + "\n")
            self.output_text.insert(tk.END, str("Pitch Angle: "))
            self.output_text.insert(tk.END, str(self.cam_pitch) + "\n")
            self.output_text.config(state='disabled')

    def start_process(self):
        """
            By using the model output from 'take_pic' to categorize the stunting level.
        """
        try:
            self.output_text.config(state='normal')

            self.cam_dist = 228
            self.cam_roll = -72.2
            self.cam_pitch = -4.0

            # Get Input Data
            mode = string.capwords(self.mode_input.get())
            name = string.capwords(self.name_input.get())
            gender = string.capwords(self.gender_input.get())
            age = int(self.age_input.get())

            # use saved pic
            frame = cv2.imread(self.resources_path + self.file_name)

            # Height measurments
            neck_coordinate = midpoint(self.keypoints[5].tolist(), self.keypoints[6].tolist())
            head_dist = dist(neck_coordinate, (self.keypoints[0][0].item(), self.bbox[1]))
            head_pixel = head_dist * 0.8 # estimation rasio

            right_base_pixel = dist(self.keypoints[12].tolist(), self.keypoints[6].tolist())
            left_base_pixel = dist(self.keypoints[11].tolist(), self.keypoints[5].tolist())
            base_pixel = (right_base_pixel + left_base_pixel) / 2
            
            right_leg_pixel = dist(self.keypoints[16].tolist(), self.keypoints[14].tolist()) + dist(self.keypoints[14].tolist(), self.keypoints[12].tolist)
            left_leg_pixel = dist(self.keypoints[15].tolist(), self.keypoints[13].tolist()) + dist(self.keypoints[13].tolist(), self.keypoints[11].tolist)
            leg_pixel = (right_leg_pixel + left_leg_pixel) / 2

            height_pixel = leg_pixel + base_pixel + head_pixel
            height_cm = (height_pixel / frame.shape[0]) * convert_to_cm(self.cam_dist)
            
            # Classification
            stuntsense_cat = cat.Categorize(mode, age, gender, height_cm)
            th_list = stuntsense_cat.get_th()
            status = stuntsense_cat.get_status(th_list)

            # Print the Results
            self.output_text.insert(tk.END, str("PXL: "))
            self.output_text.insert(tk.END, str(height_pixel) + "\n")
            self.output_text.insert(tk.END, str("CM: "))
            self.output_text.insert(tk.END, str(height_cm) + "\n")
            self.output_text.insert(tk.END, str("SD Value: "))
            self.output_text.insert(tk.END, str(th_list) + "\n")
            self.output_text.insert(tk.END, str("Stunting Status: "))
            self.output_text.insert(tk.END, str(status) + "\n")

            # Print to CSV
            csv_file = '/home/rafael/stuntsense_ws/results/data_log.csv'
            header = ['Name', 'File name', 'Distance', 'Roll Angle', 'Pitch Angle', 'Height_Pixel', 'Height_CM', 'Status']

            try:
                with open(csv_file, mode='r') as file:
                    pass
            except FileNotFoundError:
                with open(csv_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)

            file_name = self.resources_path + self.file_name
            data = [name, file_name, self.cam_dist, self.cam_roll, self.cam_pitch, height_pixel, height_cm, status]

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)

            self.output_text.insert(tk.END, str("Data stored to CSV file successfully.\n"))
            self.output_text.insert(tk.END, str("--------------------------------------------------------------------\n"))
            self.output_text.config(state='disabled')
            
            # Output the Result Image
            height, width, _ = frame.shape
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.result_label.imgtk = imgtk
            self.result_label.configure(image=imgtk)
        
        except Exception as e:
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, f'Error! Check the input then retry! {str(e)}\n')
            self.output_text.config(state='disabled')
            pass

if __name__ == '__main__':
    gui = StuntSenseApp()
    gui.mainloop()
