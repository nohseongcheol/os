import Gaeilge

def 인사하기(Ainm):
    인사말 = "안녕하세요 " + Ainm
    Gaeilge.scríobh_comhad("인사.txt", 인사말)
    Gaeilge.Aschur(Gaeilge.글해독(Gaeilge.파일읽기("인사.txt")))

인사하기("누리")
