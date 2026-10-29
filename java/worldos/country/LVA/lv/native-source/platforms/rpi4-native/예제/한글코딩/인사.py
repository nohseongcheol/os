import Latviešu

def 인사하기(Nosaukums):
    인사말 = "안녕하세요 " + Nosaukums
    Latviešu.rakstīšana_Fails("인사.txt", 인사말)
    Latviešu.Izvade(Latviešu.글해독(Latviešu.파일읽기("인사.txt")))

인사하기("누리")
