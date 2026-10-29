from 한국어 import 출력, 파일쓰기, 파일읽기, kodirati_SMS, 글해독
podaci = "PYTHON Datoteka: српски 😀\n"
파일쓰기("python.txt", kodirati_SMS(podaci))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == podaci
출력(읽은글, 끝="")
