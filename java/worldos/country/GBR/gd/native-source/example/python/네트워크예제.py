from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, dùin_lìonra, 밀리초
from 한국어 import siostam_mearachd, 다시시도오류, 글부호화, 명령인수, àireamh_shlàn
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP gd")
    바깥전문보내기(종단, "10.0.2.2", àireamh_shlàn(명령인수[1]), 전문)
    ruith = 밀리초()
    while True:
        try:
            freagair, port_VALUE = 전문받기(종단)
            break
        except siostam_mearachd as Mearachd:
            if Mearachd.INDEX != 다시시도오류 or 밀리초() - ruith >= 700:
                raise
    assert freagair == 전문
    출력("PYTHON 네트워크 dearbh: UDP gd")
finally:
    dùin_lìonra(종단)
