from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, Clôture_Reseau, 밀리초
from 한국어 import System_Feeler, 다시시도오류, 글부호화, 명령인수, Ganzzuel
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP lb")
    바깥전문보내기(종단, "10.0.2.2", Ganzzuel(명령인수[1]), 전문)
    Laf = 밀리초()
    while True:
        try:
            äntweren, Port_VALUE = 전문받기(종단)
            break
        except System_Feeler as Feeler:
            if Feeler.INDEX != 다시시도오류 or 밀리초() - Laf >= 700:
                raise
    assert äntweren == 전문
    출력("PYTHON 네트워크 verifizéieren: UDP lb")
finally:
    Clôture_Reseau(종단)
