from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, tswala_Neteweke, 밀리초
from 한국어 import tsamaiso_phoso, 다시시도오류, 글부호화, 명령인수, Palotlalo
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP tn")
    바깥전문보내기(종단, "10.0.2.2", Palotlalo(명령인수[1]), 전문)
    dirisa = 밀리초()
    while True:
        try:
            araba, gorogisetsa_Boleng = 전문받기(종단)
            break
        except tsamaiso_phoso as phoso:
            if phoso.tshupane != 다시시도오류 or 밀리초() - dirisa >= 700:
                raise
    assert araba == 전문
    출력("PYTHON 네트워크 netefatsa: UDP tn")
finally:
    tswala_Neteweke(종단)
