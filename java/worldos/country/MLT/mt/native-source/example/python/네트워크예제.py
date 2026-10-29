from Malti import 출력, 전문통신열기, 바깥전문보내기, 전문받기, agħlaq_netwerk, 밀리초
from Malti import sistema_żball, 다시시도오류, 글부호화, 명령인수, numru_sħiħ
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP mt")
    바깥전문보내기(종단, "10.0.2.2", numru_sħiħ(명령인수[1]), 전문)
    serje = 밀리초()
    while True:
        try:
            wieġeb, port_VALUE = 전문받기(종단)
            break
        except sistema_żball as żball:
            if żball.INDEX != 다시시도오류 or 밀리초() - serje >= 700:
                raise
    assert wieġeb == 전문
    출력("PYTHON 네트워크 vverifika: UDP mt")
finally:
    agħlaq_netwerk(종단)
