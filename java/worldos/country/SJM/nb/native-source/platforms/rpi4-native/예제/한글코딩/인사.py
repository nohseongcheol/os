import norsk

def 인사하기(Navn):
    인사말 = "안녕하세요 " + Navn
    norsk.skrive_Fil("인사.txt", 인사말)
    norsk.Utgang(norsk.글해독(norsk.파일읽기("인사.txt")))

인사하기("누리")
