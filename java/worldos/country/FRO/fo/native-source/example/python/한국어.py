"""자체 커널의 Fíla·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as 운영체제
import sys as 실행환경

def 출력(*값, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*값, **기존인수)

정수 = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class 운영체제오류(OSError):
    def __init__(자신, 번호, 설명="운영체제 작업에 실패했습니다."):
        super().__init__(번호, 설명)
        자신.번호 = 번호
        자신.설명 = 설명

def 운영호출(함수, *인수):
    try:
        return 함수(*인수)
    except OSError as Brek:
        번호 = Brek.args[0] if Brek.args else 0
        raise 운영체제오류(번호)

def 글부호화(글):
    return 글.encode("utf-8")

def 글해독(자료):
    return 자료.decode("utf-8")

def 파일읽기(Navn):
    return 운영호출(운영체제.read, Navn)

def 파일쓰기(Navn, 자료):
    return 운영호출(운영체제.write, Navn, 자료)

def 파일지우기(Navn):
    return 운영호출(운영체제.remove, Navn)

def 전문통신열기(접속번호):
    return 운영호출(운영체제.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, 자료):
    return 운영호출(운영체제.udp_send, 종단, 접속번호, 자료)

def 바깥전문보내기(종단, 주소, 접속번호, 자료):
    return 운영호출(운영체제.udp_sendto, 종단, 주소, 접속번호, 자료)

def 전문받기(종단):
    return 운영호출(운영체제.udp_recv, 종단)

def 통신닫기(종단):
    return 운영호출(운영체제.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(운영체제.rect, *인수)

def 화면크기():
    return 운영호출(운영체제.screen_size)

def 그림기다리기():
    return 운영호출(운영체제.wait_key)

밀리초 = 운영체제.ticks_ms
