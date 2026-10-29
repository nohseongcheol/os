from hrvatski import Izlaz, zapisivanje_Datoteka, 파일읽기, kodirati_SMS, 글해독
podaci = "PYTHON Datoteka: hr 😀\n"
zapisivanje_Datoteka("python.txt", kodirati_SMS(podaci))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == podaci
Izlaz(읽은글, 끝="")
