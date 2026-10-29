import Galego

def 인사하기(Nome):
    인사말 = "안녕하세요 " + Nome
    Galego.escribir_Ficheiro("인사.txt", 인사말)
    Galego.Saída(Galego.글해독(Galego.파일읽기("인사.txt")))

인사하기("누리")
