from math import log2
from functools import partial

LEN_OF_VALUE = 0

# 1 bajt - ile kolejnych bajtów przechowuje znaki
# x bajtów - znaki w pliku
# 1 bajt/pierwsze 3 bity - ile bitów nadmiarowych na końcu
# m bajtów - informacja skompresowana
# 1 bajt - ostatni to zera których nie uwzględniamy, po prostu żeby dopełnić

# nie uwzględniamy znaków nowej linii
# dobrze by było przechowywać do 8 znaków
# i wtedy jak osiągniemy bajt to wysyłamy do pliku i nie przechowujemy w pamięci

# nie wczytujemy do pamięci od razu 1tb pliku tylko częściami

def symbols_tab(in_file) -> list[chr]:
    """Returns sorted list of symbols in input file, without duplicates."""
    char_tab = []
    i = 0
    with open(in_file) as wej:
        for line in wej:
            line = line.strip()
            for char in line:
                i+=1
                if char not in char_tab:
                    char_tab.append(char)
    return i, sorted(char_tab)

def declare_symbols(char_tab):
    """First part of file with declared symbols."""
    char_tab = [bin(ord(char))[2:].zfill(8) for char in char_tab]
    char_string = "".join(char_tab)
    # ile kolejnych bajtów to symbole ascii
    lenght = bin(len(char_string)//8)[2:]
    str = (8-len(lenght))*'0' + lenght + char_string
    return str

def char_map(char_tab):
    """Maps each symbol in the file to number."""
    # char_number, char_tab = symbols_tab(in_file)
    log = log2(len(char_tab))
    global LEN_OF_VALUE
    LEN_OF_VALUE = log if isinstance(log, int) else int(log)+1
    next_numbers = list(range(len(char_tab)))
    for number in next_numbers:
        number = bin(number)
        # robimy mapę o dobrych dlugościach
        if LEN_OF_VALUE > len(number):
            number = '0'*(LEN_OF_VALUE - len(number)) + number

    return {char: number for char, number in zip(char_tab, next_numbers) }

def convert(text, char_map, out, left: str, add_end_bits: bool, end_bits: int):
    # with open(out_file, 'ab') as out:
    bajt = str(left)
    for char in text:
        bajt += str(bin(char_map[char]))[2:].zfill(LEN_OF_VALUE)
        while len(bajt)>=8:
            out.write(int(bajt[:8], 2).to_bytes(1, byteorder='big'))
            bajt = bajt[8:]
    if add_end_bits:
        bajt += (end_bits)*'0'
        out.write(int(bajt).to_bytes(1, byteorder='big'))
        return
    return bajt

def compress(in_file, out_file):
    char_number, char_tab = symbols_tab(in_file)
    chars = char_map(char_tab)

    end_bits = (char_number * LEN_OF_VALUE + 3) % 8 # dodajemy 3 bo to jest długość na której zapiszemy ile zbędnych bitów na koniec zostało dodanych
    symbols_header = declare_symbols(chars)
    left = bin(end_bits)[2:].zfill(3)

    with open(in_file,'r') as fin, open(out_file, 'w+b') as fout: 
        fout.write(symbols_header.encode('utf-8'))
        for line in iter(partial(fin.read, 1024), ''):
            if len(line) < 1024:
               left = convert(line,chars,fout,left,True,end_bits)
               return
            left = convert(line,chars,fout,left,False,end_bits)

if __name__=="__main__":
    compress('wej_bez_szyfr.txt', 'wyjscie_zaszyfr_skompresowane.txt')