from 한국어 import Eligo, 파일쓰기, 파일읽기, 글부호화, 글해독
자료 = "PYTHON Dosiero: eo 😀\n"
파일쓰기("python.txt", 글부호화(자료))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == 자료
Eligo(읽은글, 끝="")
