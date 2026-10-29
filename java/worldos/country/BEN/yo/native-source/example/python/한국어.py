"""자체 커널의 Fáìlì·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as OS
import sys as àkókò_iṣẹ́_èdè_tówọ́pọ̀

def 출력(*iye, ayàsọ́tọ̀=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ayàsọ́tọ̀
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*iye, **기존인수)

nọ́ńbà_odindi = int
명령인수 = àkókò_iṣẹ́_èdè_tówọ́pọ̀.argv
다시시도오류 = 11

class ètò_àṣìṣe(OSError):
    def __init__(자신, wá_atọ̀ka_àkóónú, 설명="OS 작업에 실패했습니다."):
        super().__init__(wá_atọ̀ka_àkóónú, 설명)
        자신.wá_atọ̀ka_àkóónú = wá_atọ̀ka_àkóónú
        자신.설명 = 설명

def 운영호출(ÀKÀNṢEFỌMÚLÀ_iye, *인수):
    try:
        return ÀKÀNṢEFỌMÚLÀ_iye(*인수)
    except OSError as àṣìṣe:
        wá_atọ̀ka_àkóónú = àṣìṣe.args[0] if àṣìṣe.args else 0
        raise ètò_àṣìṣe(wá_atọ̀ka_àkóónú)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(détà):
    return détà.decode("utf-8")

def 파일읽기(Orúkọ):
    return 운영호출(OS.read, Orúkọ)

def kọ_fáìlì(Orúkọ, détà):
    return 운영호출(OS.write, Orúkọ, détà)

def ṣèmúkúro_fáìlì(Orúkọ):
    return 운영호출(OS.remove, Orúkọ)

def 전문통신열기(접속번호):
    return 운영호출(OS.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, détà):
    return 운영호출(OS.udp_send, 종단, 접속번호, détà)

def 바깥전문보내기(종단, àdírẹ́ẹ̀sì, 접속번호, détà):
    return 운영호출(OS.udp_sendto, 종단, àdírẹ́ẹ̀sì, 접속번호, détà)

def 전문받기(종단):
    return 운영호출(OS.udp_recv, 종단)

def pa_dé_Alásopọ̀(종단):
    return 운영호출(OS.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(OS.rect, *인수)

def 화면크기():
    return 운영호출(OS.screen_size)

def 그림기다리기():
    return 운영호출(OS.wait_key)

밀리초 = OS.ticks_ms
