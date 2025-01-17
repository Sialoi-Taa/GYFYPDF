from PDFlib.utils import *

print("Testing move input response validation")
s = "1-3, 5.0, 7; "
print(s)
print(f"{is_valid_move_string(s)}")
left, right = s.split(';')
left = left.split(', ')
print(left)
print(type(right))
print("Finished testing validation")