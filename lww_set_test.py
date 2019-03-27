""" IMPORT LIBRARIES """
from lww_set_class import LWW_Set

new_set = LWW_Set()
new_set.add("test")
print(new_set.get())
new_set.add("another")
print(new_set.get())
new_set.add("test")
print(new_set.get())
new_set.remove("another")
print(new_set.get())
new_set.remove("test")
print(new_set.get())