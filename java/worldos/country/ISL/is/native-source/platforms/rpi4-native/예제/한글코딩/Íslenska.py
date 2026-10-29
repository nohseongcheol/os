"""eigin kjarni_VALUE MicroPython에서 사용하는 한글 fall_VALUE Heiti."""
import jkoros as stýrikerfi
úttak = print
파일읽기 = stýrikerfi.read
skrifa_skrá = stýrikerfi.write
fjarlægja_skrá = stýrikerfi.remove
입력읽기 = stýrikerfi.stdin
네모그리기 = stýrikerfi.rect
그림기다리기 = stýrikerfi.wait_key
밀리초 = stýrikerfi.ticks_ms
전문통신열기 = stýrikerfi.udp_open
전문보내기 = stýrikerfi.udp_send
바깥전문보내기 = stýrikerfi.udp_sendto
전문받기 = stýrikerfi.udp_recv
loka_Net = stýrikerfi.udp_close

def 글해독(gögn):
    return gögn.decode("utf-8")
