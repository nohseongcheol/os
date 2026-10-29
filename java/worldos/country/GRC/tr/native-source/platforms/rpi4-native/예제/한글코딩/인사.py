import Türkçe

def 인사하기(İsim):
    인사말 = "안녕하세요 " + İsim
    Türkçe.yazma_Dosya("인사.txt", 인사말)
    Türkçe.metinÇıktısı(Türkçe.글해독(Türkçe.파일읽기("인사.txt")))

인사하기("누리")
