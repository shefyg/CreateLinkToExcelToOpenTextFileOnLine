import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pyperclip  # Install with `pip install pyperclip`

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*")])
    if filepath:
        file_path_input.delete(0, tk.END)
        file_path_input.insert(0, filepath)

def create_bat_file():
    filepath = file_path_input.get()
    line_number = line_number_input.get()

    if not filepath or not line_number:
        messagebox.showwarning("Missing Input", "Please provide both file path and line number.")
        return

    if not os.path.exists(filepath):
        messagebox.showerror("Invalid File", "The selected file does not exist.")
        return

    try:
        line_number = int(line_number)
    except ValueError:
        messagebox.showerror("Invalid Input", "Line number must be an integer.")
        return

    # Create the .bat file
    file_name = os.path.basename(filepath)
    file_base_name, _ = os.path.splitext(file_name)
    bat_filename = os.path.join(os.path.dirname(filepath), f"{file_base_name}_line{line_number}.bat")
    bat_content = f'@echo off\nstart notepad++ -n{line_number} "{filepath}"'

    with open(bat_filename, "w") as bat_file:
        bat_file.write(bat_content)

    # Create hyperlink for Excel
    hyperlink_text = f"Open {file_name} at Line {line_number}"
    hyperlink = f'=HYPERLINK("{bat_filename}", "{hyperlink_text}")'
    hyperlink_input.delete(0, tk.END)
    hyperlink_input.insert(0, hyperlink)

    # Copy hyperlink to clipboard
    pyperclip.copy(hyperlink)
    messagebox.showinfo("Success", f"Batch file created:\n{bat_filename}\nHyperlink copied to clipboard.")

# Set up the GUI
root = tk.Tk()
root.title("Batch File Generator")
root.geometry("500x300")
root.resizable(False, False)

# File path input
tk.Label(root, text="File Path:").pack(anchor="w", padx=10, pady=5)
file_path_input = tk.Entry(root, width=50)
file_path_input.pack(anchor="w", padx=10)
tk.Button(root, text="Browse", command=browse_file).pack(anchor="w", padx=10, pady=5)

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
