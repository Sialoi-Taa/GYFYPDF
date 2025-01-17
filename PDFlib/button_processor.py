from .command import Command, Command_Type
from .pdf_meta import PDF_Meta, TMP
from .logger import Logger
import tkinter as tk
import pypdfium2 as pdfium
from typing import List, Optional
import os
from .utils import *
import re
import tempfile

class Button_Processor:
    def __init__(self, renderer=None):
        Logger().print("[Button Processor] Initiating button processor...")
        self.processes = {
            Command_Type.SAVE:self.save_procedure, 
            Command_Type.UNDO:self.undo_procedure,
            Command_Type.REDO:self.redo_procedure, 
            Command_Type.MERGE:self.merge_procedure,
            Command_Type.DELETE:self.delete_procedure, 
            Command_Type.SPLIT:self.split_procedure,
            Command_Type.MOVE:self.move_procedure,
            Command_Type.COPY:self.copy_procedure
            }
        self.renderer = renderer
        Logger().print("[Button Processor] Button processor complete.")

    def copy_procedure(self, user_input:tk.Entry=None):
        Logger().print("[copy_procedure] Copying file...")
        file_name = ask_file_name()
        dir = ask_for_directory()
        new_file = dir + file_name
        prep_dest_file(file_name)
        PDF_Meta().get_pdf().save(new_file)
        Logger().print("[copy_procedure] File copied.")
        pass

    def save_procedure(self, user_input:tk.Entry=None):
        """Save the file with new changes"""
        Logger().print("\n[Button Processor] Starting save procedure...")
        PDF_Meta().save()
        # TODO: Overwrite to the current PDF
        Logger().print("[Button Processor] Save procedure finished.")
        return True
    def undo_procedure(self, user_input:tk.Entry=None):
        """Undo the last change"""
        Logger().print("\n[Button Processor] Starting undo procedure...")
        # Get all relevant data
        data = Logger().get_data()
        undos = data["undos"]
        redos = data["redos"]
        history = data["history"]
        # Check the history and undo the last action
        #reverse(history[-1])
        Logger().print("[Button Processor] Undo procedure finished.")
        return True
    def redo_procedure(self, user_input:tk.Entry=None):
        """Redo the last change"""
        Logger().print("\n[Button Processor] Starting redo procedure...")
        # Check to see if there's anything to undo
        undos = Logger().get_data()["undos"]
        if len(undos) == 0:
            Logger().print("Nothing to undo!")
            return True
        # Take the last undo
        last_undo = undos[-1]
        # Make a copy
        command = last_undo.copy()
        # Pop the undo 
        Logger().pop_undo()
        # Push into history and redo
        Logger().push_history(command)
        Logger().push_redo(command)
        # Reverse it 
        #reverse(command) # TODO
        Logger().print("[Button Processor] Redo procedure finished.")
        return True
    
    def merge_procedure(self, user_input:tk.Entry=None):
        """Merge 2 PDFs"""
        Logger().print("\n[Button Processor] Starting merge procedure...")
        # Ask for file to merge
        merge_file_path = open_file()
        if not merge_file_path:
            # File not valid
            return None

        pdf = pdfium.PdfDocument(merge_file_path)
        current_pdf = PDF_Meta().get_pdf()
        current_pdf.import_pages(pdf)
        pdf.close()

        # Write current save to a new file
        tmp_path = tempfile.gettempdir() + "\\holder.pdf"
        
        prep_dest_file(tmp_path)
        current_pdf.save(tmp_path)

        # Remove current PDF file
        origin_path = PDF_Meta().get_file_path()
        PDF_Meta().close_pdf()
        remove_file(origin_path)

        # Rename tmp file into current pdf
        rename_file(tmp_path, origin_path)
        PDF_Meta().reopen_pdf()

        # Record command
        Command(type=Command_Type.MERGE, merge_file_path=user_input)
        self.renderer.update_image_labels()
        Logger().print("[Button Processor] Merge procedure finished.")
        return True

    def deletion_command(self, pages_selected:List[int], command:Command)->Optional[bool]:
        Logger().print("\n[Button Processor] Creating delete command...")
        command.info["identity"] = Command_Type.DELETE
        command.info["selected"] = pages_selected
        s = "Pages "
        for i, page in enumerate(pages_selected):
            if i+1 == len(pages_selected):
                s = s + str(page) + " "
            elif i+2 == len(pages_selected):
                s = s + str(page) + " and "
            else:
                s = s + str(page) + ", "
        s = s + "were deleted."
        command.info["description"] = s
        Logger().print("[Button Processor] Delete command created.")

    def delete_procedure(self, user_input:tk.Entry=None):
        """Delete selected page(s)"""
        Logger().print("\n[Button Processor] Starting delete procedure...")
        # Parse through the user input
        # Check for any characters except for numbers, commas, periods and minus
        page_nums = user_input.get()
        user_input.delete(0, tk.END)
        try:
            # Checks if any invalid characters are detected
            if not is_valid_deletion_string(page_nums):
                raise ValueError("User entered an invalid input!")
            
            # Parses the string into page selects 
            page_nums = re.findall(r'-?\d+\.?\d*(?:-\d+)?', page_nums)
            
            # Changes the list of page selects into a set of unique page numbers
            page_nums = del_str_list_to_int_list(page_nums)
        except ValueError as e:
            Logger().print(f"Error: {e}")
            return None
        
        command = Command()
        
        # Record the command and record what happened
        self.deletion_command(pages_selected=page_nums, command=command)
        
        # Edit current PDF
        PDF_Meta().remove_pages(pages_to_remove=page_nums)
        self.renderer.update_image_labels()
        Logger().print("[Button Processor] Delete procedure finished.")
        return True
    
    def split_parser(self, s:str=None) -> Optional[int]:
        Logger().print("\n[Button Processor] Starting split parser...")
        try:
            if not s.isdigit():
                # String not an integer
                raise ValueError("User did not put in a positive integer")
            elif not (int(s) > 0 and int(s) < len(PDF_Meta().get_data()["pdf"])):
                # Integer not inside the scope of page range
                raise ValueError("User chose a page number outside of pdf scope")
        except ValueError as e:
            Logger().print(f"Error: {e}")
            return None
        Logger().print("Split parser finished.")
        return int(s)
    
    def split_procedure(self, user_input:tk.Entry=None):
        """Split the PDF into 2 at point"""
        Logger().print("\n[Button Processor] Starting split procedure...")
        # Parse the input, find the target point to split the pdf
        target = self.split_parser(user_input.get())
        user_input.delete(0, tk.END)
        
        # Ask for the new name of the file to split off into
        file_name = ask_file_name()
        
        # Ask for the new destination
        file_dest = ask_for_directory()

        full_target_path = file_dest + file_name 
        # Write to the new file from the pdf split onwards
        split_pdf(PDF_Meta().get_file_path(), target, full_target_path)
        if ask_to_remove_pages_from_original():
            # Delete the contents after the partition on current PDF
            pages_to_remove = []
            pages_to_remove.extend(range(target, len(PDF_Meta().get_pdf())))
            PDF_Meta().remove_pages(pages_to_remove)
        # Update PDF View
        self.renderer.update_image_labels()

        ### TODO: COMMAND HISTORY INJECTION AND RECORDING
        Logger().print("[Button Processor] Split procedure finished.")
        return True
    
    def move_procedure(self, user_input:tk.Entry=None):
        """Move selected page(s) to after certain page"""
        Logger().print("\n[Button Processor] Starting move procedure...")
        # Get the user's input
        user_text = user_input.get()
        user_input.delete(0, tk.END)
        # Input format should be: (page or range);(location after a certain page)
        if not move_input_validation(input_string=user_text):
            return False
        # Collect both sides of the string and separate to between targets and target location
        collection = move_parser(user_text)
        page_nums_to_move = collection[0]
        target = collection[1][0]

        # Move the pages
        move_page(page_move_list=page_nums_to_move, target=target)

        # Update PDF view
        self.renderer.update_image_labels()

        ### TODO: COMMAND HISTORY INJECTION AND RECORDING
        Logger().print("[Button Processor] Move procedure finished.")
        return True

    def on_submit(self, type:Command_Type=None, user_input:tk.Entry=None) -> bool:
        if not PDF_Meta().is_setup_complete():
            return False
        return self.processes[type](user_input)

    def connect_to_renderer(self, renderer):
        Logger().print("[Button Processor] Connecting to renderer...")
        self.renderer = renderer
        Logger().print("[Button Processor] Renderer connected.")