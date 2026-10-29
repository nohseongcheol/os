from slovenščina import Izpis, odprto_datagram, poslati_zunanji_datagram, sprejeti_sprejemati_prejeti_prejemati_datagram, Zapri_mreža, 밀리초
from slovenščina import sistemska_napaka, 다시시도오류, kodirati_SMS, 명령인수, celo_število
končna_točka = odprto_datagram(0)
try:
    datagram = kodirati_SMS("PYTHON UDP slovenščina")
    poslati_zunanji_datagram(končna_točka, "10.0.2.2", celo_število(명령인수[1]), datagram)
    Zaženi = 밀리초()
    while True:
        try:
            odgovor, vrata_VALUE = sprejeti_sprejemati_prejeti_prejemati_datagram(končna_točka)
            break
        except sistemska_napaka as NAPAKA:
            if NAPAKA.INDEX != 다시시도오류 or 밀리초() - Zaženi >= 700:
                raise
    assert odgovor == datagram
    Izpis("PYTHON 네트워크 확인: UDP slovenščina")
finally:
    Zapri_mreža(končna_točka)
