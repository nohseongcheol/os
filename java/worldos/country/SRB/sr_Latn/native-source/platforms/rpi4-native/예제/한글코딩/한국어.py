"""자체 jezgro_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE ime."""
import jkoros as operativni_sistem
출력 = print
파일읽기 = operativni_sistem.read
파일쓰기 = operativni_sistem.write
ukloniti_Datoteka = operativni_sistem.remove
입력읽기 = operativni_sistem.stdin
네모그리기 = operativni_sistem.rect
그림기다리기 = operativni_sistem.wait_key
밀리초 = operativni_sistem.ticks_ms
otvoren_datagram = operativni_sistem.udp_open
poslati_datagram = operativni_sistem.udp_send
poslati_spoljni_datagram = operativni_sistem.udp_sendto
primiti_datagram = operativni_sistem.udp_recv
Zatvori_Mreža = operativni_sistem.udp_close

def 글해독(podaci):
    return podaci.decode("utf-8")
