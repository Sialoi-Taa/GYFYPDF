import pypdfium2 as pdfium
from PDFlib.utils import *

print("Trying to split procedure")
# Copy the original pdf so the modification doesn't change the original
unmodified_pdf = "./Example_PDFS/CSE.pdf"
origin_pdf = "./Example_PDFS/CSE1.pdf"
copy_pdf(unmodified_pdf, origin_pdf)
# Second split the original pdf after the 2nd page
split_after_page = 2
dest_pdf = "./Example_PDFS/sample.pdf"
split_pdf(origin_pdf, split_after_page, dest_pdf)
# Remove the pages that come after split from the original pdf
pages_to_remove = []
pdf_document = pdfium.PdfDocument(origin_pdf)
pages_to_remove.extend(range(split_after_page, len(pdf_document)))
pdf_document.close()
print(pages_to_remove)
remove_pages(origin_pdf, pages_to_remove)
print("Finished with split procedure")