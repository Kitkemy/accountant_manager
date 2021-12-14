import sys
from manager import manager

file_name = sys.argv[1]
id_product = sys.argv[2]
price = int(sys.argv[3])
ilosc_szt = int(sys.argv[4])

manager.read_input_data(file_name)
manager.execute()

log = f"Dokonano zakupu produktu: {id_product}, ilosc:" \
      f" {ilosc_szt}, w cenie za szt.  {price}."
paramert = ["zakup, {}, {}, {}".format(id_product,
                                    price, ilosc_szt, )]
manager.append_parametry(paramert)
manager.current_changes_purchases(id_product, price,
                                     ilosc_szt, log)
print(manager.parametry)
manager.save_parametry()
print(manager.logs)