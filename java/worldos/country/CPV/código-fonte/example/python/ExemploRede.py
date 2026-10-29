from Português import saídaTexto, abrir_datagrama, enviar_externo_datagrama, receber_datagrama, Close_rede, 밀리초
from Português import erro_do_sistema, 다시시도오류, codificar_SMS, 명령인수, inteiro
empresa = abrir_datagrama(0)
try:
    datagrama = codificar_SMS("PYTHON UDP Português")
    enviar_externo_datagrama(empresa, "10.0.2.2", inteiro(명령인수[1]), datagrama)
    iniciar = 밀리초()
    while True:
        try:
            resposta, porta_VALOR = receber_datagrama(empresa)
            break
        except erro_do_sistema as erro:
            if erro.ÍNDICE != 다시시도오류 or 밀리초() - iniciar >= 700:
                raise
    assert resposta == datagrama
    saídaTexto("PYTHON 네트워크 verificar: UDP Português")
finally:
    Close_rede(empresa)
