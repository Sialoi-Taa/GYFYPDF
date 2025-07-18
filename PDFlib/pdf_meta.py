from .command import Command
from typing import List, Set
import pypdfium2 as pdfium
import tempfile
from .logger import Logger

TMP = tempfile.gettempdir() + "\\tmp.pdf"

class PDF_Meta:
    _instance = None
    _data = {"pdf":pdfium.PdfDocument, 
             "file_path":str, 
             "unsaved_changes":[], 
             "last_saved_pdf":[],
             "setup_complete":bool}  # Persistent storage for data

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            Logger().print("[PDF_Meta] Initiating PDF_Meta...")
            cls._instance = super().__new__(cls)
            Logger().print("[PDF_Meta] PDF_Meta completed.")
        return cls._instance

    def set_data(self, pdf, file_path):
        """Set the data that will persist between calls."""
        Logger().print("[PDF_Meta] Setting PDF meta data...")
        self._data["pdf"] = pdf
        self._data["file_path"] = file_path
        self._data["setup_complete"] = False
        Logger().print("[PDF_Meta] PDF meta data set.")
    
    def is_setup_complete(self):
        Logger().print("[PDF_Meta] Returning if setup is complete.")
        return self._data["setup_complete"]
    
    def setup_complete(self):
        Logger().print("[PDF_Meta] Setup complete.")
        self._data["setup_complete"] = True

    def append(self, command:Command=None):
        self._data["unsaved_changes"].append(command)
    def pop(self):
        self._data["unsaved_changes"].pop()

    def save(self):
        Logger().print("\n[PDF_Meta] Saving PDF...")
        # Saves the modified version to the original file
        self._data["pdf"].save(self._data["file_path"])
        self._data["unsaved_changes"] = []
        Logger().print("[PDF_Meta] PDF saved.")
    
    def get_save_file_path(self):
        Logger().print("[PDF_Meta] Return save file pathway.")
        return self._data["file_path"]

    def get_data(self):
        """Retrieve the persisted data."""
        Logger().print("[PDF_Meta] Returning PDF meta data.")
        return self._data
    
    def get_pdf(self):
        Logger().print("[PDF_Meta] Returning PDF data.")
        return self._data["pdf"]
    
    def get_file_path(self):
        Logger().print("[PDF_Meta] Returning PDF file location.")
        return TMP
    
    def reopen_pdf(self):
        Logger().print("[PDF_Meta] Opening PDF...")
        self._data["pdf"] = pdfium.PdfDocument(TMP)
        Logger().print("[PDF_Meta] PDF opened.")
    
    def close_pdf(self):
        Logger().print("[PDF_Meta] Close PDF...")
        self._data["pdf"].close()
        Logger().print("[PDF_Meta] PDF closed.")

    def pdf_length(self):
        Logger().print("[PDF_Meta] Returning PDF length.")
        return len(self._data["pdf"])

    def remove_pages(self, pages_to_remove:Set[int]=None):
        Logger().print("[PDF_Meta] Removing pages from PDF...")
        
        if self.pdf_length() == 1 or self.pdf_length() <= len(pages_to_remove):
            Logger().print("[PDF_Meta] No pages were removed due to removing more pages than allowed.")
            return None
        
        from .utils import remove_file, rename_file, prep_dest_file
        # Get current PDF and file path
        pdf = self._data["pdf"]
        origin_file_path = self.get_file_path()
        
        # Iterate over all the pages, excluding the one to be removed
        while len(pages_to_remove):
            pdf.del_page(pages_to_remove.pop()-1)
            
        # Write the new pdf version to a new pdf
        dest_pdf_path = tempfile.gettempdir() + "\\holder.pdf"
        prep_dest_file(dest_pdf_path)
        pdf.save(dest_pdf_path)
        
        # Close the pdf
        pdf.close()

        # Delete the original pdf file
        remove_file(origin_file_path)

        # Rename new pdf to the old pdf name
        rename_file(dest_pdf_path, origin_file_path)

        # Reopen the PDF before leaving function
        self.reopen_pdf()
        Logger().print("[PDF_Meta] Pages removed from PDF.")
