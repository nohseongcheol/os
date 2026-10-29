from magyar import Kimenet, ír_Fájl, 파일읽기, kódolás_SMS, 글해독
adat = "PYTHON Fájl: hu 😀\n"
ír_Fájl("python.txt", kódolás_SMS(adat))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == adat
Kimenet(읽은글, 끝="")
