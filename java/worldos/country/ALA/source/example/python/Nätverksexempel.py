from Svenska import utmatningsposition, skapa_datagram, skicka_extern_datagram, få_datagram, Stäng_nätverk, 밀리초
from Svenska import systemfel, 다시시도오류, koda_SMS, 명령인수, heltal
deltagare = skapa_datagram(0)
try:
    datagram = koda_SMS("PYTHON UDP Svenska")
    skicka_extern_datagram(deltagare, "10.0.2.2", heltal(명령인수[1]), datagram)
    Kör = 밀리초()
    while True:
        try:
            svara, port_värde = få_datagram(deltagare)
            break
        except systemfel as fel:
            if fel.INDEX != 다시시도오류 or 밀리초() - Kör >= 700:
                raise
    assert svara == datagram
    utmatningsposition("PYTHON 네트워크 verifiera: UDP Svenska")
finally:
    Stäng_nätverk(deltagare)
