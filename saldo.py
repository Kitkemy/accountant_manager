import sys
from manager import manager

file_name = sys.argv[1]
saldo_value = float(sys.argv[2])
saldo_comment = sys.argv[3]

manager.read_input_data(file_name)
manager.execute()

log = f"Zmiana saldo: {saldo_value} z komentarzem: {saldo_comment}."
manager.current_change(saldo_value, log)
paramert = ["saldo, {}, {}".format(saldo_value, saldo_comment)]
manager.append_parametry(paramert)
print(manager.parametry)
manager.save_parametry()