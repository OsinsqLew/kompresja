# opisać sposób szyfrowania
# kluczem jest ten wylosowany numer od któreo ucinamy printable ascii,
# kluczem jest też pozycja startowa (a w zasadzie data zaszyfrowania)

import string
from datetime import date
import random

"""Szyfruje kod na podstawie algorytmu .
Startowe współrzędne są brane na podstawie daty.
"""
def gen_key(len_wej: int):
    """Losujemy jakie znaki będą na wewnętrznym kole. A konkretniej pierwszy znak 
    i później będziemy brać kolejne n, gdzie n to jest liczba różnych symboli w tekście wejściowym"""
    # żeby nie wyjść poza tablice przy losowaniu n kolejnych znakow to musimy odjac długość wejścia (len_wej)
    return random.randint(1,len(string.printable)-len_wej) - 1

def dist(startowa: chr, szukana: chr, znaki: list[chr] ):
    i=0
    start_index = -1
    szuk_index = -1

    for znak in znaki:
        if znak == startowa:
            start_index = i
        if znak == szukana:
            szuk_index = i
        i+=1
    
    if start_index == -1 or szuk_index == -1:
        raise KeyError(f"Jednej z podanych nie ma w tablicy. - {startowa}, {szukana}")
    
    return szuk_index - start_index


def szyfrowanie(znaki: list[chr], inp_file, out_file, key: int):
    """Flow:
        1. deklarujemy dwie tablice
            1.2 Tablica znaków które mamy w pliku
            1.3 Tablica wszystkich znaków
        2. Deklarujemy wskaźniki na podstawie daty i robimy je mod liczba znaków jakie są
        3. Deklarujemy ich poruszanie
        4. Odczyt i Zapis do pliku
    """
    
    # wybieramy konkretny podzbiór o wielkości takiej jak liczba znaków w oryginalnym tekście
    # żeby nie zwiększać redundancji
    szyfr_symb = string.printable[key : key + len(znaki)]
    data = date.today()

    # wskazuje nm wtedy na konkretne stykające się litery
    #input pointer
    inp_pntr = (((data.day)*4) + data.year) % len(znaki)
    #output pointer
    out_pntr = (((data.month)*11) + data.year) % len(szyfr_symb)


    with open(inp_file, "r") as inp, open(out_file, "w") as out:
        for line in inp:
            tmp_str = ""
            for char in line:
                distance = dist(startowa=znaki[inp_pntr], szukana=char, znaki=znaki)
                szuk_pntr = (out_pntr + distance) % len(szyfr_symb)
                tmp_str += szyfr_symb[szuk_pntr]
                #po kazdym podstawieniu przeswamy
                out_pntr = (out_pntr + 1) % len(szyfr_symb)
            out.write(tmp_str)


def odszyfrowywanie(d: int, m: int, y: int, lista_wej: list[chr], inp_file, out_file, key: int ):
    szyfr_symb = string.printable[key: key + len(lista_wej)]
    data = date(y, m, d)
    # wskazuje nm wtedy na konkretne stykające się litery
    #input pointer
    inp_pntr = (((data.day)*4) + data.year) % len(lista_wej)
    #output pointer
    out_pntr = (((data.month)*11) + data.year) % len(szyfr_symb)

    with open(inp_file, "r") as inp, open(out_file, "w") as out:
        for line in inp:
            tmp_str = ""
            for char in line:
                distance = dist(startowa=szyfr_symb[out_pntr], szukana=char, znaki=szyfr_symb)
                szuk_pntr = (inp_pntr + distance) % len(lista_wej)
                tmp_str += lista_wej[szuk_pntr]
                #po kazdym podstawieniu przesuwamy
                out_pntr = (out_pntr + 1) % len(szyfr_symb)
            out.write(tmp_str)

if __name__ == "__main__":
    # zależnie czy szyfrujemy czy odszyfrowujemy trzeba zmienić nazwe pliku
    znaki = []
    with open("wej_bez_szyfr.txt") as inp:
        for line in inp:
            for char in line:
                if char not in znaki:
                    znaki.append(char)

    key = gen_key(len(znaki))
    szyfrowanie(znaki, "wej_bez_szyfr.txt", "wejscie_zaszyfr.txt", key)
    # Trzeba podać dzien miesiac rok w ktorym zostalo zaszyfrowane oraz klucz
    odszyfrowywanie(21,4,2024,znaki,"wejscie_zaszyfr.txt", "wyjscie_odszyfr.txt", key)


