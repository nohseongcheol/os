from norsk import Utgang, skrive_Fil, 파일읽기, 글부호화, 글해독
data = "PYTHON Fil: nb 😀\n"
skrive_Fil("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
Utgang(읽은글, 끝="")
