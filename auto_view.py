'''
Requires:
pip3 install PyMuPDF pillow
Windows 

Purpose:
My version of a Windows PDF viewer and editor.

Features:
1) Deleting certain pages
2) Saving current iteration
3) Merging PDFs
4) Spliting PDFs
5) Moving pages to other places through text commands

Completed:

'''
import tkinter as tk
from PDFlib.viewer import PDF_Viewer
from PDFlib.utils import *
import sys, os
from PDFlib.logger import Logger

def main(file_path:str=None):
    root = tk.Tk()
    PDF_Viewer(window=root, file_path=file_path)
    root.mainloop()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    logs_dir = os.path.join(script_dir, "logs")
    log_path = os.path.join(logs_dir, "log.txt")
    Logger().set_log_location(log_path)
    
    # Check if the script was run with a file argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]  # This will be the file path passed from the registry
        if os.path.exists(file_path) and file_path.lower().endswith('.pdf'):
            Logger().print(f"Opening PDF: {file_path}")
            main(file_path=file_path)
            # You can now use the file_path to open and edit the PDF
        else:
            Logger().print("Invalid file path or not a PDF file.")
    else:
        Logger().print("No file path provided.")
    