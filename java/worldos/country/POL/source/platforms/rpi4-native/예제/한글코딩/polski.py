"""własny jądro_WARTOŚĆ MicroPython에서 사용하는 한글 FUNKCJA_WARTOŚĆ Nazwa."""
import jkoros as system_operacyjny
pozycja_wyjścia = print
파일읽기 = system_operacyjny.read
zapis_Plik = system_operacyjny.write
usuń_Plik = system_operacyjny.remove
입력읽기 = system_operacyjny.stdin
rysować_prostokąt = system_operacyjny.rect
그림기다리기 = system_operacyjny.wait_key
밀리초 = system_operacyjny.ticks_ms
otwarty_datagram = system_operacyjny.udp_open
wysłać_datagram = system_operacyjny.udp_send
wysłać_zewnętrzny_datagram = system_operacyjny.udp_sendto
odbierać_datagram = system_operacyjny.udp_recv
Zamknij_sieć = system_operacyjny.udp_close

def 글해독(dane):
    return dane.decode("utf-8")
