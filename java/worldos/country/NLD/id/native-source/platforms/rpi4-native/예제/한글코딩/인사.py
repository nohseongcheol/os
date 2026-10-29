import Indonesia

def 인사하기(Nama_2):
    인사말 = "안녕하세요 " + Nama_2
    Indonesia.tulis_file("인사.txt", 인사말)
    Indonesia.keluaranTeks(Indonesia.글해독(Indonesia.파일읽기("인사.txt")))

인사하기("누리")
