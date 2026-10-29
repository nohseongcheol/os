"""saját 커널의 Fájl·kommunikáció·화면 호출과 magyar kivétel. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operációs_rendszer
import sys as CLR

def Kimenet(*ÉRTÉK, elválasztó=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = elválasztó
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*ÉRTÉK, **기존인수)

egész_szám = int
명령인수 = CLR.argv
다시시도오류 = 11

class rendszerhiba(OSError):
    def __init__(자신, INDEX, 설명="operációs_rendszer 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FÜGGVÉNY_ÉRTÉK, *Argumentumok):
    try:
        return FÜGGVÉNY_ÉRTÉK(*Argumentumok)
    except OSError as HIBA:
        INDEX = HIBA.args[0] if HIBA.args else 0
        raise rendszerhiba(INDEX)

def kódolás_SMS(Szöveg):
    return Szöveg.encode("utf-8")

def 글해독(adat):
    return adat.decode("utf-8")

def 파일읽기(Név):
    return 운영호출(operációs_rendszer.read, Név)

def ír_Fájl(Név, adat):
    return 운영호출(operációs_rendszer.write, Név, adat)

def eltávolít_Fájl(Név):
    return 운영호출(operációs_rendszer.remove, Név)

def készít_datagram(portszám):
    return 운영호출(operációs_rendszer.udp_open, portszám)

def küld_datagram(végpont, portszám, adat):
    return 운영호출(operációs_rendszer.udp_send, végpont, portszám, adat)

def küld_külső_datagram(végpont, CÍM, portszám, adat):
    return 운영호출(operációs_rendszer.udp_sendto, végpont, CÍM, portszám, adat)

def fogad_datagram(végpont):
    return 운영호출(operációs_rendszer.udp_recv, végpont)

def bezár_hálózat(végpont):
    return 운영호출(operációs_rendszer.udp_close, végpont)

def Rajz_téglalap(*Argumentumok):
    return 운영호출(operációs_rendszer.rect, *Argumentumok)

def 화면크기():
    return 운영호출(operációs_rendszer.screen_size)

def 그림기다리기():
    return 운영호출(operációs_rendszer.wait_key)

밀리초 = operációs_rendszer.ticks_ms
