import Malti

def 인사하기(isem):
    인사말 = "안녕하세요 " + isem
    Malti.kiteb_fajl("인사.txt", 인사말)
    Malti.출력(Malti.글해독(Malti.파일읽기("인사.txt")))

인사하기("누리")
