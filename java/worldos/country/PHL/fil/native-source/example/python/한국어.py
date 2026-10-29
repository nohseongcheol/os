"""자체 커널의 file·통신·화면 호출과 한국어 pagbubukod. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operating_system
import sys as common_language_runtime

def 출력(*VALUE, tagahiwalay=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = tagahiwalay
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

integer_buong_numero = int
명령인수 = common_language_runtime.argv
다시시도오류 = 11

class system_error(OSError):
    def __init__(자신, INDEX, 설명="operating_system 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(pormula_VALUE, *인수):
    try:
        return pormula_VALUE(*인수)
    except OSError as error:
        INDEX = error.args[0] if error.args else 0
        raise system_error(INDEX)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(pangalan):
    return 운영호출(operating_system.read, pangalan)

def sumulat_file(pangalan, data):
    return 운영호출(operating_system.write, pangalan, data)

def tanggalin_file(pangalan):
    return 운영호출(operating_system.remove, pangalan)

def 전문통신열기(numero_ng_port):
    return 운영호출(operating_system.udp_open, numero_ng_port)

def 전문보내기(종단, numero_ng_port, data):
    return 운영호출(operating_system.udp_send, 종단, numero_ng_port, data)

def 바깥전문보내기(종단, email, numero_ng_port, data):
    return 운영호출(operating_system.udp_sendto, 종단, email, numero_ng_port, data)

def 전문받기(종단):
    return 운영호출(operating_system.udp_recv, 종단)

def isara_Network(종단):
    return 운영호출(operating_system.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(operating_system.rect, *인수)

def 화면크기():
    return 운영호출(operating_system.screen_size)

def 그림기다리기():
    return 운영호출(operating_system.wait_key)

밀리초 = operating_system.ticks_ms
