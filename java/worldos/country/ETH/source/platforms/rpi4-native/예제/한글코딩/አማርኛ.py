"""자체 ዓንኳር_እሴት MicroPython에서 사용하는 한글 ተግባር_እሴት ስም."""
import jkoros as ስርዓተ_ክወና
ውጤት = print
파일읽기 = ስርዓተ_ክወና.read
ጻፍ_ፋይል = ስርዓተ_ክወና.write
አስወግድ_ፋይል = ስርዓተ_ክወና.remove
입력읽기 = ስርዓተ_ክወና.stdin
네모그리기 = ስርዓተ_ክወና.rect
그림기다리기 = ስርዓተ_ክወና.wait_key
밀리초 = ስርዓተ_ክወና.ticks_ms
전문통신열기 = ስርዓተ_ክወና.udp_open
전문보내기 = ስርዓተ_ክወና.udp_send
바깥전문보내기 = ስርዓተ_ክወና.udp_sendto
전문받기 = ስርዓተ_ክወና.udp_recv
ዝጋ_መረብ = ስርዓተ_ክወና.udp_close

def 글해독(ውሂብ):
    return ውሂብ.decode("utf-8")
