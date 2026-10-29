from 한국어 import 출력, kọ_fáìlì, 파일읽기, 글부호화, 글해독
détà = "PYTHON Fáìlì: yo 😀\n"
kọ_fáìlì("python.txt", 글부호화(détà))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == détà
출력(읽은글, 끝="")
