"""자체 kern_VALUE MicroPython에서 사용하는 한글 funksie_VALUE Naam."""
import jkoros as bedryfstelsel
Afvoer = print
파일읽기 = bedryfstelsel.read
skryf_lêer = bedryfstelsel.write
verwyder_lêer = bedryfstelsel.remove
입력읽기 = bedryfstelsel.stdin
네모그리기 = bedryfstelsel.rect
그림기다리기 = bedryfstelsel.wait_key
밀리초 = bedryfstelsel.ticks_ms
전문통신열기 = bedryfstelsel.udp_open
전문보내기 = bedryfstelsel.udp_send
바깥전문보내기 = bedryfstelsel.udp_sendto
전문받기 = bedryfstelsel.udp_recv
sluit_Netwerk = bedryfstelsel.udp_close

def 글해독(data):
    return data.decode("utf-8")
