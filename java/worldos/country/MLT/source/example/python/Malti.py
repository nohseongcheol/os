"""자체 커널의 fajl·통신·화면 호출과 Malti 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistema_operattiva
import sys as tħaddim_tal_lingwa_komuni

def 출력(*VALUE, separatur=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = separatur
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

numru_sħiħ = int
명령인수 = tħaddim_tal_lingwa_komuni.argv
다시시도오류 = 11

class sistema_żball(OSError):
    def __init__(자신, INDEX, 설명="sistema_operattiva 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *인수):
    try:
        return FUNCTION_VALUE(*인수)
    except OSError as żball:
        INDEX = żball.args[0] if żball.args else 0
        raise sistema_żball(INDEX)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(isem):
    return 운영호출(sistema_operattiva.read, isem)

def kiteb_fajl(isem, data):
    return 운영호출(sistema_operattiva.write, isem, data)

def neħħa_fajl(isem):
    return 운영호출(sistema_operattiva.remove, isem)

def 전문통신열기(접속번호):
    return 운영호출(sistema_operattiva.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, data):
    return 운영호출(sistema_operattiva.udp_send, 종단, 접속번호, data)

def 바깥전문보내기(종단, ADDRESS, 접속번호, data):
    return 운영호출(sistema_operattiva.udp_sendto, 종단, ADDRESS, 접속번호, data)

def 전문받기(종단):
    return 운영호출(sistema_operattiva.udp_recv, 종단)

def agħlaq_netwerk(종단):
    return 운영호출(sistema_operattiva.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(sistema_operattiva.rect, *인수)

def 화면크기():
    return 운영호출(sistema_operattiva.screen_size)

def 그림기다리기():
    return 운영호출(sistema_operattiva.wait_key)

밀리초 = sistema_operattiva.ticks_ms
