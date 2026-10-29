"""자체 커널의 Faýl·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operasiýa_ulgamy
import sys as umumy_dil_işlediş_gurşawy

def 출력(*baha, bölüji=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = bölüji
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*baha, **기존인수)

bitin = int
명령인수 = umumy_dil_işlediş_gurşawy.argv
다시시도오류 = 11

class ulgam_säwlik(OSError):
    def __init__(자신, indeks, 설명="operasiýa_ulgamy 작업에 실패했습니다."):
        super().__init__(indeks, 설명)
        자신.indeks = indeks
        자신.설명 = 설명

def 운영호출(FUNCTION_baha, *인수):
    try:
        return FUNCTION_baha(*인수)
    except OSError as Hata:
        indeks = Hata.args[0] if Hata.args else 0
        raise ulgam_säwlik(indeks)

def 글부호화(Metin):
    return Metin.encode("utf-8")

def 글해독(maglumat):
    return maglumat.decode("utf-8")

def 파일읽기(Ad):
    return 운영호출(operasiýa_ulgamy.read, Ad)

def ýaz_faýl(Ad, maglumat):
    return 운영호출(operasiýa_ulgamy.write, Ad, maglumat)

def aýyr_faýl(Ad):
    return 운영호출(operasiýa_ulgamy.remove, Ad)

def 전문통신열기(접속번호):
    return 운영호출(operasiýa_ulgamy.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, maglumat):
    return 운영호출(operasiýa_ulgamy.udp_send, 종단, 접속번호, maglumat)

def 바깥전문보내기(종단, salgy, 접속번호, maglumat):
    return 운영호출(operasiýa_ulgamy.udp_sendto, 종단, salgy, 접속번호, maglumat)

def 전문받기(종단):
    return 운영호출(operasiýa_ulgamy.udp_recv, 종단)

def ýap_Tor(종단):
    return 운영호출(operasiýa_ulgamy.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(operasiýa_ulgamy.rect, *인수)

def 화면크기():
    return 운영호출(operasiýa_ulgamy.screen_size)

def 그림기다리기():
    return 운영호출(operasiýa_ulgamy.wait_key)

밀리초 = operasiýa_ulgamy.ticks_ms
