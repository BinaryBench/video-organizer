import os
import itertools
from mylib import *

source_dir = os.getcwd()

changes = {}

for name in os.listdir(source_dir):
    new_dir = reformat(name)

    if new_dir is None or new_dir == name:
        continue

    changes[name] = new_dir

if changes:

    for key in iter(changes):
        print(key + " > " + changes[key])

    change = query_yes_no("Rename files?")

    if change:
        for key in iter(changes):
            os.rename(key, changes[key])

else:
    print("No changes needed :)\n")
    input("Press ENTER to close...")
