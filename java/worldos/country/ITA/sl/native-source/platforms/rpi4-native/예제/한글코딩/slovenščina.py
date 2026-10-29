"""lastno jedro_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Ime."""
import jkoros as operacijski_sistem
Izpis = print
파일읽기 = operacijski_sistem.read
pisati_Datoteka = operacijski_sistem.write
odstraniti_Datoteka = operacijski_sistem.remove
입력읽기 = operacijski_sistem.stdin
risati_pravokotnik = operacijski_sistem.rect
그림기다리기 = operacijski_sistem.wait_key
밀리초 = operacijski_sistem.ticks_ms
odprto_datagram = operacijski_sistem.udp_open
poslati_datagram = operacijski_sistem.udp_send
poslati_zunanji_datagram = operacijski_sistem.udp_sendto
sprejeti_sprejemati_prejeti_prejemati_datagram = operacijski_sistem.udp_recv
Zapri_mreža = operacijski_sistem.udp_close

def 글해독(podatki):
    return podatki.decode("utf-8")
