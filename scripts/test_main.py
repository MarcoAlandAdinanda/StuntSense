import customtkinter as ctk

# Create the main window
root = ctk.CTk()

# Create a variable to hold the value of the selected radio button
radio_var = ctk.StringVar(value="Option1")

# Create the radio buttons and associate them with the same variable
radio_button1 = ctk.CTkRadioButton(root, text="Option 1", variable=radio_var, value="Option1")
radio_button1.pack(pady=10)

radio_button2 = ctk.CTkRadioButton(root, text="Option 2", variable=radio_var, value="Option2")
radio_button2.pack(pady=10)

radio_button3 = ctk.CTkRadioButton(root, text="Option 3", variable=radio_var, value="Option3")
radio_button3.pack(pady=10)

# Function to print the selected option
def print_selected_option():
    print("Selected option:", radio_var.get())

# Button to print the selected option
print_button = ctk.CTkButton(root, text="Print Selected Option", command=print_selected_option)
print_button.pack(pady=20)

# Run the main loop
root.mainloop()
