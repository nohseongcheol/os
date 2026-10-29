from Eesti import Väljund, avama_datagramm, saatma_väline_datagramm, saama_datagramm, Sule_võrk, 밀리초
from Eesti import süsteem_tõrge, 다시시도오류, kodeerima_SMS, 명령인수, täisarv
osaleja = avama_datagramm(0)
try:
    datagramm = kodeerima_SMS("PYTHON UDP Eesti")
    saatma_väline_datagramm(osaleja, "10.0.2.2", täisarv(명령인수[1]), datagramm)
    Käivita_2 = 밀리초()
    while True:
        try:
            vastus, port_VALUE = saama_datagramm(osaleja)
            break
        except süsteem_tõrge as VIGA:
            if VIGA.INDEX != 다시시도오류 or 밀리초() - Käivita_2 >= 700:
                raise
    assert vastus == datagramm
    Väljund("PYTHON 네트워크 kinnitama: UDP Eesti")
finally:
    Sule_võrk(osaleja)
