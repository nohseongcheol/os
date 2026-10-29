from Galego import Saída, escribir_Ficheiro, 파일읽기, 글부호화, 글해독
datos = "PYTHON Ficheiro: gl 😀\n"
escribir_Ficheiro("python.txt", 글부호화(datos))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == datos
Saída(읽은글, 끝="")
