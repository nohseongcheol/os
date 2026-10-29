"""자체 cnewyllyn_VALUE MicroPython에서 사용하는 한글 SWYDDOGAETH_VALUE Enw."""
import jkoros as system_weithredu
Allbwn = print
파일읽기 = system_weithredu.read
ysgrifennu_ffeil = system_weithredu.write
tynnu_ffeil = system_weithredu.remove
입력읽기 = system_weithredu.stdin
네모그리기 = system_weithredu.rect
그림기다리기 = system_weithredu.wait_key
밀리초 = system_weithredu.ticks_ms
전문통신열기 = system_weithredu.udp_open
전문보내기 = system_weithredu.udp_send
바깥전문보내기 = system_weithredu.udp_sendto
전문받기 = system_weithredu.udp_recv
cau_Rhwydwaith = system_weithredu.udp_close

def 글해독(data):
    return data.decode("utf-8")
