"""자체 커널의 Datoteka·통신·화면 호출과 한국어 izuzetak. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operativni_sistem
import sys as CLR_komponenta

def 출력(*VALUE, razdelnik=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = razdelnik
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

ceo_broj = int
명령인수 = CLR_komponenta.argv
다시시도오류 = 11

class sistem_greška(OSError):
    def __init__(자신, INDEX, 설명="operativni_sistem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *인수):
    try:
        return FUNCTION_VALUE(*인수)
    except OSError as greška:
        INDEX = greška.args[0] if greška.args else 0
        raise sistem_greška(INDEX)

def kodirati_SMS(SMS):
    return SMS.encode("utf-8")

def 글해독(podaci):
    return podaci.decode("utf-8")

def 파일읽기(ime):
    return 운영호출(operativni_sistem.read, ime)

def 파일쓰기(ime, podaci):
    return 운영호출(operativni_sistem.write, ime, podaci)

def ukloniti_Datoteka(ime):
    return 운영호출(operativni_sistem.remove, ime)

def otvoren_datagram(broj_porta):
    return 운영호출(operativni_sistem.udp_open, broj_porta)

def poslati_datagram(učesnik, broj_porta, podaci):
    return 운영호출(operativni_sistem.udp_send, učesnik, broj_porta, podaci)

def poslati_spoljni_datagram(učesnik, adresa, broj_porta, podaci):
    return 운영호출(operativni_sistem.udp_sendto, učesnik, adresa, broj_porta, podaci)

def primiti_datagram(učesnik):
    return 운영호출(operativni_sistem.udp_recv, učesnik)

def Zatvori_Mreža(učesnik):
    return 운영호출(operativni_sistem.udp_close, učesnik)

def 네모그리기(*인수):
    return 운영호출(operativni_sistem.rect, *인수)

def 화면크기():
    return 운영호출(operativni_sistem.screen_size)

def 그림기다리기():
    return 운영호출(operativni_sistem.wait_key)

밀리초 = operativni_sistem.ticks_ms
