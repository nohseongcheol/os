from 한국어 import Utdata, 전문통신열기, 바깥전문보내기, 전문받기, Lukk_Nettverk, 밀리초
from 한국어 import system_feil, 다시시도오류, 글부호화, 명령인수, heiltal
endepunkt = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP nn")
    바깥전문보내기(endepunkt, "10.0.2.2", heiltal(명령인수[1]), 전문)
    Køyr_2 = 밀리초()
    while True:
        try:
            svare, port_VALUE = 전문받기(endepunkt)
            break
        except system_feil as FEIL:
            if FEIL.INDEX != 다시시도오류 or 밀리초() - Køyr_2 >= 700:
                raise
    assert svare == 전문
    Utdata("PYTHON 네트워크 stadfeste: UDP nn")
finally:
    Lukk_Nettverk(endepunkt)
