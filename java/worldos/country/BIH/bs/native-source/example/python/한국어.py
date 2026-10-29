"""자체 커널의 Fajl·통신·화면 호출과 한국어 izuzetak. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operativni_sistem
import sys as zajednička_jezička_biblioteka

def Ispis(*VALUE, razdjelnik=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = razdjelnik
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

cijeli_broj = int
명령인수 = zajednička_jezička_biblioteka.argv
다시시도오류 = 11

class sistem_greška(OSError):
    def __init__(자신, INDEX, 설명="operativni_sistem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *Argumenti):
    try:
        return FUNCTION_VALUE(*Argumenti)
    except OSError as GRESKA:
        INDEX = GRESKA.args[0] if GRESKA.args else 0
        raise sistem_greška(INDEX)

def 글부호화(Tekst):
    return Tekst.encode("utf-8")

def 글해독(podaci):
    return podaci.decode("utf-8")

def 파일읽기(Naziv):
    return 운영호출(operativni_sistem.read, Naziv)

def pisati_fajl(Naziv, podaci):
    return 운영호출(operativni_sistem.write, Naziv, podaci)

def ukloniti_fajl(Naziv):
    return 운영호출(operativni_sistem.remove, Naziv)

def 전문통신열기(broj_priključka):
    return 운영호출(operativni_sistem.udp_open, broj_priključka)

def 전문보내기(završna_tačka, broj_priključka, podaci):
    return 운영호출(operativni_sistem.udp_send, završna_tačka, broj_priključka, podaci)

def 바깥전문보내기(završna_tačka, adresa, broj_priključka, podaci):
    return 운영호출(operativni_sistem.udp_sendto, završna_tačka, adresa, broj_priključka, podaci)

def 전문받기(završna_tačka):
    return 운영호출(operativni_sistem.udp_recv, završna_tačka)

def zatvoriti_Mreža(završna_tačka):
    return 운영호출(operativni_sistem.udp_close, završna_tačka)

def 네모그리기(*Argumenti):
    return 운영호출(operativni_sistem.rect, *Argumenti)

def 화면크기():
    return 운영호출(operativni_sistem.screen_size)

def 그림기다리기():
    return 운영호출(operativni_sistem.wait_key)

밀리초 = operativni_sistem.ticks_ms
