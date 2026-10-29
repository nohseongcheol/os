from polski import pozycja_wyjścia, otwarty_datagram, wysłać_zewnętrzny_datagram, odbierać_datagram, Zamknij_sieć, 밀리초
from polski import błąd_systemu, 다시시도오류, kodować_SMS, 명령인수, liczba_całkowita
uczestnik = otwarty_datagram(0)
try:
    datagram = kodować_SMS("PYTHON UDP pl")
    wysłać_zewnętrzny_datagram(uczestnik, "10.0.2.2", liczba_całkowita(명령인수[1]), datagram)
    Uruchom_2 = 밀리초()
    while True:
        try:
            odpowiedź, port_WARTOŚĆ = odbierać_datagram(uczestnik)
            break
        except błąd_systemu as błąd:
            if błąd.INDEKS != 다시시도오류 or 밀리초() - Uruchom_2 >= 700:
                raise
    assert odpowiedź == datagram
    pozycja_wyjścia("PYTHON 네트워크 확인: UDP pl")
finally:
    Zamknij_sieć(uczestnik)
