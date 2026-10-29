"""자체 kernel_VALUE MicroPython에서 사용하는 한글 pormula_VALUE pangalan."""
import jkoros as operating_system
출력 = print
파일읽기 = operating_system.read
sumulat_file = operating_system.write
tanggalin_file = operating_system.remove
입력읽기 = operating_system.stdin
네모그리기 = operating_system.rect
그림기다리기 = operating_system.wait_key
밀리초 = operating_system.ticks_ms
전문통신열기 = operating_system.udp_open
전문보내기 = operating_system.udp_send
바깥전문보내기 = operating_system.udp_sendto
전문받기 = operating_system.udp_recv
isara_Network = operating_system.udp_close

def 글해독(data):
    return data.decode("utf-8")
