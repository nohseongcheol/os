"""자체 커널의 Fayl·통신·화면 호출과 한국어 istisno. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operatsion_tizim
import sys as umumiy_til_ish_jarayoni

def 출력(*VALUE, ajratgich=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ajratgich
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

butun_son = int
명령인수 = umumiy_til_ish_jarayoni.argv
다시시도오류 = 11

class tizim_xato(OSError):
    def __init__(자신, INDEX, 설명="operatsion_tizim 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *인수):
    try:
        return FUNCTION_VALUE(*인수)
    except OSError as Xato:
        INDEX = Xato.args[0] if Xato.args else 0
        raise tizim_xato(INDEX)

def 글부호화(Matn):
    return Matn.encode("utf-8")

def 글해독(ma_lumotlar):
    return ma_lumotlar.decode("utf-8")

def 파일읽기(Nomi):
    return 운영호출(operatsion_tizim.read, Nomi)

def yozmoq_fayl(Nomi, ma_lumotlar):
    return 운영호출(operatsion_tizim.write, Nomi, ma_lumotlar)

def olib_tashlamoq_fayl(Nomi):
    return 운영호출(operatsion_tizim.remove, Nomi)

def 전문통신열기(접속번호):
    return 운영호출(operatsion_tizim.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, ma_lumotlar):
    return 운영호출(operatsion_tizim.udp_send, 종단, 접속번호, ma_lumotlar)

def 바깥전문보내기(종단, manzil, 접속번호, ma_lumotlar):
    return 운영호출(operatsion_tizim.udp_sendto, 종단, manzil, 접속번호, ma_lumotlar)

def 전문받기(종단):
    return 운영호출(operatsion_tizim.udp_recv, 종단)

def yopmoq_Tarmoq(종단):
    return 운영호출(operatsion_tizim.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(operatsion_tizim.rect, *인수)

def 화면크기():
    return 운영호출(operatsion_tizim.screen_size)

def 그림기다리기():
    return 운영호출(operatsion_tizim.wait_key)

밀리초 = operatsion_tizim.ticks_ms
