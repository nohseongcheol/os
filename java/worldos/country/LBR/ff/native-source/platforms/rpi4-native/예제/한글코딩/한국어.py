"""자체 aaluude_njaru MicroPython에서 사용하는 한글 juɓɓol_njaru innde."""
import jkoros as yuɓɓo_kurdinɗo
출력 = print
파일읽기 = yuɓɓo_kurdinɗo.read
winndude_fiilde = yuɓɓo_kurdinɗo.write
ittude_fiilde = yuɓɓo_kurdinɗo.remove
입력읽기 = yuɓɓo_kurdinɗo.stdin
네모그리기 = yuɓɓo_kurdinɗo.rect
그림기다리기 = yuɓɓo_kurdinɗo.wait_key
밀리초 = yuɓɓo_kurdinɗo.ticks_ms
전문통신열기 = yuɓɓo_kurdinɗo.udp_open
전문보내기 = yuɓɓo_kurdinɗo.udp_send
바깥전문보내기 = yuɓɓo_kurdinɗo.udp_sendto
전문받기 = yuɓɓo_kurdinɗo.udp_recv
uddude_laylaytol = yuɓɓo_kurdinɗo.udp_close

def 글해독(keɓe):
    return keɓe.decode("utf-8")
