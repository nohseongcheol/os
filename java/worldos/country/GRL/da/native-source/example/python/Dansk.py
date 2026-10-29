"""eget 커널의 Fil·통신·skærmbillede 호출과 Dansk undtagelse. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operativsystem
import sys as CLR

def Udgang(*VÆRDI, separator=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = separator
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VÆRDI, **기존인수)

heltal = int
명령인수 = CLR.argv
다시시도오류 = 11

class systemfejl(OSError):
    def __init__(자신, INDEKS, 설명="operativsystem 작업에 실패했습니다."):
        super().__init__(INDEKS, 설명)
        자신.INDEKS = INDEKS
        자신.설명 = 설명

def 운영호출(FUNKTION_VÆRDI, *Argumenter):
    try:
        return FUNKTION_VÆRDI(*Argumenter)
    except OSError as fejl:
        INDEKS = fejl.args[0] if fejl.args else 0
        raise systemfejl(INDEKS)

def kode_sms(Tekst):
    return Tekst.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Navn):
    return 운영호출(operativsystem.read, Navn)

def skrive_fil(Navn, data):
    return 운영호출(operativsystem.write, Navn, data)

def fjerne_fil(Navn):
    return 운영호출(operativsystem.remove, Navn)

def åben_datagram(portnummer):
    return 운영호출(operativsystem.udp_open, portnummer)

def maile_datagram(slutpunkt, portnummer, data):
    return 운영호출(operativsystem.udp_send, slutpunkt, portnummer, data)

def maile_ekstern_datagram(slutpunkt, mail, portnummer, data):
    return 운영호출(operativsystem.udp_sendto, slutpunkt, mail, portnummer, data)

def modtage_datagram(slutpunkt):
    return 운영호출(operativsystem.udp_recv, slutpunkt)

def Luk_netværk(slutpunkt):
    return 운영호출(operativsystem.udp_close, slutpunkt)

def tegne_rektangel(*Argumenter):
    return 운영호출(operativsystem.rect, *Argumenter)

def skærmbillede_tilpasse_størrelse():
    return 운영호출(operativsystem.screen_size)

def 그림기다리기():
    return 운영호출(operativsystem.wait_key)

밀리초 = operativsystem.ticks_ms
