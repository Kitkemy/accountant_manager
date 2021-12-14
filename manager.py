class Manager:

    def __init__(self):
        self.saldo = 0
        self.magazyn_dict = {}
        self.logs = []
        self.parametry = []
        self.cb = {}

    def read_input_data(self, file_path='input_data.txt'):
        with open(file_path) as file:
            for line in file.readlines():
                lines = line.split(",")
                lines = [x.strip() for x in lines]
                self.parametry.append(lines)

    def current_change(self, wartosc_zmiany, log):
        if wartosc_zmiany < 0 and wartosc_zmiany + self.saldo < 0:
            print("Niewystarczajace srodki!")
        else:
            self.saldo += wartosc_zmiany
            self.logs.append(log)

    def current_changes_purchases(self, index, price, number, log):
        wartosc_zakupu_koniec = number * price
        if wartosc_zakupu_koniec > self.saldo:
            print(f'Cena za towary ({wartosc_zakupu_koniec} '
                  f'przekracza wartosc salda {self.saldo}.)')
        else:
            self.saldo = self.saldo - wartosc_zakupu_koniec
            if not self.magazyn_dict.get(index):
                self.magazyn_dict[index] = {
                    "ilosc": number, "cena": price
                }
            else:
                magazyn_ilosc_prod = \
                    self.magazyn_dict[index]["ilosc"]
                self.magazyn_dict[index] = {
                    "ilosc": magazyn_ilosc_prod + number, "cena": price
                }
            self.logs.append(log)

    def current_changes_sales(self, index, price, number, log):
        wartosc_zmiany = price * number
        if not self.magazyn_dict.get(index):
            print("Brak produktu na stanie magazynowym, podaj inny produkt")
        else:
            if self.magazyn_dict.get(index)["ilosc"] < number:
                print("Brak wystarczajace ilosci produktow, "
                  "wprowadz inna ilosc.")
            magazyn_ilosc_prod = \
                self.magazyn_dict[index]["ilosc"]
            self.magazyn_dict[index] = {
                "ilosc": magazyn_ilosc_prod - number,
                "cena": price
            }
            self.saldo = self.saldo + wartosc_zmiany
            self.logs.append(log)
            if not self.magazyn_dict.get(index)['ilosc']:
                del self.magazyn_dict[index]

    def append_parametry(self, parametr):
        self.parametry.append(parametr)

    def save_parametry(self):
        with open("output_data", "w") as file:
            for item in self.parametry:
                file.write(str(item) + "\n")

    def assign(self, mode):
        def inner(func):    
            self.cb[mode] = func
        return inner

    def execute(self):
        for i in self.parametry:
            mode = i[0]
            if mode in self.cb:
                self.cb[mode](i[1:])
            elif mode == 'stop':
                print('Zakonczyles prace programu.')
            else:
                print(f'{mode} - nieobslugiwany rodzaj akcji.')
            

manager = Manager()

@manager.assign(mode='saldo')
def update_saldo(i):
    saldo_change = float(i[0])
    comment = i[1].replace("\n", "")
    log = f"Zmiana salda: {saldo_change} " \
            f"z komentarzem: {comment}."
    manager.current_change(saldo_change, log)

@manager.assign(mode='zakup')
def make_purchases(i):
        id_product_zakup = i[0]
        price_purchase = int(i[1])
        ilosc_szt_zakup = int(i[2])
        log = f"Dokonano zakupu produktu {id_product_zakup}," \
                f"ilosc {ilosc_szt_zakup} w cenie za szt.{price_purchase}."
        manager.current_changes_purchases(id_product_zakup,
                                        price_purchase,
                                        ilosc_szt_zakup,
                                        log)

@manager.assign(mode='sprzedaz')
def make_sales(i): 
        id_product_sprzedaz = i[0]
        price_sale = float(i[1])
        ilosc_szt_sprzedaz = int(i[2])
        log = f"Dokonano srzedazy " \
                f"produktu {id_product_sprzedaz}," \
                f"ilosc {ilosc_szt_sprzedaz} w cenie za szt. " \
                f"{price_sale}."
        manager.current_changes_sales(id_product_sprzedaz,
                                    price_sale,
                                    ilosc_szt_sprzedaz,
                                    log)