import Cymraeg

def 인사하기(Enw):
    인사말 = "안녕하세요 " + Enw
    Cymraeg.ysgrifennu_ffeil("인사.txt", 인사말)
    Cymraeg.Allbwn(Cymraeg.글해독(Cymraeg.파일읽기("인사.txt")))

인사하기("누리")
