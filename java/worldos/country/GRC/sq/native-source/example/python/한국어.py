"""자체 커널의 Kartelë·통신·화면 호출과 한국어 përjashtim. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistem_operativ
import sys as koha_e_ekzekutimit_të_gjuhës_së_zakonshme

def 출력(*VALUE, ndarësi=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ndarësi
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

numër_i_plotë = int
명령인수 = koha_e_ekzekutimit_të_gjuhës_së_zakonshme.argv
다시시도오류 = 11

class sistem_gabim(OSError):
    def __init__(자신, INDEX, 설명="sistem_operativ 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *Argumente):
    try:
        return FUNCTION_VALUE(*Argumente)
    except OSError as GABIM:
        INDEX = GABIM.args[0] if GABIM.args else 0
        raise sistem_gabim(INDEX)

def 글부호화(Teksti):
    return Teksti.encode("utf-8")

def 글해독(të_dhëna):
    return të_dhëna.decode("utf-8")

def 파일읽기(Emër):
    return 운영호출(sistem_operativ.read, Emër)

def shkruaj_skedar(Emër, të_dhëna):
    return 운영호출(sistem_operativ.write, Emër, të_dhëna)

def heq_skedar(Emër):
    return 운영호출(sistem_operativ.remove, Emër)

def 전문통신열기(numri_i_portës):
    return 운영호출(sistem_operativ.udp_open, numri_i_portës)

def 전문보내기(종단, numri_i_portës, të_dhëna):
    return 운영호출(sistem_operativ.udp_send, 종단, numri_i_portës, të_dhëna)

def 바깥전문보내기(종단, email, numri_i_portës, të_dhëna):
    return 운영호출(sistem_operativ.udp_sendto, 종단, email, numri_i_portës, të_dhëna)

def 전문받기(종단):
    return 운영호출(sistem_operativ.udp_recv, 종단)

def mbyll_rrjet(종단):
    return 운영호출(sistem_operativ.udp_close, 종단)

def 네모그리기(*Argumente):
    return 운영호출(sistem_operativ.rect, *Argumente)

def 화면크기():
    return 운영호출(sistem_operativ.screen_size)

def 그림기다리기():
    return 운영호출(sistem_operativ.wait_key)

밀리초 = sistem_operativ.ticks_ms
