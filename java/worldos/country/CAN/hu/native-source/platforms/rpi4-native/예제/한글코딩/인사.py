import magyar

def 인사하기(Név):
    인사말 = "안녕하세요 " + Név
    magyar.ír_Fájl("인사.txt", 인사말)
    magyar.Kimenet(magyar.글해독(magyar.파일읽기("인사.txt")))

인사하기("누리")
