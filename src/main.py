import os
import numpy as np
import openpyxl
import tkinter as tk
import customtkinter as ctk
import cv2
import string
import categorize as cat
from math import dist
from PIL import Image, ImageTk
from utils import *
from detector import Detector
import serial_communication as com
from tkinter import filedialog

class StuntSense(ctk.CTk):
    def __init__(self, title, size):
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # icon image
        self.iconpath = ImageTk.PhotoImage(file='logo.png')
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        # always dark mode
        ctk.set_appearance_mode("dark")
    
        # path
        resources = 'resources/'
        results = 'results/'
        
		# webcam
        self.cap = cv2.VideoCapture(0) 

        # widgets
        self.right_side = RightSide(self, self.cap)
        self.left_side = LeftSide(self, resources, results, self.cap, self.right_side.output_image, self.right_side.output_text)

        # run
        self.mainloop()

class LeftSide(ctk.CTkFrame):
    def __init__(self, parent, resources, results, cap, output_image, output_text):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=0.5, relheight=1)
        self.cap = cap
        self.webcam_input = ctk.CTkCanvas(self, bg='#2b2b2b', bd=0, highlightthickness=0)
        self.output_image = output_image
        self.options = Options(self, resources, results, cap, output_image, output_text)
        self.create_widgets()
        self.update_frame()

    def create_widgets(self):
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.webcam_input.grid(row=0, column=0, sticky='nswe', padx=20, pady=20)
        self.options.grid(row=1, column=0, sticky='nswe', padx=20, pady=20)
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            img = img.resize((self.webcam_input.winfo_width(), self.webcam_input.winfo_height()))  # Resize image to match canvas size
            imgtk = ImageTk.PhotoImage(image=img)
            self.webcam_input.create_image(0, 0, anchor='nw', image=imgtk)
            self.webcam_input.imgtk = imgtk
        
        self.webcam_input.after(10, self.update_frame)  # Update frame every 10 ms


class RightSide(ctk.CTkFrame):
    def __init__(self, parent, cap):
        super().__init__(parent)
        self.place(relx=0.5, y=0, relwidth=0.5, relheight=1)
        self.cap = cap
        self.output_text = tk.Text(self, state='disabled', height=10)
        self.output_image = ctk.CTkCanvas(self, bg='#2b2b2b', bd=0, highlightthickness=0)

        self.create_widgets()
        
    def create_widgets(self):
        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure((0, 1), weight=1, uniform='a')
		
        # place widgets with padding
        self.output_image.grid(row=0, column=0, sticky='nswe', padx=20, pady=20)
        self.output_text.grid(row=1, column=0, sticky='nswe', padx=20, pady=20)
        
class Options(ctk.CTkFrame):
    def __init__(self, parent, resources, results, cap, output_image, output_text):
        super().__init__(parent)
        self.place(x=0, rely=0.5, relwidth=0.5, relheight=1)
        self.resutls = results
        self.resources = resources
        self.cap = cap
        self.model = Detector()
        self.output_image = output_image
        self.output_text = output_text

        self.file_counter = 0

		# crop image
        self.crop_image = ctk.CTkSlider(self, orientation='vertical', command=self.update_rectangle)
        self.crop_image.set(0)

		# mode
        vlist = ['Panjang', 'Tinggi']
        self.mode = ctk.CTkComboBox(self, values=vlist)
        self.mode.set('Pilih mode')

		# Name
        self.name = ctk.CTkEntry(self, placeholder_text='Input nama')
        
		# Age
        self.age = ctk.CTkEntry(self, placeholder_text='Input umur')

		# Genders
        self.gender = ctk.StringVar(value='Laki-laki')
        self.toggle_male = ctk.CTkRadioButton(self, text='Laki-laki', variable=self.gender, value='Laki-laki')
        self.toggle_female= ctk.CTkRadioButton(self, text='Perempuan', variable=self.gender, value='Perempuan')

		# Buttons
        self.take_pic = ctk.CTkButton(self, text='Take Picture', command=self.take_picture)
        self.use_pic = ctk.CTkButton(self, text='Use Picture', command=self.select_img)
        self.start_processing = ctk.CTkButton(self, text='Start Processing', command=self.start_process)
        self.create_widgets()
        
    def create_widgets(self):
        # create the grid
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        
		# place widgets with padding
        self.crop_image.grid(row=0, column=0, rowspan=3, sticky='ns', padx=20, pady=20)
        self.mode.grid(row=0, column=1, columnspan=2, sticky='we', padx=20, pady=20)
        self.name.grid(row=1, column=1, columnspan=2, sticky='nswe', padx=20, pady=20)
        self.age.grid(row=2, column=1, columnspan=2, sticky='nswe', padx=20, pady=20)
        self.toggle_male.grid(row=3, column=1, sticky='nswe', padx=20, pady=20)
        self.toggle_female.grid(row=3, column=2, sticky='nswe', padx=20, pady=20)
        self.take_pic.grid(row=0, column=3, rowspan=1, sticky='nswe', padx=20, pady=20)
        self.use_pic.grid(row=1, column=3, sticky='nswe', padx=20, pady=20)
        self.start_processing.grid(row=2, column=3, rowspan=3, sticky='nswe', padx=20, pady=20)
    
    def update_rectangle(self, crop_value):
        crop_value = crop_value * 100
        height, width, _ = self.selected_pic.shape
        
        self.croped_pic = self.selected_pic.copy()
        self.croped_pic_height, crpoed_pic_width, _ = self.croped_pic.shape
        if crop_value != 0:
            draw_scale(self.croped_pic, crop_value, height, width)

        img = Image.fromarray(self.croped_pic)
        img = img.resize((self.output_image.winfo_width(), self.output_image.winfo_height()))
        imgtk = ImageTk.PhotoImage(image=img)
        self.output_image.imgtk = imgtk
        self.output_image.create_image(0, 0, anchor='nw', image=imgtk)
        
    def take_picture(self):
        ret, frame = self.cap.read()
        if ret:
            self.selected_pic = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            n_files = count_files_in_directory(self.resources)
            if n_files > 0 :
                self.filename = f"foto{n_files+1}.png"
            else:
                self.filename = 'foto1.png'        

            # save the model output img 
            # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(self.resources, self.filename), cv2.cvtColor(self.selected_pic, cv2.COLOR_BGR2RGB))
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, 'Picture taken and saved to folder resources!\n')
            
            # display image in tkinter frame
            img = Image.fromarray(self.selected_pic)
            img = img.resize((self.output_image.winfo_width(), self.output_image.winfo_height()))
            imgtk = ImageTk.PhotoImage(image=img)
            self.output_image.imgtk = imgtk
            self.output_image.create_image(0, 0, anchor='nw', image=imgtk)

            # Read Sensor
            stuntsense_com = com.SerialCommunication('COM5')
            serial_msg = stuntsense_com.read_serial()
            self.cam_dist = int(serial_msg[0].strip())
            self.cam_roll = float(serial_msg[1].strip())
            self.cam_pitch = float(serial_msg[2].strip())

            # display sensor outputs
            self.output_text.insert(tk.END, str("Distance: "))
            self.output_text.insert(tk.END, str(self.cam_dist) + "\n")
            self.output_text.insert(tk.END, str("Roll Angle: "))
            self.output_text.insert(tk.END, str(self.cam_roll) + "\n")
            self.output_text.insert(tk.END, str("Pitch Angle: "))
            self.output_text.insert(tk.END, str(self.cam_pitch) + "\n")
            self.output_text.config(state='disabled')

    def select_img(self):
        used_pic_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if used_pic_path:
            used_pic = Image.open(used_pic_path)
            self.selected_pic = np.array(used_pic)
            
            used_pic = used_pic.resize((self.output_image.winfo_width(), self.output_image.winfo_height()))
            imgtk = ImageTk.PhotoImage(used_pic)
            self.output_image.imgtk = imgtk
            self.output_image.create_image(0, 0, anchor='nw', image=imgtk)


    def start_process(self):
        """
            By using the model output from 'take_pic' to categorize the stunting level.
        """
        # try:
        self.output_text.config(state='normal')

        # self.cam_dist = 228
        # self.cam_roll = -72.2
        # self.cam_pitch = -4.0

        # Get Input Data
        mode = string.capwords(self.mode.get())
        name = string.capwords(self.name.get())
        gender = string.capwords(self.gender.get())
        age = int(self.age.get())
        
        crop_value = self.crop_image.get() * 100
        height, width, _ = self.selected_pic.shape
        
        # predict
        try:
            self.keypoints, self.bbox = self.model.predict(self.selected_pic, crop_value, height, width)
        except:
            self.output_text.insert(tk.END, str("Tidak ada yang terdeteksi, silahkan coba kembali"))
            pass
        # print(self.bbox)
        # cv2.rectangle(self.selected_pic, self.bbox[:2], self.bbox[2:], color=(255, 0, 0))

        # Height measurments
        neck_coordinate = midpoint(self.keypoints[5].tolist(), self.keypoints[6].tolist())
        head_dist = dist(neck_coordinate, (self.keypoints[0][0].item(), self.bbox[1]))
        head_pixel = head_dist * 0.8 # estimation rasio

        right_base_pixel = dist(self.keypoints[12].tolist(), self.keypoints[6].tolist())
        left_base_pixel = dist(self.keypoints[11].tolist(), self.keypoints[5].tolist())
        base_pixel = (right_base_pixel + left_base_pixel) / 2
        
        right_leg_pixel = dist(self.keypoints[16].tolist(), self.keypoints[14].tolist()) + dist(self.keypoints[14].tolist(), self.keypoints[12].tolist())
        left_leg_pixel = dist(self.keypoints[15].tolist(), self.keypoints[13].tolist()) + dist(self.keypoints[13].tolist(), self.keypoints[11].tolist())
        leg_pixel = (right_leg_pixel + left_leg_pixel) / 2

        height_pixel = leg_pixel + base_pixel + head_pixel
        height_cm = (height_pixel / self.selected_pic.shape[0]) * convert_to_cm(self.cam_dist)
        
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
    # csv_file = '/home/rafael/stuntsense_ws/results/data_log.csv'
    # header = ['Name', 'File name', 'Distance', 'Roll Angle', 'Pitch Angle', 'Height_Pixel', 'Height_CM', 'Status']

    # try:
    #     with open(csv_file, mode='r') as file:
    #         pass
    # except FileNotFoundError:
    #     with open(csv_file, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(header)

    # file_name = self.resources_path + self.file_name
    # data = [name, file_name, self.cam_dist, self.cam_roll, self.cam_pitch, height_pixel, height_cm, status]

    # with open(csv_file, mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(data)

    # self.output_text.insert(tk.END, str("Data stored to CSV file successfully.\n"))
    # self.output_text.insert(tk.END, str("--------------------------------------------------------------------\n"))
    # self.output_text.config(state='disabled')
    
        xlsx_file = 'C:/Users/ADMIN/OneDrive/Documents/PKM/Data Pusat StuntSense.xlsx'
        header = ['Name', 'File name', 'Distance', 'Roll Angle', 'Pitch Angle', 'Height_Pixel', 'Height_CM', 'Status']

        # Check if the file exists
        if not os.path.exists(xlsx_file):
            # Create a new workbook and add the header
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(header)
            workbook.save(xlsx_file)

        # Load the existing workbook
        workbook = openpyxl.load_workbook(xlsx_file)
        sheet = workbook.active

        # Define the data to append
        data = [name, self.filename, self.cam_dist, self.cam_roll, self.cam_pitch, height_pixel, height_cm, status]

        # Append the data
        sheet.append(data)
        workbook.save(xlsx_file)

        self.output_text.insert(tk.END, str("Data stored to XLSX file successfully.\n"))
        self.output_text.insert(tk.END, str("--------------------------------------------------------------------\n"))
        self.output_text.config(state='disabled')

        # Output the Result Image
        # height, width, _ = self.frame.shape
        # img = Image.fromarray(self.frame)
        # imgtk = ImageTk.PhotoImage(image=img)
        # # self.result_label.imgtk = imgtk
        # self.result_label.configure(image=imgtk)
        
        # except Exception as e:
        #     self.output_text.config(state='normal')
        #     self.output_text.insert(tk.END, f'Error! Check the input then retry! {str(e)}\n')
        #     self.output_text.config(state='disabled')

if __name__ == "__main__":
    app = StuntSense("StuntSense", (1280, 720))