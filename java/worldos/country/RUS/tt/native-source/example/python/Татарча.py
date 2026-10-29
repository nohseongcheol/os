"""자체 커널의 Birem·통신·화면 호출과 Татарча 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as операцион_система
import sys as CLR_мохите

def 출력(*VALUE, аергыч=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = аергыч
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

бөтен_сан = int
명령인수 = CLR_мохите.argv
다시시도오류 = 11

class система_хата(OSError):
    def __init__(자신, INDEX, 설명="операцион_система 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(ФУНКЦИЯ_VALUE, *인수):
    try:
        return ФУНКЦИЯ_VALUE(*인수)
    except OSError as Хата:
        INDEX = Хата.args[0] if Хата.args else 0
        raise система_хата(INDEX)

def 글부호화(Mäten):
    return Mäten.encode("utf-8")

def 글해독(мәгълүмат):
    return мәгълүмат.decode("utf-8")

def 파일읽기(исем):
    return 운영호출(операцион_система.read, исем)

def язу_файл(исем, мәгълүмат):
    return 운영호출(операцион_система.write, исем, мәгълүмат)

def бетерү_файл(исем):
    return 운영호출(операцион_система.remove, исем)

def 전문통신열기(접속번호):
    return 운영호출(операцион_система.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, мәгълүмат):
    return 운영호출(операцион_система.udp_send, 종단, 접속번호, мәгълүмат)

def 바깥전문보내기(종단, адрес, 접속번호, мәгълүмат):
    return 운영호출(операцион_система.udp_sendto, 종단, адрес, 접속번호, мәгълүмат)

def 전문받기(종단):
    return 운영호출(операцион_система.udp_recv, 종단)

def чик_Челтәр(종단):
    return 운영호출(операцион_система.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(операцион_система.rect, *인수)

def 화면크기():
    return 운영호출(операцион_система.screen_size)

def 그림기다리기():
    return 운영호출(операцион_система.wait_key)

밀리초 = операцион_система.ticks_ms
