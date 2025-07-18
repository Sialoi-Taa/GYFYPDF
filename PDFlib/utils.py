
from typing import List, Optional, Set
from tkinter import filedialog, simpledialog
import pypdfium2 as pdfium
from PDFlib.pdf_meta import PDF_Meta
import shutil, re, pypdf, tempfile, os, tkinter as tk
from .logger import Logger


def is_invalid(lst):
    Logger().print("[is_invalid] Returned if list is invalid.")
    return any(isinstance(item, float) or (item < 0 or item > len(PDF_Meta().get_data())) for item in lst)

def is_valid_deletion_string(input_string):
    Logger().print("[is_valid_deletion_string] Returned string is a valid deletion input.")
    # Regex to match a string with only allowed characters
    if re.fullmatch(r'[0-9,\-\s]*', input_string):
        return True  # Valid string
    return False  # Invalid string

def string_elems_to_int_list(str_list:List[str]=None, lb:int=None, ub:int=None) -> List[str]:
    Logger().print("[string_elems_to_int_list] Turning string list into int list...")
    ret = []
    lower_bound = lb
    upper_bound = ub
    try:
        for elem in str_list:
            if '.' in elem:
                raise TypeError("Error: User inputted a decimal!")
            elif '-' in elem:
                # Range detected
                left, right = elem.split('-')
                max_num = None
                min_num = None
                
                # Check if range is completed
                if left == "" or right =="":
                    # Didn't finish the bounds
                    raise ValueError("User inserted a range with nonexistent bounds!")
                max_num = max(int(left), int(right))+1
                min_num = min(int(left), int(right))
                if (min_num<=lower_bound or min_num>upper_bound) or (max_num<=lower_bound or max_num>upper_bound):
                    # Indexed outside the bounds of the PDF
                    raise IndexError("User indexed outisde the PDF bounds!")
                
                # Range Completed
                ret.extend(range(min_num, max_num))
            else:
                # Number detected
                page_num = None
                page_num = int(elem)
                if page_num <= lower_bound or page_num > upper_bound:
                    # Page outside of the PDF range
                    raise IndexError("User indexed outisde the PDF bounds!")
                
                # Append number
                ret.append(page_num)
    except TypeError as e:
        Logger().print(f"TypeError occurred: {e}")
        return None
    except IndexError as e:
        Logger().print(f"IndexError occurred: {e}")
        return None
    except ValueError as e:
        Logger().print(f"ValueError occurred: {e}")
        return None

    Logger().print("[string_elems_to_int_list] String list turned into int list.")
    return ret

def del_str_list_to_int_list(str_list:List[str]=None) -> Optional[List[int]]:
    Logger().print("[del_str_list_to_int_list] Turning deletion string list into a list of ints...")
    ret = []
    upper_bound = len(PDF_Meta().get_pdf())+1
    lower_bound = 0
    ret = string_elems_to_int_list(str_list=str_list, lb=lower_bound, ub=upper_bound)
    # Checks if the list was made successfully
    if not ret:
        Logger().print("[del_str_list_to_int_list] User had invalid input.")
        return None

    # Checks for negative numbered inputs
    if any(x <= 0 for x in ret):
        Logger().print("[del_str_list_to_int_list] User had invalid input that held a negative number.")
        return None
    ret = list(set(ret))
    Logger().print("[del_str_list_to_int_list] Deletion string list turned into a list of ints.")
    return ret

    # Function to open the file dialog and select a file
def open_file():
    Logger().print("[open_file] Opening existing file...")
    file_path = filedialog.askopenfilename(title="Select a file", 
                                           filetypes=[("Text files", "*.pdf"), ("All files", "*.*")])
    try:
        if file_path:
            Logger().print(f"[open_file] File selected: {file_path}")
        else:
            raise FileNotFoundError("No file selected")
    except FileExistsError as e:
        Logger().print(f"[open_file] Error: {e}") 
    except FileNotFoundError as e:
        Logger().print(f"[open_file] Error: {e}")
    
    Logger().print("[open_file] File opened.")
    return file_path

# Function to prompt for a file name
def ask_file_name():
    Logger().print("[ask_file_name] Asking for a file...")
    file_name = simpledialog.askstring("Input", "Enter the name for the file with no .extension:")

    try:
        if all(c.isalnum() or c == '_' for c in file_name):
            Logger().print("[ask_file_name] Returning desired file name.")
            return file_name + ".pdf"
        else:
            raise ValueError("Desired file name had invalid characters. Only alphanumeric and underscores are allowed.")
    except ValueError as e:
        Logger().print(f"[ask_file_name] Error: {e}")
    return None

# Function to prompt for a directory
def ask_for_directory():
    Logger().print("[ask_for_directory] Asking for directory...")
    directory = filedialog.askdirectory(title="Select a directory to save the file")
    try:
        if not directory:
            raise ValueError("No directory selected")
    except ValueError as e:
        Logger().print(f"[ask_for_directory] Error: {e}")
        return None
    Logger().print("[ask_for_directory] Returned desired directory.")
    return directory + "/"

def prep_dest_file(dest_file_path):
    Logger().print("[prep_dest_file] Prepping a new PDF location...")
    # Check if the file already exists
    if os.path.exists(dest_file_path):
        # If it exists, delete it
        os.remove(dest_file_path)
        Logger().print(f"[prep_dest_file] Existing file '{dest_file_path}' deleted.")
    else:
        Logger().print(f"[prep_dest_file] File '{dest_file_path}' does not exist. Creating a new file.")
    
    # Create a new empty PDF
    with open(dest_file_path, 'wb') as file:
        writer = pypdf.PdfWriter()
        writer.write(file)  # Writes an empty PDF structure
        Logger().print(f"[prep_dest_file] New empty PDF created at '{dest_file_path}'.")
    Logger().print("[prep_dest_file] New PDF location prepped.")

def extract_file_name(file_path:str=None):
    if not file_path:
        return ""
    file_name = os.path.basename(file_path)
    if len(file_name) > 10:
        return file_name[:10] + "..."
    return file_name

def split_pdf(source_pdf_path:str=None, partition:int=0, target_pdf_path:str=None):
    Logger().print("[split_pdf] Splitting PDF...")
    if (not source_pdf_path) or (not target_pdf_path):
        Logger().print("Source or target path is None!\nSplit unsuccessful!")
        return
    # Prepping destination file
    prep_dest_file(target_pdf_path)

    # Target file path has to have already have been made!!!
    with open(source_pdf_path, 'rb') as src_file, open(target_pdf_path, 'rb') as trg_file:
        src_pdf = pypdf.PdfReader(src_file)
        trg_pdf = pypdf.PdfWriter(trg_file)

        # Render the source page using pypdfium2
        for source_page_num in range(partition, len(src_pdf.pages)):
            Logger().print(source_page_num)
            # Get source page
            src_page = src_pdf.pages[source_page_num]

            # Add to the target PDF
            trg_pdf.add_page(src_page)

        # Save the modified target PDF
        with open(target_pdf_path, 'wb') as out_file:
            trg_pdf.write(out_file)
    Logger().print("[split_pdf] PDF split.")

def remove_file(file_path):
    Logger().print("[remove_file] Removing file...")
    # Check if the file exists before deleting
    if os.path.exists(file_path):
        os.remove(file_path)
        Logger().print(f"[remove_file] File '{file_path}' has been deleted.")
    else:
        Logger().print(f"[remove_file] File '{file_path}' does not exist.")
    Logger().print("[remove_file] File removed.")

def rename_file(old_file_path, new_file_path):
    Logger().print("[rename_file] Renaming file...")
    # Rename the file
    try:
        os.rename(old_file_path, new_file_path)
        Logger().print(f"[rename_file] File renamed.")
    except FileNotFoundError:
        Logger().print(f"[rename_file] File '{old_file_path}' does not exist.")
    except PermissionError:
        Logger().print(f"[rename_file] Permission denied: Unable to rename '{old_file_path}'.")
    except Exception as e:
        Logger().print(f"[rename_file] Error: {e}")

def remove_pages(input_pdf_path:str=None, pages_to_remove:List[int]=None):
    Logger().print("[remove_pages] Removing pages...")
    # Open the input PDF document
    pdf_document = pdfium.PdfDocument(input_pdf_path)

    # Iterate over all the pages, excluding the one to be removed
    while len(pages_to_remove):
        pdf_document.del_page(pages_to_remove.pop()-1)
    
    # Write the new pdf version to a new pdf
    dest_pdf_path = tempfile.gettempdir() + "\\holder.pdf"
    prep_dest_file(dest_pdf_path)
    pdf_document.save(dest_pdf_path)
    
    # Close the pdf
    pdf_document.close()

    # Delete the original pdf file
    remove_file(input_pdf_path)

    # Rename new pdf to the old pdf name
    rename_file(dest_pdf_path, input_pdf_path)
    Logger().print("[remove_pages] Pages removed.")
    return None

def copy_pdf(source_file_path, dest_file_path):
    Logger().print("[copy_pdf] Copying PDF...")
    remove_file(dest_file_path)
    try:
        shutil.copy(source_file_path, dest_file_path)
        Logger().print("[copy_pdf] PDF copied.")
    except FileNotFoundError:
        Logger().print(f"[copy_pdf] File '{source_file_path}' does not exist.")
    except PermissionError:
        Logger().print(f"[copy_pdf] Permission denied: Unable to copy '{source_file_path}'.")
    except Exception as e:
        Logger().print(f"[copy_pdf] An error occurred: {e}")
    
def is_valid_move_string(input_string:str=None) -> bool:
    Logger().print("[is_valid_move_string] Checking if string is a valid move string...")
    # Regex to match a string with only allowed characters
    if re.fullmatch(r'[0-9,;\-\s]*', input_string):
        Logger().print("[is_valid_move_string] Move string is valid.")
        return True  # Valid string
    Logger().print("[is_valid_move_string] Move string is not valid.")
    return False  # Invalid string

def move_input_validation(input_string:str=None) -> Optional[bool]:
    Logger().print("[move_input_validation] Validating move input string...")
    try:
        # Check holds only valid characters
        if not is_valid_move_string(input_string):
            raise ValueError("User placed invalid charcters inside the input!")
        # Check if ; is present and there's a side on both side
        left, right = input_string.split(";")
        if left == "" or right == "":
            raise ValueError("User didn't input a target to move or a destination to move to!")
    except ValueError as e:
        Logger().print(f"[move_input_validation] Error: {e}")
        return False
    Logger().print("[move_input_validation] Move input string validated.")
    return True

def move_parser(s:str=None) -> List[List[int]]:
    Logger().print("[move_parser] Parsing the string into list of list[ints]...")
    # Make the string into a list of ints
    left, right = s.split(";")
    left = left.split(', ')
    right = [int(right)-1]
    lower_bounds = 0
    upper_bounds = PDF_Meta().pdf_length()+1
    left = list(set(string_elems_to_int_list(str_list=left, lb=lower_bounds, ub=upper_bounds)))
    Logger().print("[move_parser] String parsed into list of list[ints].")
    return [left, right]

def move_page(page_move_list:List[int]=None, target:int=None):
    Logger().print("[move_page] Moving pages inside the PDF...")
    # Prepping destination file
    tmp_pdf_path = tempfile.gettempdir() + "\\holder.pdf"
    prep_dest_file(tmp_pdf_path)
    pdf_length = PDF_Meta().pdf_length()
    PDF_Meta().close_pdf()

    # Target file path has to have already have been made!!!
    with open(PDF_Meta().get_file_path(), 'rb') as src_file, open(tmp_pdf_path, 'rb') as trg_file:
        # Inintiate Reader and Writer classes
        src_pdf = pypdf.PdfReader(src_file)
        trg_pdf = pypdf.PdfWriter(trg_file)
        
        # Create the new page order
        new_order = []
        new_order.extend(range(pdf_length))
        Logger().print(f"Old target: {target}")
        Logger().print(f"Old order: {new_order}")
        page_move_list =  [x - 1 for x in page_move_list]
        page_move_list_copy = page_move_list.copy()
        Logger().print(f"Move list: {page_move_list}")
        # Deleting pages that we need to 
        for i in range(len(page_move_list)):
            page_num = page_move_list.pop()
            if target > page_num:
                target = target-1
            new_order.pop(page_num)
        Logger().print(f"New target: {target}")
        new_order = new_order[:target] + page_move_list_copy + new_order[target:]
        Logger().print(f"New order: {new_order}")
        for page_num in new_order:
            page = src_pdf.pages[page_num]
            trg_pdf.add_page(page)

        # Save the modified target PDF
        with open(tmp_pdf_path, 'wb') as out_file:
            trg_pdf.write(out_file)
    # Source and target files have been closed
    # Remove original file
    remove_file(PDF_Meta().get_file_path())

    # Rename tmp file as main file
    rename_file(tmp_pdf_path, PDF_Meta().get_file_path())

    # Reconnect the original pdf
    PDF_Meta().reopen_pdf()
    Logger().print("[move_page] Pages moved inside the PDF.")

def ask_to_remove_pages_from_original():
    Logger().print("[ask_to_remove_pages_from_original] Asking if pages should be removed from the original PDF after splitting...")
    result = ""
    def on_yes():
        nonlocal result
        result = 1
        Logger().print("[ask_to_remove_pages_from_original] Pages will be removed.")
        dialog.destroy()  # Close the pop-up window

    def on_no():
        nonlocal result
        result = 0
        Logger().print("[ask_to_remove_pages_from_original] Pages won't be removed.")
        dialog.destroy()  # Close the pop-up window

    # Create a pop-up window
    dialog = tk.Toplevel()
    dialog.title("Confirmation")
    dialog.geometry("500x150")
    dialog.transient()  # Make it a child of the main window
    dialog.grab_set()   # Make it modal (block interaction with main window)
    
    # Add a label with the question
    tk.Label(dialog, text="Do you want to remove the pages being split off?", font=("Arial", 14)).pack(pady=20)

    # Add Yes and No buttons
    yes_button = tk.Button(dialog, text="Yes", font=("Arial", 14), width=10, command=on_yes)
    yes_button.pack(side="left", padx=40, pady=10)

    no_button = tk.Button(dialog, text="No", font=("Arial", 14), width=10, command=on_no)
    no_button.pack(side="right", padx=40, pady=10)

    dialog.wait_window()  # Wait for the dialog to close
    return result