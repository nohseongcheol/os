import Svenska

def 인사하기(Namn):
    인사말 = "안녕하세요 " + Namn
    Svenska.skriva_fil("인사.txt", 인사말)
    Svenska.utmatningsposition(Svenska.글해독(Svenska.läsa_fil("인사.txt")))

인사하기("누리")
