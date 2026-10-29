from Euskara import Irteera, 전문통신열기, 바깥전문보내기, 전문받기, itxi_sare, 밀리초
from Euskara import sistema_errore, 다시시도오류, 글부호화, 명령인수, osoko_zenbaki
amaiera_puntu = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP eu")
    바깥전문보내기(amaiera_puntu, "10.0.2.2", osoko_zenbaki(명령인수[1]), 전문)
    Exekutatu_2 = 밀리초()
    while True:
        try:
            erantzun, ataka_balio = 전문받기(amaiera_puntu)
            break
        except sistema_errore as errorea:
            if errorea.INDIZE != 다시시도오류 or 밀리초() - Exekutatu_2 >= 700:
                raise
    assert erantzun == 전문
    Irteera("PYTHON 네트워크 egiaztatu: UDP eu")
finally:
    itxi_sare(amaiera_puntu)
