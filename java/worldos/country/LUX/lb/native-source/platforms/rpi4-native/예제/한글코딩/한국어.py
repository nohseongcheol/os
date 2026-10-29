"""자체 Kernel_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Numm."""
import jkoros as Betribssystem
출력 = print
파일읽기 = Betribssystem.read
schreiwen_Fichier = Betribssystem.write
ewechhuelen_Fichier = Betribssystem.remove
입력읽기 = Betribssystem.stdin
네모그리기 = Betribssystem.rect
그림기다리기 = Betribssystem.wait_key
밀리초 = Betribssystem.ticks_ms
전문통신열기 = Betribssystem.udp_open
전문보내기 = Betribssystem.udp_send
바깥전문보내기 = Betribssystem.udp_sendto
전문받기 = Betribssystem.udp_recv
Clôture_Reseau = Betribssystem.udp_close

def 글해독(Daten):
    return Daten.decode("utf-8")
