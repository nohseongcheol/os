from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, Rufe_Hanyar_sadarwa, 밀리초
from 한국어 import na_ura_Kuskure, 다시시도오류, 글부호화, 명령인수, Lamba_mara
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP ha")
    바깥전문보내기(종단, "10.0.2.2", Lamba_mara(명령인수[1]), 전문)
    Tafiyar_da = 밀리초()
    while True:
        try:
            mayar_da_martani, fot_Daraja = 전문받기(종단)
            break
        except na_ura_Kuskure as Kuskure:
            if Kuskure.Indes != 다시시도오류 or 밀리초() - Tafiyar_da >= 700:
                raise
    assert mayar_da_martani == 전문
    출력("PYTHON 네트워크 Tabbatar_da: UDP ha")
finally:
    Rufe_Hanyar_sadarwa(종단)
