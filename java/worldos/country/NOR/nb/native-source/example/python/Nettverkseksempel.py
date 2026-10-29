from norsk import Utgang, åpen_datagram, sende_ekstern_datagram, motta_datagram, Lukk_nettverk, 밀리초
from norsk import systemfeil, 다시시도오류, 글부호화, 명령인수, heltall
deltaker = åpen_datagram(0)
try:
    datagram = 글부호화("PYTHON UDP nb")
    sende_ekstern_datagram(deltaker, "10.0.2.2", heltall(명령인수[1]), datagram)
    Kjør_2 = 밀리초()
    while True:
        try:
            svar, port_VERDI = motta_datagram(deltaker)
            break
        except systemfeil as feil:
            if feil.INDEKS != 다시시도오류 or 밀리초() - Kjør_2 >= 700:
                raise
    assert svar == datagram
    Utgang("PYTHON 네트워크 bekrefte: UDP nb")
finally:
    Lukk_nettverk(deltaker)
