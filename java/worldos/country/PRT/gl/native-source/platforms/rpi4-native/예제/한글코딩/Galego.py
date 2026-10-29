"""자체 kernel_VALOR MicroPython에서 사용하는 한글 FUNCIÓN_VALOR Nome."""
import jkoros as sistema_operativo
Saída = print
파일읽기 = sistema_operativo.read
escribir_Ficheiro = sistema_operativo.write
eliminar_Ficheiro = sistema_operativo.remove
입력읽기 = sistema_operativo.stdin
네모그리기 = sistema_operativo.rect
그림기다리기 = sistema_operativo.wait_key
밀리초 = sistema_operativo.ticks_ms
전문통신열기 = sistema_operativo.udp_open
전문보내기 = sistema_operativo.udp_send
바깥전문보내기 = sistema_operativo.udp_sendto
전문받기 = sistema_operativo.udp_recv
peche_Rede = sistema_operativo.udp_close

def 글해독(datos):
    return datos.decode("utf-8")
