"""oma 커널의 Fail·통신·화면 호출과 Eesti erand. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operatsioonisüsteem
import sys as CLR

def Väljund(*VALUE, eraldaja=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = eraldaja
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

täisarv = int
명령인수 = CLR.argv
다시시도오류 = 11

class süsteem_tõrge(OSError):
    def __init__(자신, INDEX, 설명="operatsioonisüsteem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *Argumendid):
    try:
        return FUNCTION_VALUE(*Argumendid)
    except OSError as VIGA:
        INDEX = VIGA.args[0] if VIGA.args else 0
        raise süsteem_tõrge(INDEX)

def kodeerima_SMS(Tekst):
    return Tekst.encode("utf-8")

def 글해독(andmed):
    return andmed.decode("utf-8")

def 파일읽기(Nimi_2):
    return 운영호출(operatsioonisüsteem.read, Nimi_2)

def kirjutamine_Fail(Nimi_2, andmed):
    return 운영호출(operatsioonisüsteem.write, Nimi_2, andmed)

def eemaldama_Fail(Nimi_2):
    return 운영호출(operatsioonisüsteem.remove, Nimi_2)

def avama_datagramm(pordinumber):
    return 운영호출(operatsioonisüsteem.udp_open, pordinumber)

def saatma_datagramm(osaleja, pordinumber, andmed):
    return 운영호출(operatsioonisüsteem.udp_send, osaleja, pordinumber, andmed)

def saatma_väline_datagramm(osaleja, ADDRESS, pordinumber, andmed):
    return 운영호출(operatsioonisüsteem.udp_sendto, osaleja, ADDRESS, pordinumber, andmed)

def saama_datagramm(osaleja):
    return 운영호출(operatsioonisüsteem.udp_recv, osaleja)

def Sule_võrk(osaleja):
    return 운영호출(operatsioonisüsteem.udp_close, osaleja)

def Joonista_ristkülik(*Argumendid):
    return 운영호출(operatsioonisüsteem.rect, *Argumendid)

def 화면크기():
    return 운영호출(operatsioonisüsteem.screen_size)

def 그림기다리기():
    return 운영호출(operatsioonisüsteem.wait_key)

밀리초 = operatsioonisüsteem.ticks_ms
