from 한국어 import 출력, ashajaa_anaajaalaa, 파일읽기, 글부호화, 글해독
atijaaya = "PYTHON anaajaalaa: guc 😀\n"
ashajaa_anaajaalaa("python.txt", 글부호화(atijaaya))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == atijaaya
출력(읽은글, 끝="")
