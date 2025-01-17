from .button_processor import Button_Processor
from .command import Command_Type
from .pdf_meta import PDF_Meta
import tkinter as tk
from .canvas import Canvas
from .utils import extract_file_name
from .logger import Logger

class Button_Canvas:
    """Controls the setup for the button canvas section"""
    def __init__(self, name:str=None, Window:tk.Tk=None, width:int=None, height:int=None, expand:bool=None):
        Logger().print(f"[Button Canvas] Initiating {name}...")
        self.name = name
        self.window = Window
        
        self.canvas_width = width
        self.canvas_height = height
        self.canvas_expand = expand
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=self.canvas_expand)
        
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((10, 10), window=self.frame, anchor="nw")

        self.processor = Button_Processor()
        self.setup_buttons()

        # Force focus on the window and entry box
        #self.window. update_idletasks()  # Ensure widgets are drawn
        self.window.focus_force()  # Bring the window to focus
        self.delete_box.focus_set()  # Set focus on the first Entry widget
        Logger().print(f"[{self.name}] complete.")
    
    def button_pressed(self, type:Command_Type=None, user_input:tk.Entry=None):
        self.processor.on_submit(type, user_input=user_input)
        pdf_length = PDF_Meta().pdf_length()
        message = f"PDF has {pdf_length} page{'s' if pdf_length > 1 else ''}"
        self.pdf_length_label.config(text=message)
        pass

    def setup_buttons(self):
        Logger().print(f"[{self.name}] Setting up UI buttons...")
        # Save Current Iteration Button
        row = 0
        
        self.pdf_name_label = tk.Label(self.frame, text=extract_file_name(PDF_Meta().get_save_file_path()), font=("Arial", 18, "bold"))
        self.pdf_name_label.grid(row=row, column=0, padx=10, pady=20)
        pdf_length = PDF_Meta().pdf_length()
        message = f"PDF has {pdf_length} page{'s' if pdf_length > 1 else ''}"
        self.pdf_length_label = tk.Label(self.frame, text=message, font=("Arial", 18))
        self.pdf_length_label.grid(row=row, column=1, padx=10, pady=20)
        row += 1
        #self.pdf_length_label.config(text=PDF_Meta().pdf_length())

        # Save Button
        self.save_button = tk.Button(self.frame, text="Save", font=("Arial", 14), command=lambda: self.button_pressed(Command_Type.SAVE))
        self.save_button.grid(row=row, column=0, padx=5, pady=20)
        # Help Button
        self.help_button = tk.Button(self.frame, text="Help", font=("Arial", 14), command=lambda: self.open_instructions())
        self.help_button.grid(row=row, column=1, padx=10, pady=20)

        # Undo Button
        #self.undo_button = tk.Button(self.frame, text="Undo", font=("Arial", 14), command=lambda: self.processor.on_submit(Command_Type.UNDO))
        #self.undo_button.grid(row=row, column=1, padx=5, pady=20)
        row += 1

        # Redo Button
        #self.redo_button = tk.Button(self.frame, text="Redo", font=("Arial", 14), command=lambda: self.processor.on_submit(Command_Type.REDO))
        #self.redo_button.grid(row=row, column=0, padx=5, pady=20)

        # Merge Button
        self.merge_button = tk.Button(self.frame, text="Merge", font=("Arial", 14), command=lambda: self.button_pressed(Command_Type.MERGE))
        self.merge_button.grid(row=row, column=0, padx=5, pady=20)
        # Copy Button
        self.copy_button = tk.Button(self.frame, text="Copy", font=("Arial", 14), command=lambda: self.button_pressed(Command_Type.COPY))
        self.copy_button.grid(row=row, column=1, padx=5, pady=20)
        row += 1

        # Delete Pages Button
        self.delete_box = tk.Entry(self.frame, width=30, font=("Arial", 14))
        self.delete_box.grid(row=row, column=1, padx=10, pady=20)
        self.delete_button = tk.Button(self.frame, text="Delete", font=("Arial", 14), command=lambda: self.button_pressed(Command_Type.DELETE, self.delete_box))
        self.delete_button.grid(row=row, column=0, padx=10, pady=20)
        row += 1

        # Move Pages Button 
        self.move_box = tk.Entry(self.frame, width=30, font=("Arial", 14))
        self.move_box.grid(row=row, column=1, padx=10, pady=20)  # Add some spacing around the widget
        self.move_button = tk.Button(self.frame, text="Move", font=("Arial", 14), command=lambda: self.button_pressed(Command_Type.MOVE, self.move_box))
        self.move_button.grid(row=row, column=0, padx=10, pady=20)
        row += 1

        # Split Button
        self.split_box = tk.Entry(self.frame, width=30, font=("Arial", 14))
        self.split_box.grid(row=row, column=1, padx=10, pady=20)  # Add some spacing around the widget
        self.split_button = tk.Button(self.frame, text="Split", font=("Arial", 14),  command=lambda: self.button_pressed(Command_Type.SPLIT, self.split_box))
        self.split_button.grid(row=row, column=0, padx=10, pady=20)
        row += 1

        Logger().print(f"[{self.name}] Buttons complete.")

    def connect_renderer_to_button_processor(self, renderer):
        Logger().print(f"[{self.name}] Connecting to renderer to processor...")
        self.processor.connect_to_renderer(renderer)
        Logger().print(f"[{self.name}] Processor connected.")
    
    def open_instructions(self, agrs=None):
        Logger().print(f"[{self.name}] Opening instructions...")

        # Create a new top-level window
        popup = tk.Toplevel()
        popup.title("PDF Instructions")
        # Set the window to full screen
        popup.attributes('-fullscreen', True)
        #popup.geometry("700x1000")  # Set the size of the window
        
        def on_close():
            Logger().print(f"[{self.name}] Window closed.")
        def button_close():
            Logger().print(f"[{self.name}] Window closed.")
            popup.destroy()

        # Bind the close event to the custom function
        popup.protocol("WM_DELETE_WINDOW", on_close)
        
        # Create a canvas and a scrollbar
        canvas = tk.Canvas(popup, width=700, height=1000)
        scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # Create a frame inside the canvas to hold the content
        content_frame = tk.Frame(canvas)
        canvas.create_window((50, 0), window=content_frame, anchor="nw")

        # Function to adjust the canvas scroll region
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Bind the event to update the scroll region when the frame size changes
        content_frame.bind("<Configure>", update_scroll_region)

        # Instructions
        range_instructions = \
"""     A range of pages to be selected are of this format:
<integer>-<integer>. An example of this would be: 4-6.
In this example, pages 4 through 6 were selected. Whenever 
the instructions say a range of pages can be selected, a 
number followed by a dash followed by another number will 
represent the pages you want to select."""

        delete_instructions = \
"""     To use the delete feature, select the text box next 
to the right side of the delete button. Next put in 
the desired pages to be removed from the pdf. You 
can use a range of pages or a singular page to remove, 
as long as you format the input correctly, the pages will
be removed in real time. The format for specifying a
range: <integer>-<integer> or and example would be 
1-5 which will select the pages 1 through 5. You can
also select multiple pages or ranges that aren't next
to each other. You do this by separating the desired
locations by a comma. The format for selecting multiple
ranges or pages not next to each other: <integer>-<integer>, 
<integer>, ... and so on. An example of this is 1-5, 7, 
18, 10-13. Here I've selected pages 1-5, 7, 18, and 10 
through 13 to be deleted. After inputting your desired 
pages, press the delete button to the side. To permanently
delete the pages."""

        move_instructions = \
"""     To use the move feature, select the text box next to 
the right side of the move button. Next put in the 
desired pages to be moved inside the pdf. You can 
select singular pages separated by a comma or a range 
of pages. Whether it be singular or multiple pages 
wanted to be selected, a comma must be placed to 
display your desire to select another grouping of 
page(s). After you place how what pages you would like
to move, you must select a target area you want the 
pages to be located. After selection of pages, place a 
semicolon followed by another integer representing the 
page number you would like the pages to move after. An
example of wanting to move pages 4, 16, and 7-10 after
page 20 would be: 4, 16, 7-10;20. After inputting your
desired location and pages, press the move button to 
the side."""

        split_instructions = \
"""     To use the split feature, select the text box next to 
the right side of the split button. Next put in how 
many pages should remain in the original pdf. This a
singular integer value that should reflect how many
pages you would like to stay in the current PDF open
and the rest will be moved to a file your choosing.
After placing your number inside the text box, press
the split button and you will be prompted to name the
file you would like the split off pages to be inside
of. Make sure the file name doesn't have any "." extension
inside the name. Once that's done, you'll be prompted
to choose a folder on your machine to store the new
file. Selecting the folder is the last step and you
can find the pages you left inside the current pdf,
and the pages that you didn't want were moved to 
the other pdf you named."""

        merge_instructions = \
"""     To use the merge feature, press the merge button. Next 
select what PDF you would like the merge onto the current 
PDF. After selecting, you'll notice that the PDF selected 
will be appended to the bottom of the currently opened PDF."""

        save_instructions = \
"""     To save the PDF, press the save button. The PDF you 
chose originally will have all of the unsaved changes 
added to the original PDF. WARNING! If you close the PDF 
editor without saving, all of the PDF modifications will 
not be saved!"""

        copy_instructions = \
"""     To copy the PDF, press the copy button. After pressing the
copy button, you'll be asked to enter a file name without an 
extension. Once entering a valid file name, you must select a 
folder you want the copy to go into. Selecting a folder was the 
last step and you can find the copy at that location.
"""

        # Layout Variables
        row = 0
        # Labels
        range_label = tk.Label(content_frame, text="What's A Range?", font=("Arial", 24))
        range_label.grid(row=row, column=0, padx=10, pady=20)
        merge_label = tk.Label(content_frame, text="How To Merge PDFs", font=("Arial", 24))
        merge_label.grid(row=row, column=1, padx=10, pady=20)
        save_label = tk.Label(content_frame, text="How To Save Your PDF", font=("Arial", 24))
        save_label.grid(row=row, column=2, padx=10, pady=20)
        row += 2
        del_label = tk.Label(content_frame, text="How To Delete Pages", font=("Arial", 24))
        del_label.grid(row=row, column=0, padx=10, pady=20)
        move_label = tk.Label(content_frame, text="How To Move Pages", font=("Arial", 24))
        move_label.grid(row=row, column=1, padx=10, pady=20)
        split_label = tk.Label(content_frame, text="How To Split A PDF", font=("Arial", 24))
        split_label.grid(row=row, column=2, padx=10, pady=20)
        row += 2
        copy_label = tk.Label(content_frame, text="How To Copy Your PDF", font=("Arial", 24))
        copy_label.grid(row=row, column=0, padx=10, pady=20)
        
        # Instructions
        row = 1
        # Range Instructions
        range_instructions_label = tk.Label(
            content_frame,
            text=range_instructions,
            font=("Arial", 16),
            justify="left",   # Align the text to the left
            wraplength=600    # Wrap the text at 350 pixels
        )
        range_instructions_label.grid(row=row, column=0, padx=10, pady=20)
        # Merge Instructions
        merge_instructions_label = tk.Label(
            content_frame,
            text=merge_instructions,
            font=("Arial", 16),
            justify="left",   # Align the text to the left
            wraplength=600    # Wrap the text at 350 pixels
        )
        merge_instructions_label.grid(row=row, column=1, padx=10, pady=20)
        # Save Instructions
        save_instructions_label = tk.Label(
            content_frame,
            text=save_instructions,
            font=("Arial", 16),
            justify="left",   # Align the text to the left
            wraplength=600    # Wrap the text at 350 pixels
        )
        save_instructions_label.grid(row=row, column=2, padx=10, pady=20)

        row += 2
        # Delete Instructions
        delete_instructions_label = tk.Label(
            content_frame,
            text=delete_instructions,
            font=("Arial", 16),
            justify="left",   # Align the text to the left
            wraplength=600    # Wrap the text at 350 pixels
        )
        delete_instructions_label.grid(row=row, column=0, padx=10, pady=20)
        # Move Instructions
        move_instructions_label = tk.Label(
            content_frame,
            text=move_instructions,
            font=("Arial", 16),
            justify="left",   # Align the text to the left
            wraplength=600    # Wrap the text at 350 pixels
        )
        move_instructions_label.grid(row=row, column=1, padx=10, pady=20)
        # Split Instructions
        split_instructions_label = tk.Label(
            content_frame,
            text=split_instructions,
            font=("Arial", 16),
            justify="left",   # Align the text to the left
            wraplength=600    # Wrap the text at 350 pixels
        )
        split_instructions_label.grid(row=row, column=2, padx=10, pady=20)
        
        row += 2
        # Copy Instructions
        copy_instructions_label = tk.Label(
            content_frame,
            text=copy_instructions,
            font=("Arial", 16),
            justify="left",   # Align the text to the left
            wraplength=600    # Wrap the text at 350 pixels
        )
        copy_instructions_label.grid(row=row, column=0, padx=10, pady=20)
        
        # Close Button
        self.close_button = tk.Button(content_frame, text="Close", font=("Arial", 30), command=button_close)
        self.close_button.grid(row=row, column=1, padx=10, pady=20)

        Logger().print(f"[{self.name}] Instructions opened.")