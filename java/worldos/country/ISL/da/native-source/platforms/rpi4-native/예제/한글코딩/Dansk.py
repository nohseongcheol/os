"""eget kerne_VÆRDI MicroPython에서 사용하는 한글 FUNKTION_VÆRDI Navn."""
import jkoros as operativsystem
Udgang = print
파일읽기 = operativsystem.read
skrive_fil = operativsystem.write
fjerne_fil = operativsystem.remove
입력읽기 = operativsystem.stdin
tegne_rektangel = operativsystem.rect
그림기다리기 = operativsystem.wait_key
밀리초 = operativsystem.ticks_ms
åben_datagram = operativsystem.udp_open
maile_datagram = operativsystem.udp_send
maile_ekstern_datagram = operativsystem.udp_sendto
modtage_datagram = operativsystem.udp_recv
Luk_netværk = operativsystem.udp_close

def 글해독(data):
    return data.decode("utf-8")
