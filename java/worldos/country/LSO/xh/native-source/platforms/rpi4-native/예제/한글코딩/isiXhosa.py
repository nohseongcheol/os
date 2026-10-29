"""자체 ikheneli_ixabiso MicroPython에서 사용하는 한글 INKQUBO_ixabiso Igama."""
import jkoros as Indlela_yokusebenza
출력 = print
파일읽기 = Indlela_yokusebenza.read
bhala_ifayile = Indlela_yokusebenza.write
shenxisa_ifayile = Indlela_yokusebenza.remove
입력읽기 = Indlela_yokusebenza.stdin
네모그리기 = Indlela_yokusebenza.rect
그림기다리기 = Indlela_yokusebenza.wait_key
밀리초 = Indlela_yokusebenza.ticks_ms
전문통신열기 = Indlela_yokusebenza.udp_open
전문보내기 = Indlela_yokusebenza.udp_send
바깥전문보내기 = Indlela_yokusebenza.udp_sendto
전문받기 = Indlela_yokusebenza.udp_recv
vala_Inethiwekhi = Indlela_yokusebenza.udp_close

def 글해독(iingcombolo):
    return iingcombolo.decode("utf-8")
