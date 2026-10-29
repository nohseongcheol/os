from 한국어 import 출력, dee_ọbọakwụkwọ, 파일읽기, 글부호화, 글해독
datà = "PYTHON Faịlụ: ig 😀\n"
dee_ọbọakwụkwọ("python.txt", 글부호화(datà))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == datà
출력(읽은글, 끝="")
