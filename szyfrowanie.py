from szyfr import szyfrowanie, gen_key

if __name__ == "__main__":
    # zależnie czy szyfrujemy czy odszyfrowujemy trzeba zmienić nazwe pliku
    znaki = []
    with open("wej_bez_szyfr.txt") as inp:
        for line in inp:
            for char in line:
                if char not in znaki:
                    znaki.append(char)

    key = gen_key(len(znaki))
    print(key)
    szyfrowanie(znaki, "wej_bez_szyfr.txt", "wejscie_zaszyfr.txt", key)