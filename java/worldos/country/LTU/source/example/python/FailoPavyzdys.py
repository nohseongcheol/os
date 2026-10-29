from Lietuvių import Išvestis, rašymas_Failas, 파일읽기, koduoti_SMS, 글해독
duomenys = "PYTHON Failas: Lietuvių 😀\n"
rašymas_Failas("python.txt", koduoti_SMS(duomenys))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == duomenys
Išvestis(읽은글, 끝="")
