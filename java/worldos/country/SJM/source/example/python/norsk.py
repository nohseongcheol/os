"""eget 커널의 Fil·통신·skjermbilde 호출과 norsk unntak. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operativsystem
import sys as CLR

def Utgang(*VERDI, skillelinje=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = skillelinje
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VERDI, **기존인수)

heltall = int
명령인수 = CLR.argv
다시시도오류 = 11

class systemfeil(OSError):
    def __init__(자신, INDEKS, 설명="operativsystem 작업에 실패했습니다."):
        super().__init__(INDEKS, 설명)
        자신.INDEKS = INDEKS
        자신.설명 = 설명

def 운영호출(FUNKSJON_VERDI, *Argumenter):
    try:
        return FUNKSJON_VERDI(*Argumenter)
    except OSError as feil:
        INDEKS = feil.args[0] if feil.args else 0
        raise systemfeil(INDEKS)

def 글부호화(Tekst):
    return Tekst.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Navn):
    return 운영호출(operativsystem.read, Navn)

def skrive_Fil(Navn, data):
    return 운영호출(operativsystem.write, Navn, data)

def fjerne_Fil(Navn):
    return 운영호출(operativsystem.remove, Navn)

def åpen_datagram(portnummer):
    return 운영호출(operativsystem.udp_open, portnummer)

def sende_datagram(deltaker, portnummer, data):
    return 운영호출(operativsystem.udp_send, deltaker, portnummer, data)

def sende_ekstern_datagram(deltaker, e_post, portnummer, data):
    return 운영호출(operativsystem.udp_sendto, deltaker, e_post, portnummer, data)

def motta_datagram(deltaker):
    return 운영호출(operativsystem.udp_recv, deltaker)

def Lukk_nettverk(deltaker):
    return 운영호출(operativsystem.udp_close, deltaker)

def Tegn_rektangel(*Argumenter):
    return 운영호출(operativsystem.rect, *Argumenter)

def skjermbilde_skalere():
    return 운영호출(operativsystem.screen_size)

def 그림기다리기():
    return 운영호출(operativsystem.wait_key)

밀리초 = operativsystem.ticks_ms
