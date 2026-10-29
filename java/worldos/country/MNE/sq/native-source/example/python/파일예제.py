from 한국어 import 출력, shkruaj_skedar, 파일읽기, 글부호화, 글해독
të_dhëna = "PYTHON Kartelë: sq 😀\n"
shkruaj_skedar("python.txt", 글부호화(të_dhëna))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == të_dhëna
출력(읽은글, 끝="")
