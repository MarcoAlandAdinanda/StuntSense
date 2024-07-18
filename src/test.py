import customtkinter as ctk
import tkinter as tk  # Import the standard tkinter module

class DarkModeApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Set the appearance mode to "dark"
        ctk.set_appearance_mode("dark")

        # Set the title and geometry of the main window
        self.title("CustomTkinter Dark Mode Example")
        self.geometry("400x300")

        # Load the PNG icon using tkinter's PhotoImage
        self.icon_image = tk.PhotoImage(file="src/logo.png")
        self.iconphoto(False, self.icon_image)  # Set the window icon

        # Add a sample label
        self.label = ctk.CTkLabel(self, text="Hello, Dark Mode!")
        self.label.pack(pady=20)

        # Add a button to demonstrate interaction
        self.button = ctk.CTkButton(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=20)

    def on_button_click(self):
        self.label.configure(text="Button Clicked!")

if __name__ == "__main__":
    app = DarkModeApp()
    app.mainloop()
