import Lietuvių

def 인사하기(Pavadinimas_2):
    인사말 = "안녕하세요 " + Pavadinimas_2
    Lietuvių.rašymas_Failas("인사.txt", 인사말)
    Lietuvių.Išvestis(Lietuvių.글해독(Lietuvių.파일읽기("인사.txt")))

인사하기("누리")
