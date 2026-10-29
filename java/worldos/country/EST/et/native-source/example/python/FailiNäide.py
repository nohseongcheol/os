from Eesti import Väljund, kirjutamine_Fail, 파일읽기, kodeerima_SMS, 글해독
andmed = "PYTHON Fail: et 😀\n"
kirjutamine_Fail("python.txt", kodeerima_SMS(andmed))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == andmed
Väljund(읽은글, 끝="")
