"""자체 커널의 Ffeil·통신·화면 호출과 Cymraeg eithriad. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as system_weithredu
import sys as amser_rhedeg_iaith_gyffredin

def Allbwn(*VALUE, gwahanydd=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = gwahanydd
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

cyfanrif = int
명령인수 = amser_rhedeg_iaith_gyffredin.argv
다시시도오류 = 11

class system_gwall(OSError):
    def __init__(자신, INDEX, 설명="system_weithredu 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(SWYDDOGAETH_VALUE, *인수):
    try:
        return SWYDDOGAETH_VALUE(*인수)
    except OSError as Gwall:
        INDEX = Gwall.args[0] if Gwall.args else 0
        raise system_gwall(INDEX)

def 글부호화(Testun):
    return Testun.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Enw):
    return 운영호출(system_weithredu.read, Enw)

def ysgrifennu_ffeil(Enw, data):
    return 운영호출(system_weithredu.write, Enw, data)

def tynnu_ffeil(Enw):
    return 운영호출(system_weithredu.remove, Enw)

def 전문통신열기(rhif_porth):
    return 운영호출(system_weithredu.udp_open, rhif_porth)

def 전문보내기(종단, rhif_porth, data):
    return 운영호출(system_weithredu.udp_send, 종단, rhif_porth, data)

def 바깥전문보내기(종단, ADDRESS, rhif_porth, data):
    return 운영호출(system_weithredu.udp_sendto, 종단, ADDRESS, rhif_porth, data)

def 전문받기(종단):
    return 운영호출(system_weithredu.udp_recv, 종단)

def cau_Rhwydwaith(종단):
    return 운영호출(system_weithredu.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(system_weithredu.rect, *인수)

def 화면크기():
    return 운영호출(system_weithredu.screen_size)

def 그림기다리기():
    return 운영호출(system_weithredu.wait_key)

밀리초 = system_weithredu.ticks_ms
