"""자체 커널의 faele·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as Tsamaisotiriso
import sys as nakotsamaiso_ya_puo_e_e_tlwaelegileng

def 출력(*Boleng, searoganyi=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = searoganyi
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*Boleng, **기존인수)

Palotlalo = int
명령인수 = nakotsamaiso_ya_puo_e_e_tlwaelegileng.argv
다시시도오류 = 11

class tsamaiso_phoso(OSError):
    def __init__(자신, tshupane, 설명="Tsamaisotiriso 작업에 실패했습니다."):
        super().__init__(tshupane, 설명)
        자신.tshupane = tshupane
        자신.설명 = 설명

def 운영호출(TIRISO_Boleng, *인수):
    try:
        return TIRISO_Boleng(*인수)
    except OSError as phoso:
        tshupane = phoso.args[0] if phoso.args else 0
        raise tsamaiso_phoso(tshupane)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(tshedimosetso):
    return tshedimosetso.decode("utf-8")

def 파일읽기(leina):
    return 운영호출(Tsamaisotiriso.read, leina)

def kwala_faele(leina, tshedimosetso):
    return 운영호출(Tsamaisotiriso.write, leina, tshedimosetso)

def tlosa_faele(leina):
    return 운영호출(Tsamaisotiriso.remove, leina)

def 전문통신열기(접속번호):
    return 운영호출(Tsamaisotiriso.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, tshedimosetso):
    return 운영호출(Tsamaisotiriso.udp_send, 종단, 접속번호, tshedimosetso)

def 바깥전문보내기(종단, aterese, 접속번호, tshedimosetso):
    return 운영호출(Tsamaisotiriso.udp_sendto, 종단, aterese, 접속번호, tshedimosetso)

def 전문받기(종단):
    return 운영호출(Tsamaisotiriso.udp_recv, 종단)

def tswala_Neteweke(종단):
    return 운영호출(Tsamaisotiriso.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(Tsamaisotiriso.rect, *인수)

def 화면크기():
    return 운영호출(Tsamaisotiriso.screen_size)

def 그림기다리기():
    return 운영호출(Tsamaisotiriso.wait_key)

밀리초 = Tsamaisotiriso.ticks_ms
