"""vlastné jadro_VALUE MicroPython에서 사용하는 한글 funkcia_VALUE Názov."""
import jkoros as operačný_systém
Výstup = print
파일읽기 = operačný_systém.read
zapísať_Súbor = operačný_systém.write
odobrať_Súbor = operačný_systém.remove
입력읽기 = operačný_systém.stdin
kresliť_obdĺžnik = operačný_systém.rect
그림기다리기 = operačný_systém.wait_key
밀리초 = operačný_systém.ticks_ms
otvoriť_datagram = operačný_systém.udp_open
odoslať_datagram = operačný_systém.udp_send
odoslať_externý_datagram = operačný_systém.udp_sendto
dostať_datagram = operačný_systém.udp_recv
Zavrieť_sieť = operačný_systém.udp_close

def 글해독(údaje):
    return údaje.decode("utf-8")
