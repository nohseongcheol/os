import Euskara

def 인사하기(Izena):
    인사말 = "안녕하세요 " + Izena
    Euskara.idatzi_fitxategi("인사.txt", 인사말)
    Euskara.Irteera(Euskara.글해독(Euskara.파일읽기("인사.txt")))

인사하기("누리")
