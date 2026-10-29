"""자체 커널의 bara_denc·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as doxalukaay
import sys as common_language_runtime

def 출력(*xëyma, xàjjalekat=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = xàjjalekat
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*xëyma, **기존인수)

lëmm = int
명령인수 = common_language_runtime.argv
다시시도오류 = 11

class kureel_njumte(OSError):
    def __init__(자신, àlluwa_tur, 설명="doxalukaay 작업에 실패했습니다."):
        super().__init__(àlluwa_tur, 설명)
        자신.àlluwa_tur = àlluwa_tur
        자신.설명 = 설명

def 운영호출(liëey_xëyma, *인수):
    try:
        return liëey_xëyma(*인수)
    except OSError as njumte:
        àlluwa_tur = njumte.args[0] if njumte.args else 0
        raise kureel_njumte(àlluwa_tur)

def 글부호화(Tekst):
    return Tekst.encode("utf-8")

def 글해독(mbir):
    return mbir.decode("utf-8")

def 파일읽기(tur_253d1510):
    return 운영호출(doxalukaay.read, tur_253d1510)

def biir_bara_denc(tur_253d1510, mbir):
    return 운영호출(doxalukaay.write, tur_253d1510, mbir)

def dandal_bara_denc(tur_253d1510):
    return 운영호출(doxalukaay.remove, tur_253d1510)

def 전문통신열기(접속번호):
    return 운영호출(doxalukaay.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, mbir):
    return 운영호출(doxalukaay.udp_send, 종단, 접속번호, mbir)

def 바깥전문보내기(종단, dëkkuwaay, 접속번호, mbir):
    return 운영호출(doxalukaay.udp_sendto, 종단, dëkkuwaay, 접속번호, mbir)

def 전문받기(종단):
    return 운영호출(doxalukaay.udp_recv, 종단)

def Tej_mbaal(종단):
    return 운영호출(doxalukaay.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(doxalukaay.rect, *인수)

def 화면크기():
    return 운영호출(doxalukaay.screen_size)

def 그림기다리기():
    return 운영호출(doxalukaay.wait_key)

밀리초 = doxalukaay.ticks_ms
