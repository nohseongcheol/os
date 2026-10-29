import suomi

def 인사하기(Nimi):
    인사말 = "안녕하세요 " + Nimi
    suomi.kirjoitus_Tiedosto("인사.txt", 인사말)
    suomi.tulostuspaikka(suomi.글해독(suomi.lukea_Tiedosto("인사.txt")))

인사하기("누리")
