
import tkinter as tk
from .canvas import Canvas
from .utils import remove_file
from .pdf_meta import PDF_Meta
from .logger import Logger

class Window:
    """Controls all GUI setup with the window variable"""
    def __init__(self, window:tk.Tk):
        Logger().print("[Window] Initiating window...")
        self.window = window
        self.window.title("PDF Viewer")
        self.win_width = 2100
        self.win_height = 1300
        self.window.geometry(f"{self.win_width}x{self.win_height}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        Logger().print("[Window] Window completed.")

    
    def on_mouse_wheel(self, event, main_canvas:Canvas, sub_canvas:Canvas):
        """Scroll both canvases proportionally."""
        main_scroll_speed = -1 * (event.delta // 120)

        # Scroll the main canvas
        main_canvas.canvas.yview_scroll(main_scroll_speed, "units")

        # Scroll the smaller canvas proportionally
        difference = main_canvas.scrollbar.get()[1] - main_canvas.scrollbar.get()[0]
        main_middle = main_canvas.scrollbar.get()[0] + difference/2.0
        sub_difference = sub_canvas.scrollbar.get()[1] - sub_canvas.scrollbar.get()[0]
        sub_canvas.canvas.yview_moveto(main_middle - sub_difference/2.0)
    
    def bind(self, main_canvas:Canvas, sub_canvas:Canvas):
        Logger().print("[Window] Initiating window binds...")
        self.window.bind_all("<MouseWheel>", lambda event: self.on_mouse_wheel(event, main_canvas, sub_canvas))  # For Windows
        Logger().print("[Window] Window binds completed.")

    # Define the function to handle the window close event
    def on_close(self):
        Logger().print("[Window] Closing window...")
        PDF_Meta().close_pdf()
        remove_file(PDF_Meta().get_file_path())
        Logger().print("[Window] Window closing.")
        self.window.destroy()  # Close the window