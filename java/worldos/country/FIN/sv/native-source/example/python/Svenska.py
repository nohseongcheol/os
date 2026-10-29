"""eget 커널의 filnamn·kommunikation·skärmbild 호출과 Svenska fel_31f743d2. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operativsystem
import sys as CLR

def utmatningsposition(*värde, avgränsare=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = avgränsare
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*värde, **기존인수)

heltal = int
명령인수 = CLR.argv
다시시도오류 = 11

class systemfel(OSError):
    def __init__(자신, INDEX, 설명="operativsystem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNKTION_värde, *argument):
    try:
        return FUNKTION_värde(*argument)
    except OSError as fel:
        INDEX = fel.args[0] if fel.args else 0
        raise systemfel(INDEX)

def koda_SMS(text):
    return text.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def läsa_fil(Namn):
    return 운영호출(operativsystem.read, Namn)

def skriva_fil(Namn, data):
    return 운영호출(operativsystem.write, Namn, data)

def ta_bort_fil(Namn):
    return 운영호출(operativsystem.remove, Namn)

def skapa_datagram(portnummer):
    return 운영호출(operativsystem.udp_open, portnummer)

def skicka_datagram(deltagare, portnummer, data):
    return 운영호출(operativsystem.udp_send, deltagare, portnummer, data)

def skicka_extern_datagram(deltagare, Adress, portnummer, data):
    return 운영호출(operativsystem.udp_sendto, deltagare, Adress, portnummer, data)

def få_datagram(deltagare):
    return 운영호출(operativsystem.udp_recv, deltagare)

def Stäng_nätverk(deltagare):
    return 운영호출(operativsystem.udp_close, deltagare)

def Rita_rektangel(*argument):
    return 운영호출(operativsystem.rect, *argument)

def skärmbild_storlek():
    return 운영호출(operativsystem.screen_size)

def 그림기다리기():
    return 운영호출(operativsystem.wait_key)

밀리초 = operativsystem.ticks_ms
