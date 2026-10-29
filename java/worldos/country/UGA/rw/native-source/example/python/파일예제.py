from Ikinyarwanda import 출력, kwandika_dosiye, 파일읽기, 글부호화, 글해독
amakurushingiro = "PYTHON Idosiye: rw 😀\n"
kwandika_dosiye("python.txt", 글부호화(amakurushingiro))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == amakurushingiro
출력(읽은글, 끝="")
