import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from main import process_files


class DuplicateFileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate File Sorter")

        style = ttk.Style(theme="darkly")
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=BOTH, expand=True)

        self.input_var = ttk.StringVar()
        self.output_var = ttk.StringVar()

        ttk.Label(frame, text="Input Folder:", bootstyle="warning").pack(anchor=W)
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=X, pady=5)
        ttk.Entry(input_frame, textvariable=self.input_var, width=60).pack(side=LEFT, expand=True, fill=X)
        ttk.Button(input_frame, text="Browse", command=self.browse_input).pack(side=RIGHT)

        ttk.Label(frame, text="Output Folder:", bootstyle="warning").pack(anchor=W, pady=(10, 0))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=X, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_var, width=60).pack(side=LEFT, expand=True, fill=X)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(side=RIGHT)

        ttk.Button(frame, text="Start Sorting", bootstyle="info", command=self.run_sorting).pack(pady=20)

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_var.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_var.set(folder)

    def run_sorting(self):
        input_path = self.input_var.get()
        output_path = self.output_var.get()

        if not os.path.isdir(input_path) or not os.path.isdir(output_path):
            messagebox.showerror("Error", "Please select valid input and output folders.")
            return

        try:
            process_files(input_path, output_path)
            messagebox.showinfo("Success", "Files sorted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = DuplicateFileSorterApp(root)
    root.mainloop()
