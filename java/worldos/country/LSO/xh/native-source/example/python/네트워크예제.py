from isiXhosa import 출력, 전문통신열기, 바깥전문보내기, 전문받기, vala_Inethiwekhi, 밀리초
from isiXhosa import inkqubo_impazamo, 다시시도오류, 글부호화, 명령인수, inani_elipheleleyo
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP xh")
    바깥전문보내기(종단, "10.0.2.2", inani_elipheleleyo(명령인수[1]), 전문)
    Phumeza = 밀리초()
    while True:
        try:
            phendula, iphothi_ixabiso = 전문받기(종단)
            break
        except inkqubo_impazamo as Impazamo:
            if Impazamo.indeksa != 다시시도오류 or 밀리초() - Phumeza >= 700:
                raise
    assert phendula == 전문
    출력("PYTHON 네트워크 ngqinisisa: UDP xh")
finally:
    vala_Inethiwekhi(종단)
