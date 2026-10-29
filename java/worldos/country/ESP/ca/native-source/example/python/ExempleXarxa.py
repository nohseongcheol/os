from Català import Sortida, 전문통신열기, 바깥전문보내기, 전문받기, Tanca_xarxa, 밀리초
from Català import sistema_error, 다시시도오류, 글부호화, 명령인수, 정수
extrem = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP ca")
    바깥전문보내기(extrem, "10.0.2.2", 정수(명령인수[1]), 전문)
    Executa_2 = 밀리초()
    while True:
        try:
            resposta, port_VALOR = 전문받기(extrem)
            break
        except sistema_error as s_ha_produït_un_error:
            if s_ha_produït_un_error.INDEX != 다시시도오류 or 밀리초() - Executa_2 >= 700:
                raise
    assert resposta == 전문
    Sortida("PYTHON 네트워크 verificar: UDP ca")
finally:
    Tanca_xarxa(extrem)
