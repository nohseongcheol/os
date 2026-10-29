"""Eigen kernel_WAARDE MicroPython에서 사용하는 한글 FUNCTIE_WAARDE Naam."""
import jkoros as besturingssysteem
tekstuitvoer = print
파일읽기 = besturingssysteem.read
schrijven_Bestand = besturingssysteem.write
verwijderen_Bestand = besturingssysteem.remove
입력읽기 = besturingssysteem.stdin
Tekenen_rechthoek = besturingssysteem.rect
그림기다리기 = besturingssysteem.wait_key
밀리초 = besturingssysteem.ticks_ms
open_datagram = besturingssysteem.udp_open
e_mailen_datagram = besturingssysteem.udp_send
e_mailen_extern_datagram = besturingssysteem.udp_sendto
ontvangen_datagram = besturingssysteem.udp_recv
Sluiten_net = besturingssysteem.udp_close

def 글해독(gegevens):
    return gegevens.decode("utf-8")
