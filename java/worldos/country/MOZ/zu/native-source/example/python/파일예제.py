from Isi_Zulu import 출력, bhala_ifayela, 파일읽기, 글부호화, 글해독
imininingwane = "PYTHON Ihele: zu 😀\n"
bhala_ifayela("python.txt", 글부호화(imininingwane))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == imininingwane
출력(읽은글, 끝="")
