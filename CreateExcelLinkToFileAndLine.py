import tkinter as tk
from tkinter import filedialog, messagebox
import os
from shutil import copy2  # For copying the file
import pyperclip  # Install with `pip install pyperclip`

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*")])
    if filepath:
        file_path_input.delete(0, tk.END)
        file_path_input.insert(0, filepath)

def select_working_dir():
    directory = filedialog.askdirectory()
    if directory:
        working_dir_input.delete(0, tk.END)
        working_dir_input.insert(0, directory)

def create_bat_file():
    filepath = file_path_input.get()
    line_number = line_number_input.get()
    working_dir = working_dir_input.get()

    if not filepath or not line_number or not working_dir:
        messagebox.showwarning("Missing Input", "Please provide file path, line number, and working directory.")
        return

    if not os.path.exists(filepath):
        messagebox.showerror("Invalid File", "The selected file does not exist.")
        return

    if not os.path.isdir(working_dir):
        messagebox.showerror("Invalid Directory", "The selected working directory does not exist.")
        return

    try:
        line_number = int(line_number)
    except ValueError:
        messagebox.showerror("Invalid Input", "Line number must be an integer.")
        return

    # Copy file to the working directory
    file_name = os.path.basename(filepath)
    copied_file_path = os.path.join(working_dir, file_name)
    try:
        copy2(filepath, copied_file_path)
    except PermissionError:
        messagebox.showerror("Permission Error", "The file is being used by another process. Please close the file and try again.")
        return


    # Create the .bat file in the working directory
    file_base_name, _ = os.path.splitext(file_name)
    bat_filename = os.path.join(working_dir, f"{file_base_name}_line{line_number}.bat")
    bat_content = f'@echo off\nstart notepad++ -n{line_number} "{file_name}"'  # Use relative file name

    with open(bat_filename, "w") as bat_file:
        bat_file.write(bat_content)

    # Create a relative hyperlink for Excel
    relative_bat_path = os.path.relpath(bat_filename, working_dir)
    hyperlink_text = f"Open {file_name} at Line {line_number}"
    hyperlink = f'=HYPERLINK("{relative_bat_path}", "{hyperlink_text}")'
    hyperlink_input.delete(0, tk.END)
    hyperlink_input.insert(0, hyperlink)

    # Copy hyperlink to clipboard
    pyperclip.copy(hyperlink)
    messagebox.showinfo("Success", f"Batch file created in working directory:\n{bat_filename}\nHyperlink copied to clipboard.")

# Set up the GUI
root = tk.Tk()
root.title("Excel link to log line generator")
root.geometry("500x450")
root.resizable(False, False)

# File path input
tk.Label(root, text="File Path:").pack(anchor="w", padx=10, pady=5)
file_path_input = tk.Entry(root, width=50)
file_path_input.pack(anchor="w", padx=10)
tk.Button(root, text="Browse", command=browse_file).pack(anchor="w", padx=10, pady=5)

# Working directory input with note
tk.Label(root, text="Working Directory (Should be the folder where the Excel file is):").pack(anchor="w", padx=10, pady=5)
working_dir_input = tk.Entry(root, width=50)
working_dir_input.pack(anchor="w", padx=10)
tk.Button(root, text="Select Directory", command=select_working_dir).pack(anchor="w", padx=10, pady=5)

# Line number input
tk.Label(root, text="Line Number:").pack(anchor="w", padx=10, pady=5)
line_number_input = tk.Entry(root, width=10)
line_number_input.pack(anchor="w", padx=10)

# Generate .bat file button
tk.Button(root, text="Create Batch File", command=create_bat_file).pack(pady=10)

# Hyperlink output
tk.Label(root, text="Generated Hyperlink:").pack(anchor="w", padx=10, pady=5)
hyperlink_input = tk.Entry(root, width=70)
hyperlink_input.pack(anchor="w", padx=10)

# Start the main loop
root.mainloop()
