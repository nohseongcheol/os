"""자체 intima_agaciro MicroPython에서 사용하는 한글 FUNCTION_agaciro Izina."""
import jkoros as sisitemu_ngengamikorere
출력 = print
파일읽기 = sisitemu_ngengamikorere.read
kwandika_dosiye = sisitemu_ngengamikorere.write
gukuramo_dosiye = sisitemu_ngengamikorere.remove
입력읽기 = sisitemu_ngengamikorere.stdin
네모그리기 = sisitemu_ngengamikorere.rect
그림기다리기 = sisitemu_ngengamikorere.wait_key
밀리초 = sisitemu_ngengamikorere.ticks_ms
전문통신열기 = sisitemu_ngengamikorere.udp_open
전문보내기 = sisitemu_ngengamikorere.udp_send
바깥전문보내기 = sisitemu_ngengamikorere.udp_sendto
전문받기 = sisitemu_ngengamikorere.udp_recv
gufunga_Urusobemiyoboro = sisitemu_ngengamikorere.udp_close

def 글해독(amakurushingiro):
    return amakurushingiro.decode("utf-8")
