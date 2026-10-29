import slovenščina

def 인사하기(Ime):
    인사말 = "안녕하세요 " + Ime
    slovenščina.pisati_Datoteka("인사.txt", 인사말)
    slovenščina.Izpis(slovenščina.글해독(slovenščina.파일읽기("인사.txt")))

인사하기("누리")
