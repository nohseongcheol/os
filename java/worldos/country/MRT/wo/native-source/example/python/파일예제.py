from 한국어 import 출력, biir_bara_denc, 파일읽기, 글부호화, 글해독
mbir = "PYTHON bara_denc: wo 😀\n"
biir_bara_denc("python.txt", 글부호화(mbir))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == mbir
출력(읽은글, 끝="")
