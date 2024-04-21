from functools import partial
from math import log2

def decompress(inp_file, out_file):
    symb_list = []

    with open(inp_file, 'rb') as fin:
        # ktory bajt przeczytalo
        i = 0
        with open(out_file, 'w') as fout:
            # ile bajtów zajmują symbole
            symbols_lenght = int(fin.read(8), 2)
            # sym_lenght mówi ile będzie symboli i na tej podstawie obliczamy długość pojedynczego znaku
            log = log2(symbols_lenght)
            len_for_symb = log if isinstance(log, int) else int(log) + 1 # * ile bitów będzie zajmował poj znak

            #declared symbols
            symbols_str = fin.read(symbols_lenght*8)

            for i in range(symbols_lenght):
                # * czytamy po znaku zapisanym binarnie w ascii i dodajemy go do listy symboli
                symbol = int(symbols_str[i*8:(i+1)*8], 2)
                symb_list.append(chr(symbol))

            end_bits = int(fin.read(3),2)

            for line in iter(partial(fin.read, 1024), b''):

                if len(line) < 1024:
                    line = str(line)
                    line = line[2:-end_bits+1]
                else:
                    line = line[2:-1]

                for i in range(int(len(line)/len_for_symb)):
                    start = len_for_symb*i
                    end = start + len_for_symb
                    tmp_int = int(line[start:end], 2)
                    symbol = symb_list[tmp_int]
                    fout.write(symbol)

if __name__ == "__main__":
    decompress("wyjscie_zaszyfr_skompresowane.txt", "wyjscie_zaszyfr.txt")