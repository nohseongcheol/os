from čeština import výstupní_pozice, zápis_Soubor, 파일읽기, kódovat_SMS, 글해독
data = "PYTHON název_souboru: čeština 😀\n"
zápis_Soubor("python.txt", kódovat_SMS(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
výstupní_pozice(읽은글, 끝="")
