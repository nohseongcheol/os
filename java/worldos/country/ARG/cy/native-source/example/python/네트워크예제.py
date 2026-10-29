from Cymraeg import Allbwn, 전문통신열기, 바깥전문보내기, 전문받기, cau_Rhwydwaith, 밀리초
from Cymraeg import system_gwall, 다시시도오류, 글부호화, 명령인수, cyfanrif
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP cy")
    바깥전문보내기(종단, "10.0.2.2", cyfanrif(명령인수[1]), 전문)
    Gweithredu_2 = 밀리초()
    while True:
        try:
            ateb, porth_VALUE = 전문받기(종단)
            break
        except system_gwall as Gwall:
            if Gwall.INDEX != 다시시도오류 or 밀리초() - Gweithredu_2 >= 700:
                raise
    assert ateb == 전문
    Allbwn("PYTHON 네트워크 dilysu: UDP cy")
finally:
    cau_Rhwydwaith(종단)
