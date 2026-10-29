from Malti import 출력, kiteb_fajl, 파일읽기, 글부호화, 글해독
data = "PYTHON fajl: Malti 😀\n"
kiteb_fajl("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
출력(읽은글, 끝="")
