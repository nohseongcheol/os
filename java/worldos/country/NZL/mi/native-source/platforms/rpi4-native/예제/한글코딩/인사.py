import Reo_Māori

def 인사하기(Ingoa):
    인사말 = "안녕하세요 " + Ingoa
    Reo_Māori.tuhi_kōnae("인사.txt", 인사말)
    Reo_Māori.출력(Reo_Māori.글해독(Reo_Māori.파일읽기("인사.txt")))

인사하기("누리")
