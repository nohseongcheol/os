from Dansk import Udgang, åben_datagram, maile_ekstern_datagram, modtage_datagram, Luk_netværk, 밀리초
from Dansk import systemfejl, 다시시도오류, kode_sms, 명령인수, heltal
slutpunkt = åben_datagram(0)
try:
    datagram = kode_sms("PYTHON UDP Dansk")
    maile_ekstern_datagram(slutpunkt, "10.0.2.2", heltal(명령인수[1]), datagram)
    Kør_2 = 밀리초()
    while True:
        try:
            svar, port_VÆRDI = modtage_datagram(slutpunkt)
            break
        except systemfejl as fejl:
            if fejl.INDEKS != 다시시도오류 or 밀리초() - Kør_2 >= 700:
                raise
    assert svar == datagram
    Udgang("PYTHON 네트워크 bekræfte: UDP Dansk")
finally:
    Luk_netværk(slutpunkt)
