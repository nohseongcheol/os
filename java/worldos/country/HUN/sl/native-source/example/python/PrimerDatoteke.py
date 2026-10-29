from slovenščina import Izpis, pisati_Datoteka, 파일읽기, kodirati_SMS, 글해독
podatki = "PYTHON Datoteka: sl 😀\n"
pisati_Datoteka("python.txt", kodirati_SMS(podatki))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == podatki
Izpis(읽은글, 끝="")
