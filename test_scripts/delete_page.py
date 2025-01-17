from PDFlib.utils import *

print("Trying to delete certain pages")

# Create the split
origin_split_pdf_path = open_file()
dest_split_pdf_path = open_file()
part = 3
split_pdf(origin_split_pdf_path, part, dest_split_pdf_path)
# Delete page 2
pdf_delete_path = open_file()
page_to_delete = 2
remove_pages(pdf_delete_path, [page_to_delete])

print("Finished deleting pages")