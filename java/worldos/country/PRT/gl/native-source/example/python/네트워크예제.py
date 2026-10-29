from Galego import Saída, 전문통신열기, 바깥전문보내기, 전문받기, peche_Rede, 밀리초
from Galego import sistema_erro, 다시시도오류, 글부호화, 명령인수, número_enteiro
extremo = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP gl")
    바깥전문보내기(extremo, "10.0.2.2", número_enteiro(명령인수[1]), 전문)
    Executar_2 = 밀리초()
    while True:
        try:
            resposta, porto_VALOR = 전문받기(extremo)
            break
        except sistema_erro as ERRO:
            if ERRO.ÍNDICE != 다시시도오류 or 밀리초() - Executar_2 >= 700:
                raise
    assert resposta == 전문
    Saída("PYTHON 네트워크 verificar: UDP gl")
finally:
    peche_Rede(extremo)
