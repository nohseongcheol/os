from isiXhosa import 출력, bhala_ifayile, 파일읽기, 글부호화, 글해독
iingcombolo = "PYTHON iFayili: xh 😀\n"
bhala_ifayile("python.txt", 글부호화(iingcombolo))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == iingcombolo
출력(읽은글, 끝="")
