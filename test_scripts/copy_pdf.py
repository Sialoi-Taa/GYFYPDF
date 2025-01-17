import sys
import os

# Step 1: Get the absolute path to the 'PDFLib' directory in the root of your project
# This should go one level up from 'test_scripts/PDFLib' and then into the root 'PDFLib' folder
pdf_lib_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
print(f"PDFLib path: {pdf_lib_path}")

# Step 2: Add this path to sys.path
sys.path.append(pdf_lib_path)

# Step 3: Verify if it's correctly added
print("sys.path:", sys.path)

# Step 4: Try importing the module from the 'PDFLib' directory
try:
    from PDFlib.utils import *  # Replace with your actual module name
    print("Module imported successfully.")
except ImportError as e:
    print(f"Error importing module: {e}")


print("Trying to copy a pdf")
name = ask_file_name()
dir = ask_for_directory()
print(f"{dir} + {name}")
#copy_pdf(unmodified_pdf, origin_pdf)
print("Finished with copying a pdf")