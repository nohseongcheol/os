from Slovenský import Výstup, zapísať_Súbor, 파일읽기, kódovať_SMS, 글해독
údaje = "PYTHON Súbor: sk 😀\n"
zapísať_Súbor("python.txt", kódovať_SMS(údaje))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == údaje
Výstup(읽은글, 끝="")
