"""자체 o_zak_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Nomi."""
import jkoros as operatsion_tizim
출력 = print
파일읽기 = operatsion_tizim.read
yozmoq_fayl = operatsion_tizim.write
olib_tashlamoq_fayl = operatsion_tizim.remove
입력읽기 = operatsion_tizim.stdin
네모그리기 = operatsion_tizim.rect
그림기다리기 = operatsion_tizim.wait_key
밀리초 = operatsion_tizim.ticks_ms
전문통신열기 = operatsion_tizim.udp_open
전문보내기 = operatsion_tizim.udp_send
바깥전문보내기 = operatsion_tizim.udp_sendto
전문받기 = operatsion_tizim.udp_recv
yopmoq_Tarmoq = operatsion_tizim.udp_close

def 글해독(ma_lumotlar):
    return ma_lumotlar.decode("utf-8")
