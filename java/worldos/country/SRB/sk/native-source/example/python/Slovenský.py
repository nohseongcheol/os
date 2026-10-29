"""vlastné 커널의 Súbor·통신·화면 호출과 Slovenský výnimka. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operačný_systém
import sys as CLR

def Výstup(*VALUE, oddeľovač=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = oddeľovač
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

celé_číslo = int
명령인수 = CLR.argv
다시시도오류 = 11

class systém_Chyba(OSError):
    def __init__(자신, INDEX, 설명="operačný_systém 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(funkcia_VALUE, *Argumenty):
    try:
        return funkcia_VALUE(*Argumenty)
    except OSError as chyba:
        INDEX = chyba.args[0] if chyba.args else 0
        raise systém_Chyba(INDEX)

def kódovať_SMS(Spracovanie_textu):
    return Spracovanie_textu.encode("utf-8")

def 글해독(údaje):
    return údaje.decode("utf-8")

def 파일읽기(Názov):
    return 운영호출(operačný_systém.read, Názov)

def zapísať_Súbor(Názov, údaje):
    return 운영호출(operačný_systém.write, Názov, údaje)

def odobrať_Súbor(Názov):
    return 운영호출(operačný_systém.remove, Názov)

def otvoriť_datagram(číslo_portu):
    return 운영호출(operačný_systém.udp_open, číslo_portu)

def odoslať_datagram(účastník, číslo_portu, údaje):
    return 운영호출(operačný_systém.udp_send, účastník, číslo_portu, údaje)

def odoslať_externý_datagram(účastník, adresa, číslo_portu, údaje):
    return 운영호출(operačný_systém.udp_sendto, účastník, adresa, číslo_portu, údaje)

def dostať_datagram(účastník):
    return 운영호출(operačný_systém.udp_recv, účastník)

def Zavrieť_sieť(účastník):
    return 운영호출(operačný_systém.udp_close, účastník)

def kresliť_obdĺžnik(*Argumenty):
    return 운영호출(operačný_systém.rect, *Argumenty)

def 화면크기():
    return 운영호출(operačný_systém.screen_size)

def 그림기다리기():
    return 운영호출(operačný_systém.wait_key)

밀리초 = operačný_systém.ticks_ms
