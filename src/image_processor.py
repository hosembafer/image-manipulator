import asyncio
import os
from PIL import Image, ImageOps
    
class IPConfig:
    width: int
    height: int
    size: tuple
    action: str
    quality: int
    output_folder: str
    border: tuple
    flip: bool
    mirror: bool
    grayscale: bool
    invert: bool

    def __init__(self, width, height, quality, action, output_folder = None, border = None, flip = None, mirror = None, grayscale = None, invert = None):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.quality = quality
        self.action = action
        self.output_folder = output_folder
        self.border = border

        self.flip = flip
        self.mirror = mirror
        self.grayscale = grayscale
        self.invert = invert

def process_image(img, config: IPConfig, skip_action = None):
    if skip_action != True:
        if config.action == "Resize":
            img = ImageOps.contain(img, config.size)
        elif config.action == "Crop":
            img = ImageOps.fit(img, config.size)

    if config.border != None and config.border[0] != 0:
        img = ImageOps.expand(img, border=config.border[0], fill=config.border[1])
    
    if config.flip:
        img = ImageOps.flip(img)
    if config.mirror:
        img = ImageOps.mirror(img)
    if config.grayscale:
        img = ImageOps.grayscale(img)
    if config.invert:
        img = ImageOps.invert(img)

    return img

class ImageProcessor:
    config: IPConfig
    force_stopped: bool = False
    completed_count: int = 0
    file_paths: set
    total_count: int

    def start_processing(self, file_paths, config):
        self.file_paths = file_paths
        self.total_count = len(file_paths)
        self.force_stopped == False
        self.config = config

        for index, filePath in enumerate(file_paths):
            self.process(index, filePath)

    def process(self, index, filePath):
        if self.force_stopped == True:
            return

        self.trigger_item_process_complete(index)
        base_name = os.path.basename(filePath)
        img = Image.open(filePath)
        img = process_image(img, self.config)
        
        outputFilePath = self.config.output_folder + "/" + base_name
        img.save(outputFilePath, quality=self.config.quality, optimize=True)
        self.completed_count += 1
        self.update_progress()

        if self.total_count == self.completed_count:
            self.mark_completed()

    def mark_completed(self):
        self.completed_count = 0
        asyncio.run(self.trigger_process_complete())

    async def stop_processing(self):
        self.force_stopped = True
        await asyncio.sleep(0.1)
        self.completed_count = 0
        
    def update_progress(self):
        percent = 100 / self.total_count * self.completed_count
        self.trigger_progress_update(int(percent))

    def on_item_process_complete(self, cb):
        self.trigger_item_process_complete = cb
    
    def on_process_complete(self, cb):
        self.trigger_process_complete = cb
    
    def on_progress_update(self, cb):
        self.trigger_progress_update = cb
