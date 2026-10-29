from Slovenský import Výstup, otvoriť_datagram, odoslať_externý_datagram, dostať_datagram, Zavrieť_sieť, 밀리초
from Slovenský import systém_Chyba, 다시시도오류, kódovať_SMS, 명령인수, celé_číslo
účastník = otvoriť_datagram(0)
try:
    datagram = kódovať_SMS("PYTHON UDP Slovenský")
    odoslať_externý_datagram(účastník, "10.0.2.2", celé_číslo(명령인수[1]), datagram)
    Spustiť_2 = 밀리초()
    while True:
        try:
            odozva, port_VALUE = dostať_datagram(účastník)
            break
        except systém_Chyba as chyba:
            if chyba.INDEX != 다시시도오류 or 밀리초() - Spustiť_2 >= 700:
                raise
    assert odozva == datagram
    Výstup("PYTHON 네트워크 overiť: UDP Slovenský")
finally:
    Zavrieť_sieť(účastník)
