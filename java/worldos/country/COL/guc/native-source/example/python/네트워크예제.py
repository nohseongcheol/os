from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, asürülaa_kusu, 밀리초
from 한국어 import a_yatawaajiraaya_ajachitia, 다시시도오류, 글부호화, 명령인수, waneepiasü
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP guc")
    바깥전문보내기(종단, "10.0.2.2", waneepiasü(명령인수[1]), 전문)
    시작 = 밀리초()
    while True:
        try:
            응답, outtülee_ajutuu = 전문받기(종단)
            break
        except a_yatawaajiraaya_ajachitia as ajachitia:
            if ajachitia.ee_iyatialujuna != 다시시도오류 or 밀리초() - 시작 >= 700:
                raise
    assert 응답 == 전문
    출력("PYTHON 네트워크 확인: UDP guc")
finally:
    asürülaa_kusu(종단)
