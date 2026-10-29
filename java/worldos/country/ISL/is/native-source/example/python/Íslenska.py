"""eigin 커널의 Skrá·통신·화면 호출과 Íslenska undantekning. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as stýrikerfi
import sys as CLR

def úttak(*VALUE, skiltákn=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = skiltákn
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

heiltala = int
명령인수 = CLR.argv
다시시도오류 = 11

class kerfi_villa(OSError):
    def __init__(자신, INDEX, 설명="stýrikerfi 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(fall_VALUE, *Viðföng):
    try:
        return fall_VALUE(*Viðföng)
    except OSError as Villa:
        INDEX = Villa.args[0] if Villa.args else 0
        raise kerfi_villa(INDEX)

def 글부호화(Texti):
    return Texti.encode("utf-8")

def 글해독(gögn):
    return gögn.decode("utf-8")

def 파일읽기(Heiti):
    return 운영호출(stýrikerfi.read, Heiti)

def skrifa_skrá(Heiti, gögn):
    return 운영호출(stýrikerfi.write, Heiti, gögn)

def fjarlægja_skrá(Heiti):
    return 운영호출(stýrikerfi.remove, Heiti)

def 전문통신열기(tengisnúmer):
    return 운영호출(stýrikerfi.udp_open, tengisnúmer)

def 전문보내기(endastöð, tengisnúmer, gögn):
    return 운영호출(stýrikerfi.udp_send, endastöð, tengisnúmer, gögn)

def 바깥전문보내기(endastöð, slóð, tengisnúmer, gögn):
    return 운영호출(stýrikerfi.udp_sendto, endastöð, slóð, tengisnúmer, gögn)

def 전문받기(endastöð):
    return 운영호출(stýrikerfi.udp_recv, endastöð)

def loka_Net(endastöð):
    return 운영호출(stýrikerfi.udp_close, endastöð)

def 네모그리기(*Viðföng):
    return 운영호출(stýrikerfi.rect, *Viðföng)

def 화면크기():
    return 운영호출(stýrikerfi.screen_size)

def 그림기다리기():
    return 운영호출(stýrikerfi.wait_key)

밀리초 = stýrikerfi.ticks_ms
