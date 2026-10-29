"""vlastiti jezgra_sustava_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Ime."""
import jkoros as operacijski_sustav
Izlaz = print
파일읽기 = operacijski_sustav.read
zapisivanje_Datoteka = operacijski_sustav.write
ukloniti_Datoteka = operacijski_sustav.remove
입력읽기 = operacijski_sustav.stdin
Crtanje_pravokutnik = operacijski_sustav.rect
그림기다리기 = operacijski_sustav.wait_key
밀리초 = operacijski_sustav.ticks_ms
otvoreno_datogram = operacijski_sustav.udp_open
slati_datogram = operacijski_sustav.udp_send
slati_vanjski_datogram = operacijski_sustav.udp_sendto
primiti_datogram = operacijski_sustav.udp_recv
Zatvori_mreža = operacijski_sustav.udp_close

def 글해독(podaci):
    return podaci.decode("utf-8")
