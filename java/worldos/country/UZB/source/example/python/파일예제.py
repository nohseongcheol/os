from 한국어 import 출력, yozmoq_fayl, 파일읽기, 글부호화, 글해독
ma_lumotlar = "PYTHON Fayl: Uzbek 😀\n"
yozmoq_fayl("python.txt", 글부호화(ma_lumotlar))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == ma_lumotlar
출력(읽은글, 끝="")
