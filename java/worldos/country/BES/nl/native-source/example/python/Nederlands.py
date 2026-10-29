"""Eigen 커널의 bestand·communicatie·scherm 호출과 Nederlands uitzondering. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as besturingssysteem
import sys as CLR

def tekstuitvoer(*WAARDE, scheidingsbalk=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = scheidingsbalk
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*WAARDE, **기존인수)

geheel_getal = int
명령인수 = CLR.argv
다시시도오류 = 11

class systeemfout(OSError):
    def __init__(자신, INDEX, 설명="besturingssysteem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTIE_WAARDE, *argumenten):
    try:
        return FUNCTIE_WAARDE(*argumenten)
    except OSError as fout:
        INDEX = fout.args[0] if fout.args else 0
        raise systeemfout(INDEX)

def coderen_sms(tekst):
    return tekst.encode("utf-8")

def 글해독(gegevens):
    return gegevens.decode("utf-8")

def 파일읽기(Naam):
    return 운영호출(besturingssysteem.read, Naam)

def schrijven_Bestand(Naam, gegevens):
    return 운영호출(besturingssysteem.write, Naam, gegevens)

def verwijderen_Bestand(Naam):
    return 운영호출(besturingssysteem.remove, Naam)

def open_datagram(poortnummer):
    return 운영호출(besturingssysteem.udp_open, poortnummer)

def e_mailen_datagram(eindpunt, poortnummer, gegevens):
    return 운영호출(besturingssysteem.udp_send, eindpunt, poortnummer, gegevens)

def e_mailen_extern_datagram(eindpunt, ADRES, poortnummer, gegevens):
    return 운영호출(besturingssysteem.udp_sendto, eindpunt, ADRES, poortnummer, gegevens)

def ontvangen_datagram(eindpunt):
    return 운영호출(besturingssysteem.udp_recv, eindpunt)

def Sluiten_net(eindpunt):
    return 운영호출(besturingssysteem.udp_close, eindpunt)

def Tekenen_rechthoek(*argumenten):
    return 운영호출(besturingssysteem.rect, *argumenten)

def scherm_formaat_wijzigen():
    return 운영호출(besturingssysteem.screen_size)

def 그림기다리기():
    return 운영호출(besturingssysteem.wait_key)

밀리초 = besturingssysteem.ticks_ms
