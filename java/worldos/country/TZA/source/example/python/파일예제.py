from 한국어 import 출력, andika_faili, 파일읽기, 글부호화, 글해독
data = "PYTHON faili: Swahili (macrolanguage) 😀\n"
andika_faili("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
출력(읽은글, 끝="")
