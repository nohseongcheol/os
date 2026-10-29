import Melayu

def 인사하기(Nama):
    인사말 = "안녕하세요 " + Nama
    Melayu.tulis_fail("인사.txt", 인사말)
    Melayu.출력(Melayu.글해독(Melayu.파일읽기("인사.txt")))

인사하기("누리")
