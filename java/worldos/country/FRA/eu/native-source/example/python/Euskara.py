"""자체 커널의 Fitxategia·통신·화면 호출과 Euskara salbuespen. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistema_eragile
import sys as 실행환경

def Irteera(*balio, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*balio, **기존인수)

osoko_zenbaki = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class sistema_errore(OSError):
    def __init__(자신, INDIZE, 설명="sistema_eragile 작업에 실패했습니다."):
        super().__init__(INDIZE, 설명)
        자신.INDIZE = INDIZE
        자신.설명 = 설명

def 운영호출(FUNTZIOA_balio, *Argumentuak):
    try:
        return FUNTZIOA_balio(*Argumentuak)
    except OSError as errorea:
        INDIZE = errorea.args[0] if errorea.args else 0
        raise sistema_errore(INDIZE)

def 글부호화(Testua):
    return Testua.encode("utf-8")

def 글해독(datuak):
    return datuak.decode("utf-8")

def 파일읽기(Izena):
    return 운영호출(sistema_eragile.read, Izena)

def idatzi_fitxategi(Izena, datuak):
    return 운영호출(sistema_eragile.write, Izena, datuak)

def kendu_fitxategi(Izena):
    return 운영호출(sistema_eragile.remove, Izena)

def 전문통신열기(ataka_zenbaki):
    return 운영호출(sistema_eragile.udp_open, ataka_zenbaki)

def 전문보내기(amaiera_puntu, ataka_zenbaki, datuak):
    return 운영호출(sistema_eragile.udp_send, amaiera_puntu, ataka_zenbaki, datuak)

def 바깥전문보내기(amaiera_puntu, helbide, ataka_zenbaki, datuak):
    return 운영호출(sistema_eragile.udp_sendto, amaiera_puntu, helbide, ataka_zenbaki, datuak)

def 전문받기(amaiera_puntu):
    return 운영호출(sistema_eragile.udp_recv, amaiera_puntu)

def itxi_sare(amaiera_puntu):
    return 운영호출(sistema_eragile.udp_close, amaiera_puntu)

def 네모그리기(*Argumentuak):
    return 운영호출(sistema_eragile.rect, *Argumentuak)

def 화면크기():
    return 운영호출(sistema_eragile.screen_size)

def 그림기다리기():
    return 운영호출(sistema_eragile.wait_key)

밀리초 = sistema_eragile.ticks_ms
