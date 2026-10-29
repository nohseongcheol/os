from Gaeilge import Aschur, 전문통신열기, 바깥전문보내기, 전문받기, dún_Líonra, 밀리초
from Gaeilge import córas_earráid, 다시시도오류, 글부호화, 명령인수, slánuimhir
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP ga")
    바깥전문보내기(종단, "10.0.2.2", slánuimhir(명령인수[1]), 전문)
    Rith_2 = 밀리초()
    while True:
        try:
            freagair, port_VALUE = 전문받기(종단)
            break
        except córas_earráid as ERREÁID:
            if ERREÁID.INDEX != 다시시도오류 or 밀리초() - Rith_2 >= 700:
                raise
    assert freagair == 전문
    Aschur("PYTHON 네트워크 fíoraigh: UDP ga")
finally:
    dún_Líonra(종단)
