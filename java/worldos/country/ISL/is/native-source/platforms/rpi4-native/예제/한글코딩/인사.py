import Íslenska

def 인사하기(Heiti):
    인사말 = "안녕하세요 " + Heiti
    Íslenska.skrifa_skrá("인사.txt", 인사말)
    Íslenska.úttak(Íslenska.글해독(Íslenska.파일읽기("인사.txt")))

인사하기("누리")
