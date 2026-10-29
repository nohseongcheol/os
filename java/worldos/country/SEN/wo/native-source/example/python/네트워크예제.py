from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, Tej_mbaal, 밀리초
from 한국어 import kureel_njumte, 다시시도오류, 글부호화, 명령인수, lëmm
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP wo")
    바깥전문보내기(종단, "10.0.2.2", lëmm(명령인수[1]), 전문)
    daw = 밀리초()
    while True:
        try:
            tontu, jël_xëyma = 전문받기(종단)
            break
        except kureel_njumte as njumte:
            if njumte.àlluwa_tur != 다시시도오류 or 밀리초() - daw >= 700:
                raise
    assert tontu == 전문
    출력("PYTHON 네트워크 luñutu: UDP wo")
finally:
    Tej_mbaal(종단)
