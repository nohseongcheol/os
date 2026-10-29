"""자체 커널의 Fil·통신·화면 호출과 한국어 unntak. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operativsystem
import sys as Common_Language_Runtime

def Utdata(*VALUE, skiljeline=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = skiljeline
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

heiltal = int
명령인수 = Common_Language_Runtime.argv
다시시도오류 = 11

class system_feil(OSError):
    def __init__(자신, INDEX, 설명="operativsystem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *Argument):
    try:
        return FUNCTION_VALUE(*Argument)
    except OSError as FEIL:
        INDEX = FEIL.args[0] if FEIL.args else 0
        raise system_feil(INDEX)

def 글부호화(Tekst):
    return Tekst.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Namn):
    return 운영호출(operativsystem.read, Namn)

def skrive_fil(Namn, data):
    return 운영호출(operativsystem.write, Namn, data)

def fjerne_fil(Namn):
    return 운영호출(operativsystem.remove, Namn)

def 전문통신열기(portnummer):
    return 운영호출(operativsystem.udp_open, portnummer)

def 전문보내기(endepunkt, portnummer, data):
    return 운영호출(operativsystem.udp_send, endepunkt, portnummer, data)

def 바깥전문보내기(endepunkt, ADDRESS, portnummer, data):
    return 운영호출(operativsystem.udp_sendto, endepunkt, ADDRESS, portnummer, data)

def 전문받기(endepunkt):
    return 운영호출(operativsystem.udp_recv, endepunkt)

def Lukk_Nettverk(endepunkt):
    return 운영호출(operativsystem.udp_close, endepunkt)

def 네모그리기(*Argument):
    return 운영호출(operativsystem.rect, *Argument)

def 화면크기():
    return 운영호출(operativsystem.screen_size)

def 그림기다리기():
    return 운영호출(operativsystem.wait_key)

밀리초 = operativsystem.ticks_ms
