import sys
from manager import manager

file_name = sys.argv[1]

manager.read_input_data(file_name)
manager.execute()
print(f'Stan konta po wszystkich operacjach wynosi - {manager.saldo} PLN')