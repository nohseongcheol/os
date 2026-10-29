"""vlastní 커널의 název_souboru·komunikace·화면 호출과 čeština výjimka. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operační_systém
import sys as CLR

def výstupní_pozice(*HODNOTA, oddělovač=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = oddělovač
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*HODNOTA, **기존인수)

integer = int
명령인수 = CLR.argv
다시시도오류 = 11

class chyba_systému(OSError):
    def __init__(자신, INDEX, 설명="operační_systém 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(funkce_HODNOTA, *argumenty):
    try:
        return funkce_HODNOTA(*argumenty)
    except OSError as chyba:
        INDEX = chyba.args[0] if chyba.args else 0
        raise chyba_systému(INDEX)

def kódovat_SMS(text):
    return text.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Název):
    return 운영호출(operační_systém.read, Název)

def zápis_Soubor(Název, data):
    return 운영호출(operační_systém.write, Název, data)

def odebrat_Soubor(Název):
    return 운영호출(operační_systém.remove, Název)

def otevřít_datagram(číslo_portu):
    return 운영호출(operační_systém.udp_open, číslo_portu)

def poslat_datagram(účastník, číslo_portu, data):
    return 운영호출(operační_systém.udp_send, účastník, číslo_portu, data)

def poslat_externí_datagram(účastník, Adresa, číslo_portu, data):
    return 운영호출(operační_systém.udp_sendto, účastník, Adresa, číslo_portu, data)

def dostat_datagram(účastník):
    return 운영호출(operační_systém.udp_recv, účastník)

def Zavřít_síť(účastník):
    return 운영호출(operační_systém.udp_close, účastník)

def kreslit_obdélník(*argumenty):
    return 운영호출(operační_systém.rect, *argumenty)

def 화면크기():
    return 운영호출(operační_systém.screen_size)

def 그림기다리기():
    return 운영호출(operační_systém.wait_key)

밀리초 = operační_systém.ticks_ms
