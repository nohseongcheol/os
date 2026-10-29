from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, funga_Mtandao, 밀리초
from 한국어 import mfumo_kosa, 다시시도오류, 글부호화, 명령인수, namba_kamili
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP sw")
    바깥전문보내기(종단, "10.0.2.2", namba_kamili(명령인수[1]), 전문)
    endesha = 밀리초()
    while True:
        try:
            jibu, kituo_thamani = 전문받기(종단)
            break
        except mfumo_kosa as kosa:
            if kosa.kielezo != 다시시도오류 or 밀리초() - endesha >= 700:
                raise
    assert jibu == 전문
    출력("PYTHON 네트워크 thibitisha: UDP sw")
finally:
    funga_Mtandao(종단)
