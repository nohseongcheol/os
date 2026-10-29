from 한국어 import 출력, ýaz_faýl, 파일읽기, 글부호화, 글해독
maglumat = "PYTHON Faýl: Turkmen 😀\n"
ýaz_faýl("python.txt", 글부호화(maglumat))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == maglumat
출력(읽은글, 끝="")
