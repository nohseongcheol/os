"""자체 nukleo_balio MicroPython에서 사용하는 한글 FUNTZIOA_balio Izena."""
import jkoros as sistema_eragile
Irteera = print
파일읽기 = sistema_eragile.read
idatzi_fitxategi = sistema_eragile.write
kendu_fitxategi = sistema_eragile.remove
입력읽기 = sistema_eragile.stdin
네모그리기 = sistema_eragile.rect
그림기다리기 = sistema_eragile.wait_key
밀리초 = sistema_eragile.ticks_ms
전문통신열기 = sistema_eragile.udp_open
전문보내기 = sistema_eragile.udp_send
바깥전문보내기 = sistema_eragile.udp_sendto
전문받기 = sistema_eragile.udp_recv
itxi_sare = sistema_eragile.udp_close

def 글해독(datuak):
    return datuak.decode("utf-8")
