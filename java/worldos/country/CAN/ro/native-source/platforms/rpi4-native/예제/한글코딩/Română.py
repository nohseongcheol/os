"""propriu nucleu_VALUE MicroPython에서 사용하는 한글 funcție_VALUE Nume."""
import jkoros as sistem_de_operare
Rezultat = print
파일읽기 = sistem_de_operare.read
scriere_Fișier = sistem_de_operare.write
elimina_Fișier = sistem_de_operare.remove
입력읽기 = sistem_de_operare.stdin
Desen_dreptunghi = sistem_de_operare.rect
그림기다리기 = sistem_de_operare.wait_key
밀리초 = sistem_de_operare.ticks_ms
crea_diagramă_informații = sistem_de_operare.udp_open
trimite_diagramă_informații = sistem_de_operare.udp_send
trimite_extern_diagramă_informații = sistem_de_operare.udp_sendto
primi_diagramă_informații = sistem_de_operare.udp_recv
închide_rețea = sistem_de_operare.udp_close

def 글해독(date):
    return date.decode("utf-8")
