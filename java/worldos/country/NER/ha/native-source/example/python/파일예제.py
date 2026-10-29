from 한국어 import 출력, Rubuta_Fayil, 파일읽기, 글부호화, 글해독
Tarin_bayani = "PYTHON Fayil: ha 😀\n"
Rubuta_Fayil("python.txt", 글부호화(Tarin_bayani))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == Tarin_bayani
출력(읽은글, 끝="")
