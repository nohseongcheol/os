from Isi_Zulu import 출력, 전문통신열기, 바깥전문보내기, 전문받기, vala_iNethiwekhi, 밀리초
from Isi_Zulu import isistimu_iphutha, 다시시도오류, 글부호화, 명령인수, inamba
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP zu")
    바깥전문보내기(종단, "10.0.2.2", inamba(명령인수[1]), 전문)
    Sebenzisa = 밀리초()
    while True:
        try:
            phendula, intuba_inani = 전문받기(종단)
            break
        except isistimu_iphutha as Iphutha:
            if Iphutha.thola_inkomba != 다시시도오류 or 밀리초() - Sebenzisa >= 700:
                raise
    assert phendula == 전문
    출력("PYTHON 네트워크 qiniseka: UDP zu")
finally:
    vala_iNethiwekhi(종단)
