import Português

def 인사하기(Nome):
    saudação = "안녕하세요 " + Nome
    Português.gravar_Arquivo("saudação_ae353e94.txt", saudação)
    Português.saídaTexto(Português.글해독(Português.leitura_Arquivo("saudação_ae353e94.txt")))

인사하기("누리")
