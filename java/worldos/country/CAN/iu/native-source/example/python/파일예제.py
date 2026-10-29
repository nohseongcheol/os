from 한국어 import 출력, titiraq_ini, 파일읽기, 글부호화, 글해독
titiqqat = "PYTHON ini: iu 😀\n"
titiraq_ini("python.txt", 글부호화(titiqqat))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == titiqqat
출력(읽은글, 끝="")
