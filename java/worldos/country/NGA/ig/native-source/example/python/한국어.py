"""자체 커널의 Faịlụ·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as OS
import sys as ọgịga_oge_otu_asụsụ

def 출력(*valuu, nkewa=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = nkewa
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*valuu, **기존인수)

ọnụọgụ_nzùrùòkè = int
명령인수 = ọgịga_oge_otu_asụsụ.argv
다시시도오류 = 11

class sistèm_mmejọ(OSError):
    def __init__(자신, indèks, 설명="OS 작업에 실패했습니다."):
        super().__init__(indèks, 설명)
        자신.indèks = indèks
        자신.설명 = 설명

def 운영호출(ọrụ_valuu, *인수):
    try:
        return ọrụ_valuu(*인수)
    except OSError as mmejọ:
        indèks = mmejọ.args[0] if mmejọ.args else 0
        raise sistèm_mmejọ(indèks)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(datà):
    return datà.decode("utf-8")

def 파일읽기(Aha):
    return 운영호출(OS.read, Aha)

def dee_ọbọakwụkwọ(Aha, datà):
    return 운영호출(OS.write, Aha, datà)

def wepụ_ọbọakwụkwọ(Aha):
    return 운영호출(OS.remove, Aha)

def 전문통신열기(접속번호):
    return 운영호출(OS.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, datà):
    return 운영호출(OS.udp_send, 종단, 접속번호, datà)

def 바깥전문보내기(종단, àdreèsì, 접속번호, datà):
    return 운영호출(OS.udp_sendto, 종단, àdreèsì, 접속번호, datà)

def 전문받기(종단):
    return 운영호출(OS.udp_recv, 종단)

def mmechi_Netwọọkụ(종단):
    return 운영호출(OS.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(OS.rect, *인수)

def 화면크기():
    return 운영호출(OS.screen_size)

def 그림기다리기():
    return 운영호출(OS.wait_key)

밀리초 = OS.ticks_ms
