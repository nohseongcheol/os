from Latviešu import Izvade, rakstīšana_Fails, 파일읽기, kodēt_SMS, 글해독
dati = "PYTHON Fails: lv 😀\n"
rakstīšana_Fails("python.txt", kodēt_SMS(dati))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == dati
Izvade(읽은글, 끝="")
