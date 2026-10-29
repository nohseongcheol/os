"""자체 커널의 Faele·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as tshepedišotirišo
import sys as lebakanako_la_polelotlwaelwa

def 출력(*boleng, searoganyi=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = searoganyi
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*boleng, **기존인수)

palotlalo = int
명령인수 = lebakanako_la_polelotlwaelwa.argv
다시시도오류 = 11

class lenaneo_phošo(OSError):
    def __init__(자신, lokela, 설명="tshepedišotirišo 작업에 실패했습니다."):
        super().__init__(lokela, 설명)
        자신.lokela = lokela
        자신.설명 = 설명

def 운영호출(TIRO_boleng, *인수):
    try:
        return TIRO_boleng(*인수)
    except OSError as Phošo:
        lokela = Phošo.args[0] if Phošo.args else 0
        raise lenaneo_phošo(lokela)

def 글부호화(Sengwalwa):
    return Sengwalwa.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Leina):
    return 운영호출(tshepedišotirišo.read, Leina)

def ngwala_faele(Leina, data):
    return 운영호출(tshepedišotirišo.write, Leina, data)

def tloša_faele(Leina):
    return 운영호출(tshepedišotirišo.remove, Leina)

def 전문통신열기(접속번호):
    return 운영호출(tshepedišotirišo.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, data):
    return 운영호출(tshepedišotirišo.udp_send, 종단, 접속번호, data)

def 바깥전문보내기(종단, atrese, 접속번호, data):
    return 운영호출(tshepedišotirišo.udp_sendto, 종단, atrese, 접속번호, data)

def 전문받기(종단):
    return 운영호출(tshepedišotirišo.udp_recv, 종단)

def tswalela_Netweke(종단):
    return 운영호출(tshepedišotirišo.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(tshepedišotirišo.rect, *인수)

def 화면크기():
    return 운영호출(tshepedišotirišo.screen_size)

def 그림기다리기():
    return 운영호출(tshepedišotirišo.wait_key)

밀리초 = tshepedišotirišo.ticks_ms
