"""propi nucli_VALOR MicroPython에서 사용하는 한글 FUNCIÓ_VALOR Nom."""
import jkoros as sistema_operatiu
Sortida = print
tancar_arxiu = sistema_operatiu.read
escriure_arxiu = sistema_operatiu.write
suprimir_arxiu = sistema_operatiu.remove
입력읽기 = sistema_operatiu.stdin
네모그리기 = sistema_operatiu.rect
그림기다리기 = sistema_operatiu.wait_key
밀리초 = sistema_operatiu.ticks_ms
전문통신열기 = sistema_operatiu.udp_open
전문보내기 = sistema_operatiu.udp_send
바깥전문보내기 = sistema_operatiu.udp_sendto
전문받기 = sistema_operatiu.udp_recv
Tanca_xarxa = sistema_operatiu.udp_close

def 글해독(dades):
    return dades.decode("utf-8")
