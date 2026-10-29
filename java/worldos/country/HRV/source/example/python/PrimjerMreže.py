from hrvatski import Izlaz, otvoreno_datogram, slati_vanjski_datogram, primiti_datogram, Zatvori_mreža, 밀리초
from hrvatski import sustav_pogreška, 다시시도오류, kodirati_SMS, 명령인수, cijeli_broj
sudionik = otvoreno_datogram(0)
try:
    datogram = kodirati_SMS("PYTHON UDP hrvatski")
    slati_vanjski_datogram(sudionik, "10.0.2.2", cijeli_broj(명령인수[1]), datogram)
    Pokreni = 밀리초()
    while True:
        try:
            odgovor, prebaciti_VALUE = primiti_datogram(sudionik)
            break
        except sustav_pogreška as GREŠKA:
            if GREŠKA.INDEX != 다시시도오류 or 밀리초() - Pokreni >= 700:
                raise
    assert odgovor == datogram
    Izlaz("PYTHON 네트워크 provjeriti: UDP hrvatski")
finally:
    Zatvori_mreža(sudionik)
