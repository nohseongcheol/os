from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, matuli_Kasuqatigiitsimajut, 밀리초
from 한국어 import qarasaujaq_tammarniq, 다시시도오류, 글부호화, 명령인수, naasaut
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP iu")
    바깥전문보내기(종단, "10.0.2.2", naasaut(명령인수[1]), 전문)
    시작 = 밀리초()
    while True:
        try:
            응답, kapputigaq_atuutilik = 전문받기(종단)
            break
        except qarasaujaq_tammarniq as tammarniq:
            if tammarniq.nalunaiqsimavik != 다시시도오류 or 밀리초() - 시작 >= 700:
                raise
    assert 응답 == 전문
    출력("PYTHON 네트워크 nalunairli_1aacb54c: UDP iu")
finally:
    matuli_Kasuqatigiitsimajut(종단)
