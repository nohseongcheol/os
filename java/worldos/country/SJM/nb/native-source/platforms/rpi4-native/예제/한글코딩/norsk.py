"""eget kjerne_VERDI MicroPython에서 사용하는 한글 FUNKSJON_VERDI Navn."""
import jkoros as operativsystem
Utgang = print
파일읽기 = operativsystem.read
skrive_Fil = operativsystem.write
fjerne_Fil = operativsystem.remove
입력읽기 = operativsystem.stdin
Tegn_rektangel = operativsystem.rect
그림기다리기 = operativsystem.wait_key
밀리초 = operativsystem.ticks_ms
åpen_datagram = operativsystem.udp_open
sende_datagram = operativsystem.udp_send
sende_ekstern_datagram = operativsystem.udp_sendto
motta_datagram = operativsystem.udp_recv
Lukk_nettverk = operativsystem.udp_close

def 글해독(data):
    return data.decode("utf-8")
