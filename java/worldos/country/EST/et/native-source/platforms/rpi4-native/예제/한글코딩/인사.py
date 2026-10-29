import Eesti

def 인사하기(Nimi_2):
    인사말 = "안녕하세요 " + Nimi_2
    Eesti.kirjutamine_Fail("인사.txt", 인사말)
    Eesti.Väljund(Eesti.글해독(Eesti.파일읽기("인사.txt")))

인사하기("누리")
