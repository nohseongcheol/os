"""oma 커널의 tiedoston_nimi·통신·화면 호출과 suomi poikkeus. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as käyttöjärjestelmä
import sys as CLR

def tulostuspaikka(*ARVO, erotin=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = erotin
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*ARVO, **기존인수)

kokonaisluku = int
명령인수 = CLR.argv
다시시도오류 = 11

class järjestelmävirhe(OSError):
    def __init__(자신, INDEKSI, 설명="käyttöjärjestelmä 작업에 실패했습니다."):
        super().__init__(INDEKSI, 설명)
        자신.INDEKSI = INDEKSI
        자신.설명 = 설명

def 운영호출(funktio_ARVO, *argumentit):
    try:
        return funktio_ARVO(*argumentit)
    except OSError as VIRHE:
        INDEKSI = VIRHE.args[0] if VIRHE.args else 0
        raise järjestelmävirhe(INDEKSI)

def koodata_SMS(teksti):
    return teksti.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def lukea_Tiedosto(Nimi):
    return 운영호출(käyttöjärjestelmä.read, Nimi)

def kirjoitus_Tiedosto(Nimi, data):
    return 운영호출(käyttöjärjestelmä.write, Nimi, data)

def poistaa_Tiedosto(Nimi):
    return 운영호출(käyttöjärjestelmä.remove, Nimi)

def avata_datagrammi(portin_numero):
    return 운영호출(käyttöjärjestelmä.udp_open, portin_numero)

def lähettää_datagrammi(päätepiste, portin_numero, data):
    return 운영호출(käyttöjärjestelmä.udp_send, päätepiste, portin_numero, data)

def lähettää_ulkoinen_datagrammi(päätepiste, OSOITE, portin_numero, data):
    return 운영호출(käyttöjärjestelmä.udp_sendto, päätepiste, OSOITE, portin_numero, data)

def saada_datagrammi(päätepiste):
    return 운영호출(käyttöjärjestelmä.udp_recv, päätepiste)

def Sulje_verkko(päätepiste):
    return 운영호출(käyttöjärjestelmä.udp_close, päätepiste)

def Piirrä_suorakulmio(*argumentit):
    return 운영호출(käyttöjärjestelmä.rect, *argumentit)

def 화면크기():
    return 운영호출(käyttöjärjestelmä.screen_size)

def 그림기다리기():
    return 운영호출(käyttöjärjestelmä.wait_key)

밀리초 = käyttöjärjestelmä.ticks_ms
