from 한국어 import 출력, otvoren_datagram, poslati_spoljni_datagram, primiti_datagram, Zatvori_Mreža, 밀리초
from 한국어 import sistem_greška, 다시시도오류, kodirati_SMS, 명령인수, ceo_broj
učesnik = otvoren_datagram(0)
try:
    datagram = kodirati_SMS("PYTHON UDP српски")
    poslati_spoljni_datagram(učesnik, "10.0.2.2", ceo_broj(명령인수[1]), datagram)
    koristiti = 밀리초()
    while True:
        try:
            odgovor, port_VALUE = primiti_datagram(učesnik)
            break
        except sistem_greška as greška:
            if greška.INDEX != 다시시도오류 or 밀리초() - koristiti >= 700:
                raise
    assert odgovor == datagram
    출력("PYTHON 네트워크 verifikovati: UDP српски")
finally:
    Zatvori_Mreža(učesnik)
