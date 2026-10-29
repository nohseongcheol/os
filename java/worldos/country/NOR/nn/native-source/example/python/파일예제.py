from 한국어 import Utdata, skrive_fil, 파일읽기, 글부호화, 글해독
data = "PYTHON Fil: nn 😀\n"
skrive_fil("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
Utdata(읽은글, 끝="")
