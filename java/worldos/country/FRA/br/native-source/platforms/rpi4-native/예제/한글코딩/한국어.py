"""자체 커널 MicroPython에서 사용하는 한글 함수 Anv."""
import jkoros as 운영체제
Ec_hankad = print
파일읽기 = 운영체제.read
파일쓰기 = 운영체제.write
파일지우기 = 운영체제.remove
입력읽기 = 운영체제.stdin
네모그리기 = 운영체제.rect
그림기다리기 = 운영체제.wait_key
밀리초 = 운영체제.ticks_ms
전문통신열기 = 운영체제.udp_open
전문보내기 = 운영체제.udp_send
바깥전문보내기 = 운영체제.udp_sendto
전문받기 = 운영체제.udp_recv
통신닫기 = 운영체제.udp_close

def 글해독(자료):
    return 자료.decode("utf-8")
