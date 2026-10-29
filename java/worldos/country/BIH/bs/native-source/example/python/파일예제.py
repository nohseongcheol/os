from 한국어 import Ispis, pisati_fajl, 파일읽기, 글부호화, 글해독
podaci = "PYTHON Fajl: bs 😀\n"
pisati_fajl("python.txt", 글부호화(podaci))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == podaci
Ispis(읽은글, 끝="")
