"""vlastiti 커널의 Datoteka·통신·화면 호출과 hrvatski iznimka. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operacijski_sustav
import sys as CLR

def Izlaz(*VALUE, razdjelnik=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = razdjelnik
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

cijeli_broj = int
명령인수 = CLR.argv
다시시도오류 = 11

class sustav_pogreška(OSError):
    def __init__(자신, INDEX, 설명="operacijski_sustav 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *Argumenti):
    try:
        return FUNCTION_VALUE(*Argumenti)
    except OSError as GREŠKA:
        INDEX = GREŠKA.args[0] if GREŠKA.args else 0
        raise sustav_pogreška(INDEX)

def kodirati_SMS(Tekst):
    return Tekst.encode("utf-8")

def 글해독(podaci):
    return podaci.decode("utf-8")

def 파일읽기(Ime):
    return 운영호출(operacijski_sustav.read, Ime)

def zapisivanje_Datoteka(Ime, podaci):
    return 운영호출(operacijski_sustav.write, Ime, podaci)

def ukloniti_Datoteka(Ime):
    return 운영호출(operacijski_sustav.remove, Ime)

def otvoreno_datogram(broj_priključka):
    return 운영호출(operacijski_sustav.udp_open, broj_priključka)

def slati_datogram(sudionik, broj_priključka, podaci):
    return 운영호출(operacijski_sustav.udp_send, sudionik, broj_priključka, podaci)

def slati_vanjski_datogram(sudionik, adresa, broj_priključka, podaci):
    return 운영호출(operacijski_sustav.udp_sendto, sudionik, adresa, broj_priključka, podaci)

def primiti_datogram(sudionik):
    return 운영호출(operacijski_sustav.udp_recv, sudionik)

def Zatvori_mreža(sudionik):
    return 운영호출(operacijski_sustav.udp_close, sudionik)

def Crtanje_pravokutnik(*Argumenti):
    return 운영호출(operacijski_sustav.rect, *Argumenti)

def 화면크기():
    return 운영호출(operacijski_sustav.screen_size)

def 그림기다리기():
    return 운영호출(operacijski_sustav.wait_key)

밀리초 = operacijski_sustav.ticks_ms
