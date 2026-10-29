"""자체 kjerne_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Namn."""
import jkoros as operativsystem
Utdata = print
파일읽기 = operativsystem.read
skrive_fil = operativsystem.write
fjerne_fil = operativsystem.remove
입력읽기 = operativsystem.stdin
네모그리기 = operativsystem.rect
그림기다리기 = operativsystem.wait_key
밀리초 = operativsystem.ticks_ms
전문통신열기 = operativsystem.udp_open
전문보내기 = operativsystem.udp_send
바깥전문보내기 = operativsystem.udp_sendto
전문받기 = operativsystem.udp_recv
Lukk_Nettverk = operativsystem.udp_close

def 글해독(data):
    return data.decode("utf-8")
