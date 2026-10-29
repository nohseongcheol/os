"""자체 ýadro_baha MicroPython에서 사용하는 한글 FUNCTION_baha Ad."""
import jkoros as operasiýa_ulgamy
출력 = print
파일읽기 = operasiýa_ulgamy.read
ýaz_faýl = operasiýa_ulgamy.write
aýyr_faýl = operasiýa_ulgamy.remove
입력읽기 = operasiýa_ulgamy.stdin
네모그리기 = operasiýa_ulgamy.rect
그림기다리기 = operasiýa_ulgamy.wait_key
밀리초 = operasiýa_ulgamy.ticks_ms
전문통신열기 = operasiýa_ulgamy.udp_open
전문보내기 = operasiýa_ulgamy.udp_send
바깥전문보내기 = operasiýa_ulgamy.udp_sendto
전문받기 = operasiýa_ulgamy.udp_recv
ýap_Tor = operasiýa_ulgamy.udp_close

def 글해독(maglumat):
    return maglumat.decode("utf-8")
