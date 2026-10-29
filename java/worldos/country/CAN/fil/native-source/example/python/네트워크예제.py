from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, isara_Network, 밀리초
from 한국어 import system_error, 다시시도오류, 글부호화, 명령인수, integer_buong_numero
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP fil")
    바깥전문보내기(종단, "10.0.2.2", integer_buong_numero(명령인수[1]), 전문)
    run = 밀리초()
    while True:
        try:
            tumugon, port_VALUE = 전문받기(종단)
            break
        except system_error as error:
            if error.INDEX != 다시시도오류 or 밀리초() - run >= 700:
                raise
    assert tumugon == 전문
    출력("PYTHON 네트워크 tiyakin_kumpirmahin: UDP fil")
finally:
    isara_Network(종단)
