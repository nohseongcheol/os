import 한국어

def 인사하기(Numm):
    인사말 = "안녕하세요 " + Numm
    한국어.schreiwen_Fichier("인사.txt", 인사말)
    한국어.출력(한국어.글해독(한국어.파일읽기("인사.txt")))

인사하기("누리")
