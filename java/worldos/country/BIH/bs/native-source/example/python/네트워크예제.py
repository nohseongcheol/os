from 한국어 import Ispis, 전문통신열기, 바깥전문보내기, 전문받기, zatvoriti_Mreža, 밀리초
from 한국어 import sistem_greška, 다시시도오류, 글부호화, 명령인수, cijeli_broj
završna_tačka = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP bs")
    바깥전문보내기(završna_tačka, "10.0.2.2", cijeli_broj(명령인수[1]), 전문)
    Pokreni = 밀리초()
    while True:
        try:
            odgovoriti, port_VALUE = 전문받기(završna_tačka)
            break
        except sistem_greška as GRESKA:
            if GRESKA.INDEX != 다시시도오류 or 밀리초() - Pokreni >= 700:
                raise
    assert odgovoriti == 전문
    Ispis("PYTHON 네트워크 potvrditi: UDP bs")
finally:
    zatvoriti_Mreža(završna_tačka)
