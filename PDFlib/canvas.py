import tkinter as tk
from PIL import Image, ImageTk
from .logger import Logger

class Canvas:
    """Controls the setup and interactions with a TK canvas and custom classes"""
    def __init__(self, name:str=None, Window:tk.Tk=None, width:int=None, height:int=None, expand:bool=True):
        Logger().print(f"[{name}] Initiating Canvas...")
        self.name = name
        self.window = Window
        self.canvas_width = width
        self.canvas_height = height
        self.canvas_expand = expand
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=self.canvas_expand)
        self.frame = None

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)  # Place the scrollbar on the LEFT side of the micro canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        Logger().print(f"[{self.name}] Initiating Canvas...")

    def clear_frame(self):
        Logger().print(f"[{self.name}] Clearing frames...")
        for widget in self.frame.winfo_children():
            widget.destroy()
        Logger().print(f"[{self.name}] Frames cleared.")

    def on_scrollbar_drag(self, can2:"Canvas"=None):
        # Scroll the smaller canvas proportionally
        difference1 = self.scrollbar.get()[1] - self.scrollbar.get()[0]
        middle1 = self.scrollbar.get()[0] + difference1/2.0
        difference2 = can2.scrollbar.get()[1] - can2.scrollbar.get()[0]
        can2.canvas.yview_moveto(middle1 - difference2/2.0)
    
    # Configure the canvas scroll region
    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_frame(self, x:int=0, y:int=0):
        Logger().print(f"[{self.name}] Creating frame...")
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((x, y), window=self.frame, anchor="nw")
        Logger().print(f"[{self.name}] Frame created.")

    def bind(self, a_canvas:"Canvas"=None):
        Logger().print(f"[{self.name}] Initiating binding...")
        self.scrollbar.bind('<B1-Motion>', lambda event: self.on_scrollbar_drag(a_canvas))
        self.frame.bind("<Configure>", lambda e: self.update_scrollregion(e))
        Logger().print(f"[{self.name}] Binding finished.")
        

    def page_to_img(self, page, scaling=1.6):
        Logger().print(f"[{self.name}] Changing page to img...")
        bitmap = page.render(
            scale=scaling,    # 72dpi resolution
            rotation=0,       # no additional rotation
        )
        Logger().print(f"[{self.name}] Img created.")
        return bitmap.to_pil()

    def create_image_labels(self, pages, scaling=1.6, padding=10):
        """Create labels with images and add them to the frame."""
        Logger().print(f"[{self.name}] Creating image labels...")
        for page_num, page in zip(range(1, len(pages) + 1), pages):
            image = self.page_to_img(page, scaling)
            
            tk_image = ImageTk.PhotoImage(image)
            # Store a reference to prevent garbage collection
            image_label = tk.Label(self.frame, image=tk_image)
            image_label.image = tk_image
            image_label.pack(pady=padding)  # Add some spacing between images

            # Create a label for the text and add it under the image
            text_label = tk.Label(self.frame, text=f"Page {page_num}", font=("Arial", 20))
            text_label.pack(pady=padding // 2)  # Add some padding between the image and text
        self.canvas.yview_moveto(0)
        Logger().print(f"[{self.name}] Image labels created.")