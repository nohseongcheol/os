import čeština

def 인사하기(Název):
    인사말 = "안녕하세요 " + Název
    čeština.zápis_Soubor("인사.txt", 인사말)
    čeština.výstupní_pozice(čeština.글해독(čeština.파일읽기("인사.txt")))

인사하기("누리")
