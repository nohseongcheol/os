from Gaeilge import Aschur, scríobh_comhad, 파일읽기, 글부호화, 글해독
sonraí = "PYTHON Comhad: ga 😀\n"
scríobh_comhad("python.txt", 글부호화(sonraí))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == sonraí
Aschur(읽은글, 끝="")
