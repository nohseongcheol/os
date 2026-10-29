from 한국어 import Sortida, 전문통신열기, 바깥전문보내기, 전문받기, 통신닫기, 밀리초
from 한국어 import 운영체제오류, 다시시도오류, 글부호화, 명령인수, 정수
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP oc")
    바깥전문보내기(종단, "10.0.2.2", 정수(명령인수[1]), 전문)
    Executar_2 = 밀리초()
    while True:
        try:
            응답, 창구 = 전문받기(종단)
            break
        except 운영체제오류 as 오류:
            if 오류.번호 != 다시시도오류 or 밀리초() - Executar_2 >= 700:
                raise
    assert 응답 == 전문
    Sortida("PYTHON 네트워크 확인: UDP oc")
finally:
    통신닫기(종단)
