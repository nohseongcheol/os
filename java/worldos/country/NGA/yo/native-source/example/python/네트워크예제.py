from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, pa_dé_Alásopọ̀, 밀리초
from 한국어 import ètò_àṣìṣe, 다시시도오류, 글부호화, 명령인수, nọ́ńbà_odindi
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP yo")
    바깥전문보내기(종단, "10.0.2.2", nọ́ńbà_odindi(명령인수[1]), 전문)
    Rọ́ọ̀nù = 밀리초()
    while True:
        try:
            Fèsì, ojú_iye = 전문받기(종단)
            break
        except ètò_àṣìṣe as àṣìṣe:
            if àṣìṣe.wá_atọ̀ka_àkóónú != 다시시도오류 or 밀리초() - Rọ́ọ̀nù >= 700:
                raise
    assert Fèsì == 전문
    출력("PYTHON 네트워크 ridájú: UDP yo")
finally:
    pa_dé_Alásopọ̀(종단)
