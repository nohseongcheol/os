from 한국어 import Afvoer, 전문통신열기, 바깥전문보내기, 전문받기, sluit_Netwerk, 밀리초
from 한국어 import stelsel_fout, 다시시도오류, 글부호화, 명령인수, heelgetal
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP af")
    바깥전문보내기(종단, "10.0.2.2", heelgetal(명령인수[1]), 전문)
    Loop = 밀리초()
    while True:
        try:
            antwoord, ombou_VALUE = 전문받기(종단)
            break
        except stelsel_fout as Fout:
            if Fout.INDEX != 다시시도오류 or 밀리초() - Loop >= 700:
                raise
    assert antwoord == 전문
    Afvoer("PYTHON 네트워크 verifieer: UDP af")
finally:
    sluit_Netwerk(종단)
