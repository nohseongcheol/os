"""자체 kākano_uara_0611a8a8 MicroPython에서 사용하는 한글 TAUMAHI_uara Ingoa."""
import jkoros as pūnaha_mahi
출력 = print
파일읽기 = pūnaha_mahi.read
tuhi_kōnae = pūnaha_mahi.write
tango_kōnae = pūnaha_mahi.remove
입력읽기 = pūnaha_mahi.stdin
네모그리기 = pūnaha_mahi.rect
그림기다리기 = pūnaha_mahi.wait_key
밀리초 = pūnaha_mahi.ticks_ms
전문통신열기 = pūnaha_mahi.udp_open
전문보내기 = pūnaha_mahi.udp_send
바깥전문보내기 = pūnaha_mahi.udp_sendto
전문받기 = pūnaha_mahi.udp_recv
kati_whatunga = pūnaha_mahi.udp_close

def 글해독(raraunga):
    return raraunga.decode("utf-8")
