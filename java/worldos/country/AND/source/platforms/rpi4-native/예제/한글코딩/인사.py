import Català

def 인사하기(Nom):
    인사말 = "안녕하세요 " + Nom
    Català.escriure_arxiu("인사.txt", 인사말)
    Català.Sortida(Català.글해독(Català.tancar_arxiu("인사.txt")))

인사하기("누리")
