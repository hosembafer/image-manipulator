import tkinter as tk
from tkinter import ACTIVE, BOTH, BOTTOM, DISABLED, LEFT, NSEW, RIGHT, SW, ttk
from tkinter.colorchooser import askcolor

from src.image_processor import IPConfig

class Controls:
    def __init__(self, widget):
        controls_frame = tk.Frame(widget)

        tk.Label(controls_frame, 
                text="Action").grid(row=0, sticky=SW)
        tk.Label(controls_frame, 
                text="Width").grid(row=1, sticky=SW)
        tk.Label(controls_frame,
                text="Height").grid(row=2, sticky=SW)

        tk.Label(controls_frame,
                text="Quality").grid(row=0, column=2, sticky=SW)
        tk.Label(controls_frame,
                text="Border").grid(row=1, column=2, sticky=SW)
        tk.Label(controls_frame,
                text="Invert").grid(row=2, column=2, sticky=SW)

        tk.Label(controls_frame,
                text="Flip (vertical)").grid(row=0, column=4, sticky=SW)
        tk.Label(controls_frame,
                text="Flip (horizontal)").grid(row=1, column=4, sticky=SW)
        tk.Label(controls_frame,
                text="Grayscale").grid(row=2, column=4, sticky=SW)

        self.width_var = tk.IntVar()
        self.width_var.set(1000)
        self.width_entry = ttk.Entry(controls_frame, width=8, textvariable=self.width_var, state=DISABLED)

        self.height_var = tk.IntVar()
        self.height_var.set(1000)
        self.height_entry = ttk.Entry(controls_frame, width=8, textvariable=self.height_var, state=DISABLED)

        self.action_var = tk.StringVar(controls_frame)
        actions = ["None", "Resize", "Crop"]
        self.action_var.set(actions[0]) # default value
        self.action_select_box = tk.OptionMenu(controls_frame, self.action_var, *actions, command=self.handle_action_change)

        self.quality_var = tk.IntVar(controls_frame, value=100)
        quality_entry = ttk.Entry(controls_frame, width=4, textvariable=self.quality_var)

        border_entry_frame = tk.Frame(controls_frame)
        self.border_width_var = tk.StringVar()
        self.border_width_var.set(0)
        self.border_width_entry = tk.Entry(
            master=border_entry_frame,
            width=3,
            textvariable=self.border_width_var,
        )
        self.border_width_entry.pack(side=LEFT)
        self.border_color_var = tk.StringVar()
        self.color_icon = tk.PhotoImage(file='./assets/color-wheel.png', width=24, height=24)
        self.border_color_entry = tk.Button(
            master=border_entry_frame,
            image=self.color_icon,
            command=self.handle_border_color,
        )
        self.border_color_entry.pack(side=RIGHT)

        self.invert_var = tk.BooleanVar(value=False)
        invert_checkbox = tk.Checkbutton(controls_frame, onvalue=True, offvalue=False, variable=self.invert_var, command=self.handle_control_change)

        self.grayscale_var = tk.BooleanVar(value=False)
        grayscale_checkbox = tk.Checkbutton(controls_frame, onvalue=True, offvalue=False, variable=self.grayscale_var, command=self.handle_control_change)

        self.flip_var = tk.BooleanVar(value=False)
        flip_checkbox = tk.Checkbutton(controls_frame, onvalue=True, offvalue=False, variable=self.flip_var, command=self.handle_control_change)

        self.mirror_var = tk.BooleanVar(value=False)
        mirror_checkbox = tk.Checkbutton(controls_frame, onvalue=True, offvalue=False, variable=self.mirror_var, command=self.handle_control_change)

        self.action_select_box.grid(row=0, column=1, sticky=NSEW)
        self.width_entry.grid(row=1, column=1)
        self.height_entry.grid(row=2, column=1)

        quality_entry.grid(row=0, column=3)
        border_entry_frame.grid(row=1, column=3)
        invert_checkbox.grid(row=2, column=3)

        flip_checkbox.grid(row=0, column=5)
        mirror_checkbox.grid(row=1, column=5)
        grayscale_checkbox.grid(row=2, column=5)

        controls_frame.pack(side=BOTTOM, fill=BOTH)

    def handle_border_color(self):
        color_answer = askcolor()
        color = color_answer[1]
        self.border_color_var.set(color)
        self.border_width_entry.config({'bg': color})
        self.trigger_control_change()

    def handle_action_change(self, value):
        if value != "None":
            self.width_entry.config({'state': ACTIVE})
            self.height_entry.config({'state': ACTIVE})
        else:
            self.width_entry.config({'state': DISABLED})
            self.height_entry.config({'state': DISABLED})

    def get_config(self, output_folder_path = None):
        return IPConfig(
            width=int(self.width_var.get()),
            height=int(self.height_var.get()),
            quality=int(self.quality_var.get()),
            action=self.action_var.get(),
            output_folder=output_folder_path,
            border=(int(self.border_width_var.get()), self.border_color_var.get()),
            invert=self.invert_var.get(),
            grayscale=self.grayscale_var.get(),
            flip=self.flip_var.get(),
            mirror=self.mirror_var.get(),
        )

    def handle_control_change(self):
        self.trigger_control_change()

    def on_control_change(self, cb):
        self.trigger_control_change = cb