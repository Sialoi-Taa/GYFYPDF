# PDF Viewer & Editor
![Python](https://img.shields.io/badge/python-3.9%2B-blue)  ![License](https://img.shields.io/badge/license-MIT-green)  
An interactive PDF viewer and editor built with Python, Tkinter, and pypdfium2. Easily view, manipulate, and edit PDFs with a user-friendly GUI.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

## Features
- View and navigate multi-page PDFs with a scrollable GUI.
- Edit PDFs: merge, copy, split, delete, or move pages.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sialoi-Taa/GYFYPDF.git
   cd GYFYPDF
   ```


## Usage
### Running Through Executable
Go to the **dist** folder and you'll see the pdf_editor.exe file. You can use that exe file in 1 of 3 ways.  
1) First way is to right click a PDF, press "Open with", press "Choose another app", scroll down and press "Choose app on your PC", go to the directory with the exe file, select the exe file, press "Always use this app", and when you double click any PDF it'll run the custom exe file.  
2) Second way is to click and drag a PDF file to the exe file and it'll automatically open the app and run the script.  
3) Last way is to open the exe by itself and select the PDF file.  

### How To Use The PDF Editor
There's a few features that are highlighted in the PDF editor:
1. Saving
2. Merging
3. Copying
4. Deleting
5. Move
6. Split  

**Saving The PDF**  
To save, press the Save button on the button panel to the right of the PDF. Any modifications to the PDF without pressing the Save button will result in the PDF not being saved.  

**Merging PDFs**  
To merge PDFs, press the merge button and the file explorer will open. Choose the PDF you want to merge into the current PDF and the PDF you choose will be appended at the bottom.  

**Copying PDFs**  
To copy PDFs, press the copy button and a small window will pop up. This window will ask for a file name without the "." extension. This is asking what name you want the copy pdf to be, the .pdf extension will be added automatically. After submitting your desired new pdf copy's name, you'll then be asked for the folder you would like the file to be stored. Select the folder you want and the copy will be there.  

**Deleting Pages**  
To delete pages on your PDF, you need to type the pages you want deleted and then press the delete button. There are 2 types of inputs acceptable: singular pages and ranges of pages. While a singular page will target that specific page, a range of pages will select a group of pages in sequential order. Below is an example of a deletion input:
```bash
1, 2, 3-5, 9, 20, 13-16
```
In this example, each selection is separated by a comma and each selection is either selecting a single page or a group of pages. As shown above the targeted pages to delete are pages 1, 2, 9, 20 as well as pages 3 through 5 and 13 through 16. Also the order of deletion doesn't matter as you can delete page 9 and then page 3 without having any adverse or unexpected result happening on the PDF. If any accidents were to happen and the page is deleted, you can close the PDF editor and restart because as long as the Save button isn't pressed no changes will be written to the original PDF.  

**Moving Pages**  
To move pages from one place on the PDF to another, you will need to type in a valid input for moving pages and then press the move button. The format will be as such below:
```bash
target_pages;target_location
```
The target_pages will be the selection process the same as when deleting pages, followed by a semicolon (;) to separate the target location, and lastly closely following is the target location which will represent what page you would like all of the target_pages to move after to. An example would be below:
```bash
1, 2, 3-5, 9, 20, 13-16;10
```
In this example, pages 1, 2, 9, 20, 3 through 5, and 13 through 16 are to be selected and moved after page 10. What this will look like is that those pages in sequential order from least to greatest will be removed from the PDF and all inserted together at the target location or in this case page 10.  

**Splitting PDFs**  
To split a PDF into another PDF and section the original, you will need to type in a valid input for splitting the PDF and then press the split button. The format is as follows:
```bash
page_number
```
Where page_number is a single positive integer that represents how many pages you would like to keep in this PDF. An example would be putting 2 as an input and the expectation is to create a new PDF that will have everything except the first 2 pages of the original PDF this was splintered off from. After pressing the split button, you'll be prompted to give a name for the new PDF that will store the splitted contents. After submitting the name, you choose a folder to hold the PDF. Once the folder is selected, you will be prompted with a yes or no button window. This window is asking if you would like to remove the pages you are splitting off from the original PDF. Selecting yes would mean that only the page_number amount of pages will be left inside the PDF while selecting no will mean that the new PDF will be created but nothing will be deleted from the original PDF.  


## Acknowledgments
- [pypdfium2](https://github.com/pypdfium2/pypdfium2) for PDF rendering support.
- [Pillow](https://github.com/python-pillow/Pillow) for image handling.
- [pypdf](https://github.com/py-pdf/pypdf) for PDF editing support.
- [pyinstaller](https://pypi.org/project/pyinstaller) for creating the executable for portable use.
