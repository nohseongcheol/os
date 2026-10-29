"""자체 커널의 Kōnae·통신·화면 호출과 Reo_Māori 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as pūnaha_mahi
import sys as wāhaere_reo_noa

def 출력(*uara, whakawehe=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = whakawehe
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*uara, **기존인수)

tau_tōpū = int
명령인수 = wāhaere_reo_noa.argv
다시시도오류 = 11

class pūnaha_hapa(OSError):
    def __init__(자신, INDEX, 설명="pūnaha_mahi 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(TAUMAHI_uara, *인수):
    try:
        return TAUMAHI_uara(*인수)
    except OSError as Pōhēhē:
        INDEX = Pōhēhē.args[0] if Pōhēhē.args else 0
        raise pūnaha_hapa(INDEX)

def 글부호화(Ngā_kupu):
    return Ngā_kupu.encode("utf-8")

def 글해독(raraunga):
    return raraunga.decode("utf-8")

def 파일읽기(Ingoa):
    return 운영호출(pūnaha_mahi.read, Ingoa)

def tuhi_kōnae(Ingoa, raraunga):
    return 운영호출(pūnaha_mahi.write, Ingoa, raraunga)

def tango_kōnae(Ingoa):
    return 운영호출(pūnaha_mahi.remove, Ingoa)

def 전문통신열기(접속번호):
    return 운영호출(pūnaha_mahi.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, raraunga):
    return 운영호출(pūnaha_mahi.udp_send, 종단, 접속번호, raraunga)

def 바깥전문보내기(종단, ADDRESS, 접속번호, raraunga):
    return 운영호출(pūnaha_mahi.udp_sendto, 종단, ADDRESS, 접속번호, raraunga)

def 전문받기(종단):
    return 운영호출(pūnaha_mahi.udp_recv, 종단)

def kati_whatunga(종단):
    return 운영호출(pūnaha_mahi.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(pūnaha_mahi.rect, *인수)

def 화면크기():
    return 운영호출(pūnaha_mahi.screen_size)

def 그림기다리기():
    return 운영호출(pūnaha_mahi.wait_key)

밀리초 = pūnaha_mahi.ticks_ms
