from Cymraeg import Allbwn, ysgrifennu_ffeil, 파일읽기, 글부호화, 글해독
data = "PYTHON Ffeil: cy 😀\n"
ysgrifennu_ffeil("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
Allbwn(읽은글, 끝="")
