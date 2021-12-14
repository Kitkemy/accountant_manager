import sys
from manager import manager


file_name = sys.argv[1]
id_product = sys.argv[2:]

manager.read_input_data(file_name)
manager.execute()

print(manager.magazyn_dict)
for index in id_product:
    if not index in manager.magazyn_dict:
        print("{}: ilosc 0, cena 0".format(index))
    else:
        print("{}: ilosc {}, cena {}".format(index,
                                         manager.magazyn_dict[index]["ilosc"],
                                         manager.magazyn_dict[index]["cena"]))