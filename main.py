import sys

ALLOWED_ACTIONS = ("saldo", "sprzedaz", "zakup", "stop", "przegląd")


commands = sys.argv[1]
saldo = 0
magazyn_dict = {}
parametry = []
logs = []

with open("input_data") as input_:
    for line in input_.readlines():
        lines = line.split(",")
        action = lines[0]
        if not action in ALLOWED_ACTIONS:
            print("Niedozwolona komenda, podaj prawidlowa komende.")
            continue
        elif action == "stop":
            print("Zakonczyles prace systemu!")
            break
        elif action == "saldo":
            konto_zmiana_saldo = float(lines[1])
            zmiana_komentarz_saldo = lines[2].replace("\n", "")
            paratmert = ("Rodzaj akcji:{} "
                         "Wartosc zmiany na koncie (gr):{}. "
                         "Komentarz do zmiany: {}. ".
                         format(action, konto_zmiana_saldo,
                                zmiana_komentarz_saldo))
            parametry.append(paratmert)
            if (konto_zmiana_saldo) < 0 and (saldo + konto_zmiana_saldo) < 0:
                print("Podana wartosc przewyzsza saldo, wpisz wartosc ponownie.")
                continue
            saldo = saldo + konto_zmiana_saldo
            log = f"Zmiana saldo: {konto_zmiana_saldo} " \
                  f"z komentarzem: {zmiana_komentarz_saldo}."
            logs.append(log)
        elif action == "zakup":
            id_product_purchase = lines[1]
            price_purchase = float(lines[2])
            ilosc_szt_zakup = int(lines[3].replace(".\n", ""))
            paratmert = ("Rodzaj akcji: {} "
                         "id_product:{}. "
                         "Cene jednostkowa: {}. "
                         "Ilosc szt:{}".
                         format(action, id_product_purchase,
                                price_purchase, ilosc_szt_zakup))
            parametry.append(paratmert)
            wartosc_zakupu = ilosc_szt_zakup * price_purchase
            if wartosc_zakupu > saldo:
                print(f'Cena za towary ({wartosc_zakupu} '
                      f'przekracza wartosc salda {saldo}.)')
                continue
            else:
                saldo = saldo - wartosc_zakupu
                if not magazyn_dict.get(id_product_purchase):
                    magazyn_dict[id_product_purchase] = {
                        "ilosc": ilosc_szt_zakup, "cena": price_purchase
                    }
                else:
                    magazyn_ilosc_prod = magazyn_dict[id_product_purchase]["ilosc"]
                    magazyn_dict[id_product_purchase] = {
                        "ilosc": magazyn_ilosc_prod + ilosc_szt_zakup,
                        "cena": price_purchase
                    }
            log = f"Dokonano zakupu produktu {id_product_purchase}," \
                  f"ilosc {ilosc_szt_zakup} w cenie za szt.{price_purchase}."
            logs.append(log)
        elif action == "sprzedaz":
            id_product_sale = lines[1]
            price_sale = float(lines[2])
            ilosc_szt_sprzedaz = int(lines[3].replace("\n", ""))
            paratmert = ("Rodzaj akcji: {} "
                         "id_product:{}. "
                         "Cene jednostkowa: {}. "
                         "Ilosc szt:{}".
                         format(action, id_product_sale,
                                price_sale, ilosc_szt_sprzedaz))
            parametry.append(paratmert)
            wartosc_sprzedazy = price_sale * ilosc_szt_sprzedaz
            if not magazyn_dict.get(id_product_sale):
                print("Brak produktu na stanie magazynowym, podaj inny produkt")
                continue
            if magazyn_dict.get(id_product_sale)["ilosc"] < \
                    ilosc_szt_sprzedaz:
                print("Brak wystarczajace ilosci produktow, "
                      "wprowadz inna ilosc.")
                continue
            magazyn_ilosc_prod = \
                magazyn_dict[id_product_sale]["ilosc"]
            magazyn_dict[id_product_sale] = {
                "ilosc": magazyn_ilosc_prod - ilosc_szt_sprzedaz,
                "cena": price_sale
            }
            saldo = saldo + wartosc_sprzedazy
            if not magazyn_dict.get(id_product_sale)['ilosc']:
                del magazyn_dict[id_product_sale]
            log = f"Dokonano srzedazy produktu " \
                  f"{id_product_sale}," \
                  f"ilosc {ilosc_szt_sprzedaz} w cenie za szt." \
                  f"{price_sale}."
            logs.append(log)


if commands == "konto":
    print(f"Saldo:{saldo}")
    output = open("output_data", "w")
    output.write("Saldo: " + str(saldo))
    output.close()
elif commands == "magazyn":
    magazyn = (sys.argv[2:])
    ilosc = magazyn_dict.get("ilosc")
    cena = magazyn_dict.get("cena")
    print(ilosc)
    for i in magazyn:
        magazyn_dict[i] = {
            "ilosc": 0,
            "cena": 0
        }
    print(f"Stan magazynu:{magazyn_dict}")
    with open("output_data", "w") as file:
        for line, value in magazyn_dict.items():
            file.write(str(line) + str(value) + "\n")
elif commands == "przeglad":
    print(logs)
    with open("output_data", "w") as f:
        for item in logs:
            f.write("%s\n" % item)
elif commands == "saldo":
    wartosc_zmiany = int(sys.argv[2])
    komentarz = sys.argv[3]
    if (wartosc_zmiany) < 0 and (saldo + wartosc_zmiany) < 0:
        print("Podana wartosc przewyzsza saldo, wpisz wartosc ponownie.")
    saldo = saldo + wartosc_zmiany
    paratmert = ("Rodzaj akcji: {} "
                 "Wartosc zmiany na koncie (gr):{}. "
                 "Komentarz do zmiany: {}. ".
                 format(sys.argv[1], wartosc_zmiany, komentarz))
    with open("output_data", "w") as f:
        for item in parametry:
            f.write(str(item) + "\n")
elif commands == "sprzedaz":
    id_sale = sys.argv[2]
    cena_sprzedaz = int(sys.argv[3])
    ilosc_sprzedaz = int(sys.argv[4])
    paratmert = ("Rodzaj akcji: {} "
                 "id_product: {}. "
                 "Cene jednostkowa: {}. "
                 "Ilosc szt:{}".
                 format(sys.argv[1], id_sale,
                        cena_sprzedaz, ilosc_sprzedaz))
    parametry.append(paratmert)
    wartosc_sprzedazy_koniec = cena_sprzedaz * ilosc_sprzedaz
    if not magazyn_dict.get(id_sale) or \
            magazyn_dict.get(id_sale)["ilosc"] < ilosc_sprzedaz:
        print("Brak produktu na stanie lub niewystrczajaca ilosc produktow, "
              "aby dokonac sprzedazy.")
    magazyn_dict[id_sale] = {
        "ilosc": magazyn_ilosc_prod - ilosc_sprzedaz,
        "cena": cena_sprzedaz
    }
    saldo = saldo + wartosc_sprzedazy_koniec
    if not magazyn_dict.get(id_sale)['ilosc']:
        del magazyn_dict[id_sale]
    with open("output_data", "w") as f:
        for item in parametry:
            f.write(str(item) + "\n")

elif commands == "zakup":
    id_purchase = str(sys.argv[2])
    cena_zakup = int(sys.argv[3])
    ilosc_zakup = int(sys.argv[4])
    wartosc_zakupu_koniec = ilosc_zakup * cena_zakup
    paratmert = ("Rodzaj akcji: {} "
                 " id_product:{}. "
                 "Cene jednostkowa: {}. "
                 "Ilosc szt:{}".
                 format(sys.argv[1], id_purchase,
                        cena_zakup, ilosc_zakup))
    parametry.append(paratmert)
    if wartosc_zakupu_koniec > saldo:
        print(f'Cena za towary ({wartosc_zakupu_koniec} '
              f'przekracza wartosc salda {saldo}.)')
    else:
        saldo = saldo - wartosc_zakupu_koniec
    if not magazyn_dict.get(id_purchase):
        magazyn_dict[id_purchase] = {"ilosc": ilosc_zakup,
                                              "cena": cena_zakup}
    else:
        magazyn_ilosc_prod = magazyn_dict[id_purchase]["ilosc"]
        magazyn_dict[id_purchase] = {
            "ilosc": magazyn_ilosc_prod + ilosc_zakup,"cena": cena_zakup
        }
    with open("output_data", "w") as f:
        for item in parametry:
            f.write(str(item) + "\n")

for podane_parametry in enumerate(parametry):
    if commands in ALLOWED_ACTIONS:
        print(f"Podane parametry:{podane_parametry}")