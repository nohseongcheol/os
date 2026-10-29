from Română import Rezultat, scriere_Fișier, 파일읽기, codifica_SMS, 글해독
date = "PYTHON Fișier: Română 😀\n"
scriere_Fișier("python.txt", codifica_SMS(date))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == date
Rezultat(읽은글, 끝="")
