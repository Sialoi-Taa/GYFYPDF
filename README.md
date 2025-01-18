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
2. Run the package installation scripts to make sure you get all of the dependencies downloaded before running.
   ```bash
   python3 install_packages.py
   ```

## Usage
### Running Through Manual
Using this way you will have to run the editor through terminal every time. If you would like to be able to right click a PDF and choose to run the editor through the right-click menu, look at the registry edit method of running this application.   

1. Run the manual_view.py file:
   ```bash
   python3 manual_view.py
   ```
2. Choose a file to open.
![open_sample_file](/imgs/open_sample_file.png)
3. Using the buttons and text boxes on the right side of the editor, edit the PDF as you'd like.
![full layout](/imgs/fullscreen_layout.png)
4. When you're satisfied with what was editted, press the save button to save the PDF. If the editor closes before saving, all modifications will be erased and the user will be forced to start over.
![button layout](/imgs/button_layout.png)

### Running Through Registry Edit
Using this method you'll be able to right click any PDFs and have a more access friendly interface to run the script.  
![right_click](/imgs/right_click_menu_example.png)

1. Go to your Windows search bar and type below
   ```bash
   regedit
   ```
   You'll see a window as such below:  
![Registry Edit Base Menu](/imgs/base_regedit_menu.png)

2. Select and expand the *HKEY_CLASSES_ROOT* folder.  
![HKEY_CLASSES_ROOT](/imgs/HKEY_expanded.png)

3. Scroll down, select and expand the "*" folder.  
![pdf_folder](/imgs/all_folder_expanded.png)

4. Select and expand the *shell* folder.  
![expand_shell_folder](/imgs/shell_folder_expanded.png)

5. Select and right click the *shell* folder icon. Press "New" in the menu and then press "Key".  
![create_new_key](/imgs/create_new_key.png)  

6. A new folder will appear in the regedit window, name the folder "Open with PDF Editor".  
![context_key_created](/imgs/context_key_created.png)

7. Select the "Open with PDF Editor" folder and you'll a the variable on the right side. Double click that variable and a window will open.   
![point_to_default_value](/imgs/pointing_to_default_context_value.png)  

8. Press OK after changing the default value to "Open with PDF Editor" but without quotes and press OK.  
![change_context_value](/imgs/change_context_default_value.png)  

9. Select and right click the "Open with PDF Editor" folder icon. Make a new key and call it command.  
![create_command_key](/imgs/command_selected.png)  
Before moving onto the next step you have to find a 2 things. First you need the path to the where your python executable is located on your machine.  
   You can do this by typing the following:
   ```bash
   where python3
   ```  
   Store the outputted pathway somewhere, we'll need that for the next step. Next locate the *reg_view.py* file inside this repo.  
   Right click the file, copy the absolute path and store it somewhere for the next step. 

10. Select the command key and double click the default value. A menu to edit the value will open.  
![command_value_changed](/imgs/change_command_default_value.png)

11. Select the default value box and place 3 double quotes ("") with space inbetween them.  
![double quotes](/imgs/double_quote_data.png)  

12. In the first double quotes, place in the path for your *python3.exe* file. An example would be below:  
```bash
"C:\Users\joe\AppData\Local\Microsoft\WindowsApps\python3.exe"
```
![first_double](/imgs/python_path.png)

12. In the second double quotes, place in the path for your *reg_view.exe* file. An example would be below:  
```bash
"C:\Users\joe\OneDrive\Desktop\Custom_Utils\pdf_editor\reg_view.py"
```
![second_double](/imgs/reg_view_path.png)

12. In the third double quotes, place in "". An example would be below:  
```bash
"%1"
```

13. Altogether, the default value should look like this:
```bash
"C:\Users\joe\AppData\Local\Microsoft\WindowsApps\python3.exe" "C:\Users\joe\OneDrive\Desktop\Custom_Utils\pdf_editor\reg_view.py" "%1"
```

14. Press OK and exit out of the regedit.

15. The setup is complete and now this is how you can use the PDF Editor. Go to any PDF inside your file explorer and right click it.
16. Scroll down the menu and select "more options".
17. In that menu you'll see an option called "Open with PDF Editor". Click it and wait until the PDF editor opens up with your PDF.

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
- [pypdf](https://github.com/py-pdf/pypdf) for PDF editing support
