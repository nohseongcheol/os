"""자체 커널의 ini·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as qarasaujakkut_aulattijjut
import sys as 실행환경

def 출력(*atuutilik, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*atuutilik, **기존인수)

naasaut = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class qarasaujaq_tammarniq(OSError):
    def __init__(자신, nalunaiqsimavik, 설명="qarasaujakkut_aulattijjut 작업에 실패했습니다."):
        super().__init__(nalunaiqsimavik, 설명)
        자신.nalunaiqsimavik = nalunaiqsimavik
        자신.설명 = 설명

def 운영호출(sugiakkannirut_atuutilik, *인수):
    try:
        return sugiakkannirut_atuutilik(*인수)
    except OSError as tammarniq:
        nalunaiqsimavik = tammarniq.args[0] if tammarniq.args else 0
        raise qarasaujaq_tammarniq(nalunaiqsimavik)

def 글부호화(titiqqaq):
    return titiqqaq.encode("utf-8")

def 글해독(titiqqat):
    return titiqqat.decode("utf-8")

def 파일읽기(atiq):
    return 운영호출(qarasaujakkut_aulattijjut.read, atiq)

def titiraq_ini(atiq, titiqqat):
    return 운영호출(qarasaujakkut_aulattijjut.write, atiq, titiqqat)

def sanirvalli_ini(atiq):
    return 운영호출(qarasaujakkut_aulattijjut.remove, atiq)

def 전문통신열기(접속번호):
    return 운영호출(qarasaujakkut_aulattijjut.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, titiqqat):
    return 운영호출(qarasaujakkut_aulattijjut.udp_send, 종단, 접속번호, titiqqat)

def 바깥전문보내기(종단, turaarut, 접속번호, titiqqat):
    return 운영호출(qarasaujakkut_aulattijjut.udp_sendto, 종단, turaarut, 접속번호, titiqqat)

def 전문받기(종단):
    return 운영호출(qarasaujakkut_aulattijjut.udp_recv, 종단)

def matuli_Kasuqatigiitsimajut(종단):
    return 운영호출(qarasaujakkut_aulattijjut.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(qarasaujakkut_aulattijjut.rect, *인수)

def 화면크기():
    return 운영호출(qarasaujakkut_aulattijjut.screen_size)

def 그림기다리기():
    return 운영호출(qarasaujakkut_aulattijjut.wait_key)

밀리초 = qarasaujakkut_aulattijjut.ticks_ms
