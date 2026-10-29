from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, mbyll_rrjet, 밀리초
from 한국어 import sistem_gabim, 다시시도오류, 글부호화, 명령인수, numër_i_plotë
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP sq")
    바깥전문보내기(종단, "10.0.2.2", numër_i_plotë(명령인수[1]), 전문)
    Ekzekuto = 밀리초()
    while True:
        try:
            replikë, portë_VALUE = 전문받기(종단)
            break
        except sistem_gabim as GABIM:
            if GABIM.INDEX != 다시시도오류 or 밀리초() - Ekzekuto >= 700:
                raise
    assert replikë == 전문
    출력("PYTHON 네트워크 verifikoj: UDP sq")
finally:
    mbyll_rrjet(종단)
