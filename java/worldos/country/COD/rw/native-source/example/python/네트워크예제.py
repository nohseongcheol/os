from Ikinyarwanda import 출력, 전문통신열기, 바깥전문보내기, 전문받기, gufunga_Urusobemiyoboro, 밀리초
from Ikinyarwanda import sisitemu_ikosa, 다시시도오류, 글부호화, 명령인수, umubare_wuzuye
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP rw")
    바깥전문보내기(종단, "10.0.2.2", umubare_wuzuye(명령인수[1]), 전문)
    ihuriro = 밀리초()
    while True:
        try:
            gusubiza, poti_agaciro = 전문받기(종단)
            break
        except sisitemu_ikosa as IKOSA:
            if IKOSA.umugerekashakiro != 다시시도오류 or 밀리초() - ihuriro >= 700:
                raise
    assert gusubiza == 전문
    출력("PYTHON 네트워크 gusuzuma: UDP rw")
finally:
    gufunga_Urusobemiyoboro(종단)
