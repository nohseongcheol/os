from polski import pozycja_wyjścia, zapis_Plik, 파일읽기, kodować_SMS, 글해독
dane = "PYTHON nazwa_pliku: polski 😀\n"
zapis_Plik("python.txt", kodować_SMS(dane))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == dane
pozycja_wyjścia(읽은글, 끝="")
