import hrvatski

def 인사하기(Ime):
    인사말 = "안녕하세요 " + Ime
    hrvatski.zapisivanje_Datoteka("인사.txt", 인사말)
    hrvatski.Izlaz(hrvatski.글해독(hrvatski.파일읽기("인사.txt")))

인사하기("누리")
