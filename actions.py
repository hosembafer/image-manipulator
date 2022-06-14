import tkinter as tk
from tkinter import BOTH, LEFT, RIGHT, ttk

class Actions:
    def __init__(self, widget, open_file_chooser, handle_start, handle_stop):
        self.actions_frame = tk.Frame(widget)

        self.add_files_button = ttk.Button(
            master=self.actions_frame,
            text="Add files",
            command=open_file_chooser,
        ).pack(side=LEFT)
        self.start_button = ttk.Button(
            master=self.actions_frame,
            text="Start",
            command=handle_start,
        ).pack(side=LEFT)
        self.stop_button = ttk.Button(
            master=self.actions_frame,
            text="Stop",
            command=handle_stop,
        ).pack(side=LEFT)
        self.clear_list_button = ttk.Button(
            master=self.actions_frame,
            text="Clear list",
            command=self.handle_clear_list,
        ).pack(side=RIGHT)

        self.actions_frame.pack(fill=BOTH)
    
    def handle_clear_list(self):
        self.trigger_clear_list()

    def on_clear_list(self, cb):
        self.trigger_clear_list = cb