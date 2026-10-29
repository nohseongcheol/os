"""자체 커널의 faidhle·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as siostam_obrachaidh
import sys as Common_Language_Runtime

def 출력(*VALUE, sgaradair=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = sgaradair
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

àireamh_shlàn = int
명령인수 = Common_Language_Runtime.argv
다시시도오류 = 11

class siostam_mearachd(OSError):
    def __init__(자신, INDEX, 설명="siostam_obrachaidh 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *인수):
    try:
        return FUNCTION_VALUE(*인수)
    except OSError as Mearachd:
        INDEX = Mearachd.args[0] if Mearachd.args else 0
        raise siostam_mearachd(INDEX)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(dàta):
    return dàta.decode("utf-8")

def 파일읽기(Ainm):
    return 운영호출(siostam_obrachaidh.read, Ainm)

def sgrìobh_faidhle(Ainm, dàta):
    return 운영호출(siostam_obrachaidh.write, Ainm, dàta)

def thoir_air_falbh_faidhle(Ainm):
    return 운영호출(siostam_obrachaidh.remove, Ainm)

def 전문통신열기(접속번호):
    return 운영호출(siostam_obrachaidh.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, dàta):
    return 운영호출(siostam_obrachaidh.udp_send, 종단, 접속번호, dàta)

def 바깥전문보내기(종단, ADDRESS, 접속번호, dàta):
    return 운영호출(siostam_obrachaidh.udp_sendto, 종단, ADDRESS, 접속번호, dàta)

def 전문받기(종단):
    return 운영호출(siostam_obrachaidh.udp_recv, 종단)

def dùin_lìonra(종단):
    return 운영호출(siostam_obrachaidh.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(siostam_obrachaidh.rect, *인수)

def 화면크기():
    return 운영호출(siostam_obrachaidh.screen_size)

def 그림기다리기():
    return 운영호출(siostam_obrachaidh.wait_key)

밀리초 = siostam_obrachaidh.ticks_ms
