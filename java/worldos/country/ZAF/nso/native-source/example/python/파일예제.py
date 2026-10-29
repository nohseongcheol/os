from 한국어 import 출력, ngwala_faele, 파일읽기, 글부호화, 글해독
data = "PYTHON Faele: nso 😀\n"
ngwala_faele("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
출력(읽은글, 끝="")
