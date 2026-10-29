"""eget kärna_värde MicroPython에서 사용하는 한글 FUNKTION_värde Namn."""
import jkoros as operativsystem
utmatningsposition = print
läsa_fil = operativsystem.read
skriva_fil = operativsystem.write
ta_bort_fil = operativsystem.remove
läsa_indata = operativsystem.stdin
Rita_rektangel = operativsystem.rect
그림기다리기 = operativsystem.wait_key
밀리초 = operativsystem.ticks_ms
skapa_datagram = operativsystem.udp_open
skicka_datagram = operativsystem.udp_send
skicka_extern_datagram = operativsystem.udp_sendto
få_datagram = operativsystem.udp_recv
Stäng_nätverk = operativsystem.udp_close

def 글해독(data):
    return data.decode("utf-8")
