"""자체 커널의 Comhad·통신·화면 호출과 Gaeilge eisceacht. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as córas_oibriúcháin
import sys as am_rite_teanga_coiteann

def Aschur(*VALUE, deighilteoir=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = deighilteoir
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

slánuimhir = int
명령인수 = am_rite_teanga_coiteann.argv
다시시도오류 = 11

class córas_earráid(OSError):
    def __init__(자신, INDEX, 설명="córas_oibriúcháin 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(feidhm_VALUE, *Argóintí):
    try:
        return feidhm_VALUE(*Argóintí)
    except OSError as ERREÁID:
        INDEX = ERREÁID.args[0] if ERREÁID.args else 0
        raise córas_earráid(INDEX)

def 글부호화(Téacs):
    return Téacs.encode("utf-8")

def 글해독(sonraí):
    return sonraí.decode("utf-8")

def 파일읽기(Ainm):
    return 운영호출(córas_oibriúcháin.read, Ainm)

def scríobh_comhad(Ainm, sonraí):
    return 운영호출(córas_oibriúcháin.write, Ainm, sonraí)

def bain_comhad(Ainm):
    return 운영호출(córas_oibriúcháin.remove, Ainm)

def 전문통신열기(uimhir_phoirt):
    return 운영호출(córas_oibriúcháin.udp_open, uimhir_phoirt)

def 전문보내기(종단, uimhir_phoirt, sonraí):
    return 운영호출(córas_oibriúcháin.udp_send, 종단, uimhir_phoirt, sonraí)

def 바깥전문보내기(종단, ADDRESS, uimhir_phoirt, sonraí):
    return 운영호출(córas_oibriúcháin.udp_sendto, 종단, ADDRESS, uimhir_phoirt, sonraí)

def 전문받기(종단):
    return 운영호출(córas_oibriúcháin.udp_recv, 종단)

def dún_Líonra(종단):
    return 운영호출(córas_oibriúcháin.udp_close, 종단)

def 네모그리기(*Argóintí):
    return 운영호출(córas_oibriúcháin.rect, *Argóintí)

def 화면크기():
    return 운영호출(córas_oibriúcháin.screen_size)

def 그림기다리기():
    return 운영호출(córas_oibriúcháin.wait_key)

밀리초 = córas_oibriúcháin.ticks_ms
