import tkinter as tk
from tkinter import filedialog
import os

selected_string = ""

def select_html():
    file_path = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select HTML file",
                                           filetypes = (("HTML files", "*.html"),
                                                        ("all files", "*.*")))
    print("Selected HTML file:", file_path)

def select_pdf():
    file_path = filedialog.askopenfilename(initialdir = "/",
                                           title = "Select PDF file",
                                           filetypes = (("PDF files", "*.pdf"),
                                                        ("all files", "*.*")))
    print("Selected PDF file:", file_path)

def start():
    global selected_string
    selected_string = string_entry.get()
    root.destroy()

root = tk.Tk()
root.geometry("300x150")
root.title("File Selector")

html_button = tk.Button(text="Select HTML file", command=select_html)
html_button.pack(pady=10)

pdf_button = tk.Button(text="Select PDF file", command=select_pdf)
pdf_button.pack(pady=10)

string_label = tk.Label(text="Enter string:")
string_label.pack(pady=10)

string_entry = tk.Entry()
string_entry.pack(pady=10)

start_button = tk.Button(text="Start", command=start)
start_button.pack(pady=10)

root.mainloop()

print("Selected string:", selected_string)