from 한국어 import 출력, winndude_fiilde, 파일읽기, 글부호화, 글해독
keɓe = "PYTHON fiilde: ff 😀\n"
winndude_fiilde("python.txt", 글부호화(keɓe))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == keɓe
출력(읽은글, 끝="")
