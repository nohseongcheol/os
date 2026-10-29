from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, yopmoq_Tarmoq, 밀리초
from 한국어 import tizim_xato, 다시시도오류, 글부호화, 명령인수, butun_son
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP Uzbek")
    바깥전문보내기(종단, "10.0.2.2", butun_son(명령인수[1]), 전문)
    Bajarish = 밀리초()
    while True:
        try:
            javob_berish, port_VALUE = 전문받기(종단)
            break
        except tizim_xato as Xato:
            if Xato.INDEX != 다시시도오류 or 밀리초() - Bajarish >= 700:
                raise
    assert javob_berish == 전문
    출력("PYTHON 네트워크 tasdiqlamoq: UDP Uzbek")
finally:
    yopmoq_Tarmoq(종단)
