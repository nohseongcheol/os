"""자체 kernel_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE isem."""
import jkoros as sistema_operattiva
출력 = print
파일읽기 = sistema_operattiva.read
kiteb_fajl = sistema_operattiva.write
neħħa_fajl = sistema_operattiva.remove
입력읽기 = sistema_operattiva.stdin
네모그리기 = sistema_operattiva.rect
그림기다리기 = sistema_operattiva.wait_key
밀리초 = sistema_operattiva.ticks_ms
전문통신열기 = sistema_operattiva.udp_open
전문보내기 = sistema_operattiva.udp_send
바깥전문보내기 = sistema_operattiva.udp_sendto
전문받기 = sistema_operattiva.udp_recv
agħlaq_netwerk = sistema_operattiva.udp_close

def 글해독(data):
    return data.decode("utf-8")
