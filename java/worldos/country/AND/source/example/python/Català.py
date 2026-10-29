"""propi 커널의 Fitxer·통신·화면 호출과 Català excepció. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistema_operatiu
import sys as 실행환경

def Sortida(*VALOR, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALOR, **기존인수)

정수 = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class sistema_error(OSError):
    def __init__(자신, INDEX, 설명="sistema_operatiu 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCIÓ_VALOR, *인수):
    try:
        return FUNCIÓ_VALOR(*인수)
    except OSError as s_ha_produït_un_error:
        INDEX = s_ha_produït_un_error.args[0] if s_ha_produït_un_error.args else 0
        raise sistema_error(INDEX)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(dades):
    return dades.decode("utf-8")

def tancar_arxiu(Nom):
    return 운영호출(sistema_operatiu.read, Nom)

def escriure_arxiu(Nom, dades):
    return 운영호출(sistema_operatiu.write, Nom, dades)

def suprimir_arxiu(Nom):
    return 운영호출(sistema_operatiu.remove, Nom)

def 전문통신열기(número_de_port):
    return 운영호출(sistema_operatiu.udp_open, número_de_port)

def 전문보내기(extrem, número_de_port, dades):
    return 운영호출(sistema_operatiu.udp_send, extrem, número_de_port, dades)

def 바깥전문보내기(extrem, Adreça, número_de_port, dades):
    return 운영호출(sistema_operatiu.udp_sendto, extrem, Adreça, número_de_port, dades)

def 전문받기(extrem):
    return 운영호출(sistema_operatiu.udp_recv, extrem)

def Tanca_xarxa(extrem):
    return 운영호출(sistema_operatiu.udp_close, extrem)

def 네모그리기(*인수):
    return 운영호출(sistema_operatiu.rect, *인수)

def 화면크기():
    return 운영호출(sistema_operatiu.screen_size)

def 그림기다리기():
    return 운영호출(sistema_operatiu.wait_key)

밀리초 = sistema_operatiu.ticks_ms
