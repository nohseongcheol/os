from 한국어 import 출력, sgrìobh_faidhle, 파일읽기, 글부호화, 글해독
dàta = "PYTHON faidhle: gd 😀\n"
sgrìobh_faidhle("python.txt", 글부호화(dàta))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == dàta
출력(읽은글, 끝="")
