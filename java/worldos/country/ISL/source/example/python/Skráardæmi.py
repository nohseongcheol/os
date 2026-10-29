from Íslenska import úttak, skrifa_skrá, 파일읽기, 글부호화, 글해독
gögn = "PYTHON Skrá: Íslenska 😀\n"
skrifa_skrá("python.txt", 글부호화(gögn))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == gögn
úttak(읽은글, 끝="")
