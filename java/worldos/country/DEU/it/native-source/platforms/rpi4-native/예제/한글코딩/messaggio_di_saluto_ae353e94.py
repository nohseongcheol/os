import Italiano

def 인사하기(Nome):
    messaggio_di_saluto = "안녕하세요 " + Nome
    Italiano.scrivere_File("messaggio_di_saluto_ae353e94.txt", messaggio_di_saluto)
    Italiano.uscitaTesto(Italiano.글해독(Italiano.파일읽기("messaggio_di_saluto_ae353e94.txt")))

인사하기("누리")
