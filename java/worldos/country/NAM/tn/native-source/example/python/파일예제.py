from 한국어 import 출력, kwala_faele, 파일읽기, 글부호화, 글해독
tshedimosetso = "PYTHON faele: tn 😀\n"
kwala_faele("python.txt", 글부호화(tshedimosetso))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == tshedimosetso
출력(읽은글, 끝="")
