import 한국어

def 인사하기(Ainm):
    인사말 = "안녕하세요 " + Ainm
    한국어.sgrìobh_faidhle("인사.txt", 인사말)
    한국어.출력(한국어.글해독(한국어.파일읽기("인사.txt")))

인사하기("누리")
