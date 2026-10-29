from Reo_Māori import 출력, tuhi_kōnae, 파일읽기, 글부호화, 글해독
raraunga = "PYTHON Kōnae: mi 😀\n"
tuhi_kōnae("python.txt", 글부호화(raraunga))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == raraunga
출력(읽은글, 끝="")
