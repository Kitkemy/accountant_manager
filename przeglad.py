import sys
from manager import manager

file_name = sys.argv[1]

manager.read_input_data(file_name)
manager.execute()
print(manager.logs)