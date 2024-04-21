from szyfr import odszyfrowywanie

if __name__ == "__main__":
    # zależnie czy szyfrujemy czy odszyfrowujemy trzeba zmienić nazwe pliku
    znaki = []
    with open("wej_bez_szyfr.txt") as inp:
        for line in inp:
            for char in line:
                if char not in znaki:
                    znaki.append(char)
    print(znaki)

    # Trzeba podać dzien miesiac rok w ktorym zostalo zaszyfrowane, klucz oraz zewnętrzne koło
    odszyfrowywanie(21,4,2024,znaki,"wejscie_zaszyfr.txt", "wyjscie_odszyfr.txt", 72)