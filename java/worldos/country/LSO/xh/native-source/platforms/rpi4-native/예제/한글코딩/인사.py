import isiXhosa

def 인사하기(Igama):
    인사말 = "안녕하세요 " + Igama
    isiXhosa.bhala_ifayile("인사.txt", 인사말)
    isiXhosa.출력(isiXhosa.글해독(isiXhosa.파일읽기("인사.txt")))

인사하기("누리")
