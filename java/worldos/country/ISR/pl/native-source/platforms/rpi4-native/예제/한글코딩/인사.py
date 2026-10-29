import polski

def 인사하기(Nazwa):
    인사말 = "안녕하세요 " + Nazwa
    polski.zapis_Plik("인사.txt", 인사말)
    polski.pozycja_wyjścia(polski.글해독(polski.파일읽기("인사.txt")))

인사하기("누리")
