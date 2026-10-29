import 한국어

def 인사하기(Naziv):
    인사말 = "안녕하세요 " + Naziv
    한국어.pisati_fajl("인사.txt", 인사말)
    한국어.Ispis(한국어.글해독(한국어.파일읽기("인사.txt")))

인사하기("누리")
