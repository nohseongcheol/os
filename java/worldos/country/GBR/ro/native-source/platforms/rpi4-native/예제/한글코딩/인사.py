import Română

def 인사하기(Nume):
    인사말 = "안녕하세요 " + Nume
    Română.scriere_Fișier("인사.txt", 인사말)
    Română.Rezultat(Română.글해독(Română.파일읽기("인사.txt")))

인사하기("누리")
