from 한국어 import Afvoer, skryf_lêer, 파일읽기, 글부호화, 글해독
data = "PYTHON Lêer: af 😀\n"
skryf_lêer("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
Afvoer(읽은글, 끝="")
