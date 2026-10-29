from 한국어 import 출력, yazmaq_fayl, 파일읽기, 글부호화, 글해독
verilənlər = "PYTHON FAYL: az 😀\n"
yazmaq_fayl("python.txt", 글부호화(verilənlər))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == verilənlər
출력(읽은글, 끝="")
