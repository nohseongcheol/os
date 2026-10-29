from Italiano import uscitaTesto, scrivere_File, 파일읽기, codificare_SMS, 글해독
dati = "PYTHON file: Italiano 😀\n"
scrivere_File("python.txt", codificare_SMS(dati))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == dati
uscitaTesto(읽은글, 끝="")
