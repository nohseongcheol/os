"""자체 bërthamë_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Emër."""
import jkoros as sistem_operativ
출력 = print
파일읽기 = sistem_operativ.read
shkruaj_skedar = sistem_operativ.write
heq_skedar = sistem_operativ.remove
입력읽기 = sistem_operativ.stdin
네모그리기 = sistem_operativ.rect
그림기다리기 = sistem_operativ.wait_key
밀리초 = sistem_operativ.ticks_ms
전문통신열기 = sistem_operativ.udp_open
전문보내기 = sistem_operativ.udp_send
바깥전문보내기 = sistem_operativ.udp_sendto
전문받기 = sistem_operativ.udp_recv
mbyll_rrjet = sistem_operativ.udp_close

def 글해독(të_dhëna):
    return të_dhëna.decode("utf-8")
