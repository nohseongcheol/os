"""자체 Khenele_Boleng MicroPython에서 사용하는 한글 TIRISO_Boleng leina."""
import jkoros as Tsamaisotiriso
출력 = print
파일읽기 = Tsamaisotiriso.read
kwala_faele = Tsamaisotiriso.write
tlosa_faele = Tsamaisotiriso.remove
입력읽기 = Tsamaisotiriso.stdin
네모그리기 = Tsamaisotiriso.rect
그림기다리기 = Tsamaisotiriso.wait_key
밀리초 = Tsamaisotiriso.ticks_ms
전문통신열기 = Tsamaisotiriso.udp_open
전문보내기 = Tsamaisotiriso.udp_send
바깥전문보내기 = Tsamaisotiriso.udp_sendto
전문받기 = Tsamaisotiriso.udp_recv
tswala_Neteweke = Tsamaisotiriso.udp_close

def 글해독(tshedimosetso):
    return tshedimosetso.decode("utf-8")
