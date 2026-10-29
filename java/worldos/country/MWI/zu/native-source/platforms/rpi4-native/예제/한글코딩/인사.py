import Isi_Zulu

def 인사하기(Igama):
    인사말 = "안녕하세요 " + Igama
    Isi_Zulu.bhala_ifayela("인사.txt", 인사말)
    Isi_Zulu.출력(Isi_Zulu.글해독(Isi_Zulu.파일읽기("인사.txt")))

인사하기("누리")
