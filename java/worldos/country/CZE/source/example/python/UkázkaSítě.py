from čeština import výstupní_pozice, otevřít_datagram, poslat_externí_datagram, dostat_datagram, Zavřít_síť, 밀리초
from čeština import chyba_systému, 다시시도오류, kódovat_SMS, 명령인수, integer
účastník = otevřít_datagram(0)
try:
    datagram = kódovat_SMS("PYTHON UDP čeština")
    poslat_externí_datagram(účastník, "10.0.2.2", integer(명령인수[1]), datagram)
    Spustit_2 = 밀리초()
    while True:
        try:
            odezva, port_HODNOTA = dostat_datagram(účastník)
            break
        except chyba_systému as chyba:
            if chyba.INDEX != 다시시도오류 or 밀리초() - Spustit_2 >= 700:
                raise
    assert odezva == datagram
    výstupní_pozice("PYTHON 네트워크 ověřit: UDP čeština")
finally:
    Zavřít_síť(účastník)
