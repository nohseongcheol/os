from Indonesia import keluaranTeks, tulis_file, 파일읽기, 글부호화, 글해독
data = "PYTHON berkas: Indonesian 😀\n"
tulis_file("python.txt", 글부호화(data))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == data
keluaranTeks(읽은글, 끝="")
