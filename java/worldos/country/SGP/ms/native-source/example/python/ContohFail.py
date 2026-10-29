from Melayu import 출력, tulis_fail, 파일읽기, 글부호화, 글해독
data = "PYTHON Fail: ms 😀\n"
tulis_fail("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
출력(읽은글, 끝="")
