"""자체 eithne_VALUE MicroPython에서 사용하는 한글 feidhm_VALUE Ainm."""
import jkoros as córas_oibriúcháin
Aschur = print
파일읽기 = córas_oibriúcháin.read
scríobh_comhad = córas_oibriúcháin.write
bain_comhad = córas_oibriúcháin.remove
입력읽기 = córas_oibriúcháin.stdin
네모그리기 = córas_oibriúcháin.rect
그림기다리기 = córas_oibriúcháin.wait_key
밀리초 = córas_oibriúcháin.ticks_ms
전문통신열기 = córas_oibriúcháin.udp_open
전문보내기 = córas_oibriúcháin.udp_send
바깥전문보내기 = córas_oibriúcháin.udp_sendto
전문받기 = córas_oibriúcháin.udp_recv
dún_Líonra = córas_oibriúcháin.udp_close

def 글해독(sonraí):
    return sonraí.decode("utf-8")
