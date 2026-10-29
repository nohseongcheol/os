from Dansk import Udgang, skrive_fil, 파일읽기, kode_sms, 글해독
data = "PYTHON Fil: Dansk 😀\n"
skrive_fil("python.txt", kode_sms(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
Udgang(읽은글, 끝="")
