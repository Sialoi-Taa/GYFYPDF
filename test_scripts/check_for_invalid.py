from PDFlib.utils import *

print("Checking for invalid characters")
s = "10-"
left, right = s.split('-')
print(f"{left} {type(left)}, {right} {type(right)}")
s = "1, 10, 2.4, -3, 2, 3-5"
res = is_valid_deletion_string(s)
print(f"Is the string valid? {res}")
s = "1, 10-5, 3, 7, 8-13"
page_nums = re.findall(r'-?\d+\.?\d*(?:-\d+)?', s)
print(f"Page Nums: {page_nums}")
page_nums = del_str_list_to_int_list(page_nums)
print(f"Selection Page Nums: {page_nums}")
print("Finished with checking for invalid characters")