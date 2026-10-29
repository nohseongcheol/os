import Slovenský

def 인사하기(Názov):
    인사말 = "안녕하세요 " + Názov
    Slovenský.zapísať_Súbor("인사.txt", 인사말)
    Slovenský.Výstup(Slovenský.글해독(Slovenský.파일읽기("인사.txt")))

인사하기("누리")
