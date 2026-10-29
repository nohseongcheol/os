from Euskara import Irteera, idatzi_fitxategi, 파일읽기, 글부호화, 글해독
datuak = "PYTHON Fitxategia: eu 😀\n"
idatzi_fitxategi("python.txt", 글부호화(datuak))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == datuak
Irteera(읽은글, 끝="")
