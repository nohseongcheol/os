"""자체 khenele_boleng MicroPython에서 사용하는 한글 TIRO_boleng Leina."""
import jkoros as tshepedišotirišo
출력 = print
파일읽기 = tshepedišotirišo.read
ngwala_faele = tshepedišotirišo.write
tloša_faele = tshepedišotirišo.remove
입력읽기 = tshepedišotirišo.stdin
네모그리기 = tshepedišotirišo.rect
그림기다리기 = tshepedišotirišo.wait_key
밀리초 = tshepedišotirišo.ticks_ms
전문통신열기 = tshepedišotirišo.udp_open
전문보내기 = tshepedišotirišo.udp_send
바깥전문보내기 = tshepedišotirišo.udp_sendto
전문받기 = tshepedišotirišo.udp_recv
tswalela_Netweke = tshepedišotirišo.udp_close

def 글해독(data):
    return data.decode("utf-8")
