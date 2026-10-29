import Dansk

def 인사하기(Navn):
    인사말 = "안녕하세요 " + Navn
    Dansk.skrive_fil("인사.txt", 인사말)
    Dansk.Udgang(Dansk.글해독(Dansk.파일읽기("인사.txt")))

인사하기("누리")
