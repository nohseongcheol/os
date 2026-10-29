"""lastno 커널의 Datoteka·통신·화면 호출과 slovenščina izjema. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operacijski_sistem
import sys as skupni_jezikovni_izvajalnik

def Izpis(*VALUE, ločilo=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ločilo
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

celo_število = int
명령인수 = skupni_jezikovni_izvajalnik.argv
다시시도오류 = 11

class sistemska_napaka(OSError):
    def __init__(자신, INDEX, 설명="operacijski_sistem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *Argumenti):
    try:
        return FUNCTION_VALUE(*Argumenti)
    except OSError as NAPAKA:
        INDEX = NAPAKA.args[0] if NAPAKA.args else 0
        raise sistemska_napaka(INDEX)

def kodirati_SMS(Besedilo):
    return Besedilo.encode("utf-8")

def 글해독(podatki):
    return podatki.decode("utf-8")

def 파일읽기(Ime):
    return 운영호출(operacijski_sistem.read, Ime)

def pisati_Datoteka(Ime, podatki):
    return 운영호출(operacijski_sistem.write, Ime, podatki)

def odstraniti_Datoteka(Ime):
    return 운영호출(operacijski_sistem.remove, Ime)

def odprto_datagram(številka_vrat):
    return 운영호출(operacijski_sistem.udp_open, številka_vrat)

def poslati_datagram(končna_točka, številka_vrat, podatki):
    return 운영호출(operacijski_sistem.udp_send, končna_točka, številka_vrat, podatki)

def poslati_zunanji_datagram(končna_točka, naslov, številka_vrat, podatki):
    return 운영호출(operacijski_sistem.udp_sendto, končna_točka, naslov, številka_vrat, podatki)

def sprejeti_sprejemati_prejeti_prejemati_datagram(končna_točka):
    return 운영호출(operacijski_sistem.udp_recv, končna_točka)

def Zapri_mreža(končna_točka):
    return 운영호출(operacijski_sistem.udp_close, končna_točka)

def risati_pravokotnik(*Argumenti):
    return 운영호출(operacijski_sistem.rect, *Argumenti)

def 화면크기():
    return 운영호출(operacijski_sistem.screen_size)

def 그림기다리기():
    return 운영호출(operacijski_sistem.wait_key)

밀리초 = operacijski_sistem.ticks_ms
