from .window import Window
from .canvas import Canvas
from .button_canvas import Button_Canvas
from .pdf_meta import PDF_Meta
from .logger import Logger
import tkinter as tk


class Renderer:
    """Focuses on building the GUI and handles all layout features associated with it"""
    def __init__(self, window:tk.Tk=None):
        Logger().print("[Renderer] Initiating renderer...")
        # Initiate members
        try:
            if window is None:
                raise TypeError("Window is of type None, make sure the window is being passed correctly to the renderer!")
        except TypeError as e:
            Logger().print(f"Error: {e}")

        self.window = Window(window)
        self.sub_canvas = Canvas(name="Sub Canvas", Window=window, width=450, height=500, expand=False)
        self.sub_canvas.create_frame(x=10, y=0)
        self.main_canvas = Canvas(name="Main Canvas", Window=window, width=550, height=500, expand=True)
        self.main_canvas.create_frame(x=10, y=0)
        self.button_canvas = Button_Canvas(name="Button Canvas", Window=window, width=50, height=500, expand=True)
        self.button_canvas.connect_renderer_to_button_processor(self)

        # Assign bindings
        self.main_canvas.bind(self.sub_canvas)
        self.sub_canvas.bind(self.main_canvas)
        self.window.bind(main_canvas=self.main_canvas, sub_canvas=self.sub_canvas)
        Logger().print("[Renderer] Renderer complete.")
    
    def update_image_labels(self):
        Logger().print("[Renderer] Updating image labels...")
        # Clear the frames
        self.main_canvas.clear_frame()
        self.sub_canvas.clear_frame()
        # Assign images
        self.main_canvas.create_image_labels(pages=PDF_Meta().get_pdf(), scaling=1.6, padding=10)
        self.sub_canvas.create_image_labels(pages=PDF_Meta().get_pdf(), scaling=0.7, padding=20)
        Logger().print("[Renderer] Image labels updated.")