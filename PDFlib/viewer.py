from .renderer import Renderer
import tkinter as tk
import os
import pypdfium2 as pdfium
from .pdf_meta import PDF_Meta, TMP
from .utils import open_file, copy_pdf
from .logger import Logger

class PDF_Viewer:
    """Creates a PDF viewing/editing interface for the user"""
    def __init__(self, window:tk.Tk=None, file_path:str=None):
        Logger().print("[PDF_Viewer] Initiating PDF Viewer...")
        # Opens the target PDF and stores it as an object
        #self.file_path = open_file()
        self.file_path = file_path
        copy_pdf(self.file_path, TMP)
        #input(f"viewer1: {TMP}")
        self.pdf = pdfium.PdfDocument(TMP)
        #input("viewer1")
        self.pdf_meta = PDF_Meta()
        self.pdf_meta.set_data(pdf=self.pdf, file_path=self.file_path)

        # Renders the GUI
        self.renderer = Renderer(window)
        self.pdf_meta.setup_complete()
        self.renderer.update_image_labels()
        Logger().print("[PDF_Viewer] PDF Viewer initiation complete.")