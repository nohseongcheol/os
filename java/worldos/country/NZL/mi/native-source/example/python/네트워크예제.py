from Reo_Māori import 출력, 전문통신열기, 바깥전문보내기, 전문받기, kati_whatunga, 밀리초
from Reo_Māori import pūnaha_hapa, 다시시도오류, 글부호화, 명령인수, tau_tōpū
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP mi")
    바깥전문보내기(종단, "10.0.2.2", tau_tōpū(명령인수[1]), 전문)
    whakahaere = 밀리초()
    while True:
        try:
            whakautu, kawe_uara = 전문받기(종단)
            break
        except pūnaha_hapa as Pōhēhē:
            if Pōhēhē.INDEX != 다시시도오류 or 밀리초() - whakahaere >= 700:
                raise
    assert whakautu == 전문
    출력("PYTHON 네트워크 manatoko: UDP mi")
finally:
    kati_whatunga(종단)
