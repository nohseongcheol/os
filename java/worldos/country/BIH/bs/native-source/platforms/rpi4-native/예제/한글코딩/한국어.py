"""자체 jezgro_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Naziv."""
import jkoros as operativni_sistem
Ispis = print
파일읽기 = operativni_sistem.read
pisati_fajl = operativni_sistem.write
ukloniti_fajl = operativni_sistem.remove
입력읽기 = operativni_sistem.stdin
네모그리기 = operativni_sistem.rect
그림기다리기 = operativni_sistem.wait_key
밀리초 = operativni_sistem.ticks_ms
전문통신열기 = operativni_sistem.udp_open
전문보내기 = operativni_sistem.udp_send
바깥전문보내기 = operativni_sistem.udp_sendto
전문받기 = operativni_sistem.udp_recv
zatvoriti_Mreža = operativni_sistem.udp_close

def 글해독(podaci):
    return podaci.decode("utf-8")
