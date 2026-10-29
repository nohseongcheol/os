from Nederlands import tekstuitvoer, schrijven_Bestand, 파일읽기, coderen_sms, 글해독
gegevens = "PYTHON bestand: nl 😀\n"
schrijven_Bestand("python.txt", coderen_sms(gegevens))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == gegevens
tekstuitvoer(읽은글, 끝="")
