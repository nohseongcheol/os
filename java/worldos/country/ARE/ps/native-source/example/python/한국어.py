"""자체 커널의 دوتنه·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as چليز_غونډال
import sys as 실행환경

def 출력(*ارزښت, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*ارزښت, **기존인수)

صحيح_عدد = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class غونډال_تېروتنه(OSError):
    def __init__(자신, لړیال, 설명="چليز_غونډال 작업에 실패했습니다."):
        super().__init__(لړیال, 설명)
        자신.لړیال = لړیال
        자신.설명 = 설명

def 운영호출(함수, *인수):
    try:
        return 함수(*인수)
    except OSError as تېروتنه:
        لړیال = تېروتنه.args[0] if تېروتنه.args else 0
        raise غونډال_تېروتنه(لړیال)

def 글부호화(ليکنه):
    return ليکنه.encode("utf-8")

def 글해독(اومتوک):
    return اومتوک.decode("utf-8")

def 파일읽기(نوم):
    return 운영호출(چليز_غونډال.read, نوم)

def ليکل_دوتنه(نوم, اومتوک):
    return 운영호출(چليز_غونډال.write, نوم, اومتوک)

def 파일지우기(نوم):
    return 운영호출(چليز_غونډال.remove, نوم)

def 전문통신열기(접속번호):
    return 운영호출(چليز_غونډال.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, اومتوک):
    return 운영호출(چليز_غونډال.udp_send, 종단, 접속번호, اومتوک)

def 바깥전문보내기(종단, پته, 접속번호, اومتوک):
    return 운영호출(چليز_غونډال.udp_sendto, 종단, پته, 접속번호, اومتوک)

def 전문받기(종단):
    return 운영호출(چليز_غونډال.udp_recv, 종단)

def بندول_جال(종단):
    return 운영호출(چليز_غونډال.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(چليز_غونډال.rect, *인수)

def 화면크기():
    return 운영호출(چليز_غونډال.screen_size)

def 그림기다리기():
    return 운영호출(چليز_غونډال.wait_key)

밀리초 = چليز_غونډال.ticks_ms
