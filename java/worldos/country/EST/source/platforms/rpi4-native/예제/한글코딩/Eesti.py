"""oma tuum_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Nimi_2."""
import jkoros as operatsioonisüsteem
Väljund = print
파일읽기 = operatsioonisüsteem.read
kirjutamine_Fail = operatsioonisüsteem.write
eemaldama_Fail = operatsioonisüsteem.remove
입력읽기 = operatsioonisüsteem.stdin
Joonista_ristkülik = operatsioonisüsteem.rect
그림기다리기 = operatsioonisüsteem.wait_key
밀리초 = operatsioonisüsteem.ticks_ms
avama_datagramm = operatsioonisüsteem.udp_open
saatma_datagramm = operatsioonisüsteem.udp_send
saatma_väline_datagramm = operatsioonisüsteem.udp_sendto
saama_datagramm = operatsioonisüsteem.udp_recv
Sule_võrk = operatsioonisüsteem.udp_close

def 글해독(andmed):
    return andmed.decode("utf-8")
