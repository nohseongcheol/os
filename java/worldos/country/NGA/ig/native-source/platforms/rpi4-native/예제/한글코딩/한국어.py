"""자체 mkpụrụobī_kọmpùta_valuu MicroPython에서 사용하는 한글 ọrụ_valuu Aha."""
import jkoros as OS
출력 = print
파일읽기 = OS.read
dee_ọbọakwụkwọ = OS.write
wepụ_ọbọakwụkwọ = OS.remove
입력읽기 = OS.stdin
네모그리기 = OS.rect
그림기다리기 = OS.wait_key
밀리초 = OS.ticks_ms
전문통신열기 = OS.udp_open
전문보내기 = OS.udp_send
바깥전문보내기 = OS.udp_sendto
전문받기 = OS.udp_recv
mmechi_Netwọọkụ = OS.udp_close

def 글해독(datà):
    return datà.decode("utf-8")
