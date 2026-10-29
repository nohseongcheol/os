"""자체 커널의 Idosiye·통신·화면 호출과 Ikinyarwanda 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sisitemu_ngengamikorere
import sys as igihe_ururimi_rukorwamo

def 출력(*agaciro, mutandukanya=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = mutandukanya
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*agaciro, **기존인수)

umubare_wuzuye = int
명령인수 = igihe_ururimi_rukorwamo.argv
다시시도오류 = 11

class sisitemu_ikosa(OSError):
    def __init__(자신, umugerekashakiro, 설명="sisitemu_ngengamikorere 작업에 실패했습니다."):
        super().__init__(umugerekashakiro, 설명)
        자신.umugerekashakiro = umugerekashakiro
        자신.설명 = 설명

def 운영호출(FUNCTION_agaciro, *인수):
    try:
        return FUNCTION_agaciro(*인수)
    except OSError as IKOSA:
        umugerekashakiro = IKOSA.args[0] if IKOSA.args else 0
        raise sisitemu_ikosa(umugerekashakiro)

def 글부호화(Umwandiko):
    return Umwandiko.encode("utf-8")

def 글해독(amakurushingiro):
    return amakurushingiro.decode("utf-8")

def 파일읽기(Izina):
    return 운영호출(sisitemu_ngengamikorere.read, Izina)

def kwandika_dosiye(Izina, amakurushingiro):
    return 운영호출(sisitemu_ngengamikorere.write, Izina, amakurushingiro)

def gukuramo_dosiye(Izina):
    return 운영호출(sisitemu_ngengamikorere.remove, Izina)

def 전문통신열기(접속번호):
    return 운영호출(sisitemu_ngengamikorere.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, amakurushingiro):
    return 운영호출(sisitemu_ngengamikorere.udp_send, 종단, 접속번호, amakurushingiro)

def 바깥전문보내기(종단, aderesi, 접속번호, amakurushingiro):
    return 운영호출(sisitemu_ngengamikorere.udp_sendto, 종단, aderesi, 접속번호, amakurushingiro)

def 전문받기(종단):
    return 운영호출(sisitemu_ngengamikorere.udp_recv, 종단)

def gufunga_Urusobemiyoboro(종단):
    return 운영호출(sisitemu_ngengamikorere.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(sisitemu_ngengamikorere.rect, *인수)

def 화면크기():
    return 운영호출(sisitemu_ngengamikorere.screen_size)

def 그림기다리기():
    return 운영호출(sisitemu_ngengamikorere.wait_key)

밀리초 = sisitemu_ngengamikorere.ticks_ms
