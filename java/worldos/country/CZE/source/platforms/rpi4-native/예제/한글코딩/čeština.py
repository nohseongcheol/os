"""vlastní jádro_HODNOTA MicroPython에서 사용하는 한글 funkce_HODNOTA Název."""
import jkoros as operační_systém
výstupní_pozice = print
파일읽기 = operační_systém.read
zápis_Soubor = operační_systém.write
odebrat_Soubor = operační_systém.remove
입력읽기 = operační_systém.stdin
kreslit_obdélník = operační_systém.rect
그림기다리기 = operační_systém.wait_key
밀리초 = operační_systém.ticks_ms
otevřít_datagram = operační_systém.udp_open
poslat_datagram = operační_systém.udp_send
poslat_externí_datagram = operační_systém.udp_sendto
dostat_datagram = operační_systém.udp_recv
Zavřít_síť = operační_systém.udp_close

def 글해독(data):
    return data.decode("utf-8")
