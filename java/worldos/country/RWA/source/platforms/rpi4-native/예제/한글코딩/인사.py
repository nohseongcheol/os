import Ikinyarwanda

def 인사하기(Izina):
    인사말 = "안녕하세요 " + Izina
    Ikinyarwanda.kwandika_dosiye("인사.txt", 인사말)
    Ikinyarwanda.출력(Ikinyarwanda.글해독(Ikinyarwanda.파일읽기("인사.txt")))

인사하기("누리")
