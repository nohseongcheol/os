import Nederlands

def 인사하기(Naam):
    인사말 = "안녕하세요 " + Naam
    Nederlands.schrijven_Bestand("인사.txt", 인사말)
    Nederlands.tekstuitvoer(Nederlands.글해독(Nederlands.파일읽기("인사.txt")))

인사하기("누리")
