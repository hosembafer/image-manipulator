import asyncio
import threading
import tkinter as tk
from tkinter import BOTH, CENTER, RIGHT, TOP, ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from actions import Actions
from src.image_processor import ImageProcessor, process_image
from src.controls import Controls

window_width = 800
window_height = 500

window = tk.Tk()
window.resizable(False, False)
window.title("Image manipulator")
window.config(padx=12)
window.config(pady=12)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

root = window
master = window

PREVIEW_SIZE = 128

progress_var = tk.DoubleVar()

image_processor = ImageProcessor()

canvas = tk.Canvas(window, width = PREVIEW_SIZE, height = PREVIEW_SIZE)

def open_file_chooser():
    global file_paths
    new_file_paths = fd.askopenfilenames()
    file_paths |= set(new_file_paths)
    
    items_listbox.delete(0, items_listbox.size())
    for index, path in enumerate(file_paths):
        items_listbox.insert(index, path)

def handle_start():
    if len(file_paths) == 0:
        tk.messagebox.showinfo("Empty file list", "No images selected")
        return

    output_folder_path = fd.askdirectory()
    
    if output_folder_path:
        image_processor.force_stopped = False
        config = controls.get_config(output_folder_path)
        thread = threading.Thread(target=image_processor.start_processing, args=(file_paths, config,))
        thread.start()

def handle_stop():
    progress_var.set(0)
    asyncio.run(image_processor.stop_processing())

actions = Actions(window, open_file_chooser, handle_start, handle_stop)
def handle_clear_list():
    global file_paths
    items_listbox.delete(0, len(file_paths))
    file_paths = set()
actions.on_clear_list(handle_clear_list)

list_frame = tk.Frame(window)

scrollbar = ttk.Scrollbar(list_frame, orient="vertical")

items_listbox = tk.Listbox(list_frame, width=50, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=items_listbox.yview)
scrollbar.pack(side="right", fill="y", expand=False)
items_listbox.pack(side="top",fill="both", expand=True)

def handle_item_process_complete(index):
    items_listbox.itemconfig(index, {'bg':'#00CC44'})
image_processor.on_item_process_complete(handle_item_process_complete)

async def handle_process_complete():
    for n in range(0, len(file_paths)):
        items_listbox.itemconfig(n, {'bg':'systemTransparent'})
    await asyncio.sleep(0.1)
    tk.messagebox.showinfo("Completed", "Completed")
    progress_var.set(0)
image_processor.on_process_complete(handle_process_complete)

python_image = None
selected_file_path = None

def draw_preview():
    global python_image, canvas
    image = Image.open(selected_file_path)
    image = process_image(image, config=controls.get_config(), skip_action=True)
    image = image.resize(size=(PREVIEW_SIZE, PREVIEW_SIZE))
    python_image = ImageTk.PhotoImage(image)
    canvas.create_image(PREVIEW_SIZE / 2, PREVIEW_SIZE / 2, anchor=CENTER, image=python_image)

def callback(event):
    global python_image, selected_file_path
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        payload = event.widget.get(index)
        selected_file_path = payload
        draw_preview()

items_listbox.bind("<<ListboxSelect>>", callback)

list_frame.pack(side=TOP, fill=BOTH)

progress_bar = ttk.Progressbar(window, orient='horizontal', mode="determinate", length=800, variable=progress_var)
progress_bar.pack()
progress_var.set(0)

def handle_progress_update(percent):
    progress_var.set(percent)
image_processor.on_progress_update(handle_progress_update)


file_paths = set()

canvas.pack(side=RIGHT)

controls = Controls(window)
controls.on_control_change(draw_preview)

window.mainloop()