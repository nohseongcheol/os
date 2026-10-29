from 한국어 import Jessude, 파일쓰기, 파일읽기, 글부호화, 글해독
자료 = "PYTHON 파일: fur 😀\n"
파일쓰기("python.txt", 글부호화(자료))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == 자료
Jessude(읽은글, 끝="")
