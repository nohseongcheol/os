"""자체 ፍረ_ዋጋ MicroPython에서 사용하는 한글 ተግባር_ዋጋ ሽም."""
import jkoros as ስርዓት_ስርሒት
출력 = print
파일읽기 = ስርዓት_ስርሒት.read
ጸሓፍ_ፋይል = ስርዓት_ስርሒት.write
ኣልግስ_ፋይል = ስርዓት_ስርሒት.remove
입력읽기 = ስርዓት_ስርሒት.stdin
네모그리기 = ስርዓት_ስርሒት.rect
그림기다리기 = ስርዓት_ስርሒት.wait_key
밀리초 = ስርዓት_ስርሒት.ticks_ms
전문통신열기 = ስርዓት_ስርሒት.udp_open
전문보내기 = ስርዓት_ስርሒት.udp_send
바깥전문보내기 = ስርዓት_ስርሒት.udp_sendto
전문받기 = ስርዓት_ስርሒት.udp_recv
ዕጸው_ማሕበራዊ_ኔትወርክ = ስርዓት_ስርሒት.udp_close

def 글해독(ሓበሬታ):
    return ሓበሬታ.decode("utf-8")
