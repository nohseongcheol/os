"""자체 커널의 fiilde·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as yuɓɓo_kurdinɗo
import sys as 실행환경

def 출력(*njaru, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*njaru, **기존인수)

정수 = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class yuɓɓo_juumre(OSError):
    def __init__(자신, joopirdu, 설명="yuɓɓo_kurdinɗo 작업에 실패했습니다."):
        super().__init__(joopirdu, 설명)
        자신.joopirdu = joopirdu
        자신.설명 = 설명

def 운영호출(juɓɓol_njaru, *인수):
    try:
        return juɓɓol_njaru(*인수)
    except OSError as juumre:
        joopirdu = juumre.args[0] if juumre.args else 0
        raise yuɓɓo_juumre(joopirdu)

def 글부호화(binndi):
    return binndi.encode("utf-8")

def 글해독(keɓe):
    return keɓe.decode("utf-8")

def 파일읽기(innde):
    return 운영호출(yuɓɓo_kurdinɗo.read, innde)

def winndude_fiilde(innde, keɓe):
    return 운영호출(yuɓɓo_kurdinɗo.write, innde, keɓe)

def ittude_fiilde(innde):
    return 운영호출(yuɓɓo_kurdinɗo.remove, innde)

def 전문통신열기(접속번호):
    return 운영호출(yuɓɓo_kurdinɗo.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, keɓe):
    return 운영호출(yuɓɓo_kurdinɗo.udp_send, 종단, 접속번호, keɓe)

def 바깥전문보내기(종단, ñiiɓirde, 접속번호, keɓe):
    return 운영호출(yuɓɓo_kurdinɗo.udp_sendto, 종단, ñiiɓirde, 접속번호, keɓe)

def 전문받기(종단):
    return 운영호출(yuɓɓo_kurdinɗo.udp_recv, 종단)

def uddude_laylaytol(종단):
    return 운영호출(yuɓɓo_kurdinɗo.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(yuɓɓo_kurdinɗo.rect, *인수)

def 화면크기():
    return 운영호출(yuɓɓo_kurdinɗo.screen_size)

def 그림기다리기():
    return 운영호출(yuɓɓo_kurdinɗo.wait_key)

밀리초 = yuɓɓo_kurdinɗo.ticks_ms
