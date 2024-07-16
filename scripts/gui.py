import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

class StuntSense:
    def __init__(self, root):
        self.root = root
        self.root.geometry('860x680')
        self.root.titlee('StuntSense')
        self.resized_tk = None

        # configure the grid layout
        self.root.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.root.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # load images
        self.image_original = 