from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, bağlamaq_Şəbəkə, 밀리초
from 한국어 import sistem_səhv, 다시시도오류, 글부호화, 명령인수, tam_ədəd
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP Azerbaijani")
    바깥전문보내기(종단, "10.0.2.2", tam_ədəd(명령인수[1]), 전문)
    İcra_Et = 밀리초()
    while True:
        try:
            cavab, port_VALUE = 전문받기(종단)
            break
        except sistem_səhv as XƏTA:
            if XƏTA.INDEX != 다시시도오류 or 밀리초() - İcra_Et >= 700:
                raise
    assert cavab == 전문
    출력("PYTHON 네트워크 yoxlamaq: UDP Azerbaijani")
finally:
    bağlamaq_Şəbəkə(종단)
