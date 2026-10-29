"""własny 커널의 nazwa_pliku·komunikacja·화면 호출과 polski wyjątek. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as system_operacyjny
import sys as CLR

def pozycja_wyjścia(*WARTOŚĆ, separator=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = separator
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*WARTOŚĆ, **기존인수)

liczba_całkowita = int
명령인수 = CLR.argv
다시시도오류 = 11

class błąd_systemu(OSError):
    def __init__(자신, INDEKS, 설명="system_operacyjny 작업에 실패했습니다."):
        super().__init__(INDEKS, 설명)
        자신.INDEKS = INDEKS
        자신.설명 = 설명

def 운영호출(FUNKCJA_WARTOŚĆ, *argumenty):
    try:
        return FUNKCJA_WARTOŚĆ(*argumenty)
    except OSError as błąd:
        INDEKS = błąd.args[0] if błąd.args else 0
        raise błąd_systemu(INDEKS)

def kodować_SMS(tekst):
    return tekst.encode("utf-8")

def 글해독(dane):
    return dane.decode("utf-8")

def 파일읽기(Nazwa):
    return 운영호출(system_operacyjny.read, Nazwa)

def zapis_Plik(Nazwa, dane):
    return 운영호출(system_operacyjny.write, Nazwa, dane)

def usuń_Plik(Nazwa):
    return 운영호출(system_operacyjny.remove, Nazwa)

def otwarty_datagram(numer_portu):
    return 운영호출(system_operacyjny.udp_open, numer_portu)

def wysłać_datagram(uczestnik, numer_portu, dane):
    return 운영호출(system_operacyjny.udp_send, uczestnik, numer_portu, dane)

def wysłać_zewnętrzny_datagram(uczestnik, Adres, numer_portu, dane):
    return 운영호출(system_operacyjny.udp_sendto, uczestnik, Adres, numer_portu, dane)

def odbierać_datagram(uczestnik):
    return 운영호출(system_operacyjny.udp_recv, uczestnik)

def Zamknij_sieć(uczestnik):
    return 운영호출(system_operacyjny.udp_close, uczestnik)

def rysować_prostokąt(*argumenty):
    return 운영호출(system_operacyjny.rect, *argumenty)

def 화면크기():
    return 운영호출(system_operacyjny.screen_size)

def 그림기다리기():
    return 운영호출(system_operacyjny.wait_key)

밀리초 = system_operacyjny.ticks_ms
