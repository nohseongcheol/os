"""saját kernel_ÉRTÉK MicroPython에서 사용하는 한글 FÜGGVÉNY_ÉRTÉK Név."""
import jkoros as operációs_rendszer
Kimenet = print
파일읽기 = operációs_rendszer.read
ír_Fájl = operációs_rendszer.write
eltávolít_Fájl = operációs_rendszer.remove
입력읽기 = operációs_rendszer.stdin
Rajz_téglalap = operációs_rendszer.rect
그림기다리기 = operációs_rendszer.wait_key
밀리초 = operációs_rendszer.ticks_ms
készít_datagram = operációs_rendszer.udp_open
küld_datagram = operációs_rendszer.udp_send
küld_külső_datagram = operációs_rendszer.udp_sendto
fogad_datagram = operációs_rendszer.udp_recv
bezár_hálózat = operációs_rendszer.udp_close

def 글해독(adat):
    return adat.decode("utf-8")
