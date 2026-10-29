from 한국어 import 출력, schreiwen_Fichier, 파일읽기, 글부호화, 글해독
Daten = "PYTHON Fichier: lb 😀\n"
schreiwen_Fichier("python.txt", 글부호화(Daten))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == Daten
출력(읽은글, 끝="")
