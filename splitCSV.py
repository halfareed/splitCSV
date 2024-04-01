import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter.filedialog import askopenfilename
from pandas.core.groupby.groupby import DataError
import re


class App(tk.Tk):  # the App class inherits from Tk
    def __init__(self, title, text):
        # main setup
        super().__init__()
        self.title(title)
        self.text = text
        # self.geometry('400x150')
        # self.wm_attributes('-topmost', True)
        self.update_idletasks()  # Add this line
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width + 200, height - 50, x, y))

        # widgets
        self.menu = Menu(self, self.text)

        # run
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.index_toggle = None
        self.header_toggle = None
        self.col_num = None
        self.rows_num = None
        self.filename = None
        self.b2 = None
        self.b1 = None
        self.entry = None
        self.place(x=50, y=0, relwidth=2, relheight=2)
        self.create_widgets(text)

    def create_widgets(self, text):
        label = ttk.Label(self, text=text)
        label.grid(row=0, column=1, pady=(10, 10), columnspan=2, sticky='w', padx=10)
        self.entry = ttk.Entry(self, width=40)
        self.b1 = ttk.Button(self, text='Split', width=10, command=self.submit_row_num, state="disabled")
        self.b2 = ttk.Button(self, text='Choose a csv file', width=20, command=self.choose_file)
        toggle_frame = ttk.Frame(self)
        self.index_toggle = ttk.Checkbutton(toggle_frame, text='keep index')
        self.header_toggle = ttk.Checkbutton(toggle_frame, text='keep header')
        self.index_toggle.state(['selected'])
        self.header_toggle.state(['selected'])
        self.b1.grid(row=3, column=1, pady=10)
        self.b2.grid(row=3, column=2, pady=10)
        self.entry.grid(row=1, column=0, columnspan=3, padx=10)
        toggle_frame.grid(row=6, column=0, columnspan=3, sticky='nsew')
        self.index_toggle.grid(row=6, column=1, padx=20)
        self.header_toggle.grid(row=6, column=2, padx=15)

    def submit_row_num(self):
        header_status = self.header_toggle.instate(['selected'])
        index_status = self.index_toggle.instate(['selected'])
        print(type(header_status),index_status)
        copies = 0
        try:
            copies = int(self.entry.get())
            if copies <= 1:
                print('Please enter a number larger than 1. Try again. ')
                return
            elif copies > 50:
                print('The number you entered is too large, Try again.')
                return
            # elif (self.rows_num / copies
            with pd.read_csv(self.filename, chunksize=self.rows_num / copies) as reader:
                for i, chunk in enumerate(reader):
                    chunk.to_csv(f'{self.filename.split(".")[0]}_{i + 1}.csv', index= index_status, header=header_status)
            self.b1.config(state="disabled")
        except (TypeError, ValueError):
            print('Please enter a valid (integer) number')


    def choose_file(self):
        try:
            self.filename = askopenfilename()
            filedim = ttk.Label(self)
            filedim.grid(row=6, column=1, pady=25, columnspan=2, sticky='w', padx=70)
            if self.filename:
                if self.filename.split('.')[1] == "csv":
                    self.rows_num, self.col_num = (pd.read_csv(self.filename).shape[0]), (pd.read_csv(self.filename).shape[1])
                    filedim.config(text=f' {self.rows_num} rows {self.col_num} columns')
                    self.b1.config(state="enable")
                else:
                    self.b1.config(state="disable")
        except(DataError, AttributeError, pd.errors.EmptyDataError, FileNotFoundError):
            print('Please select a valid file')
            return

a = App('Split CSV dataset', 'How many files are you splitting this dataset into?')
