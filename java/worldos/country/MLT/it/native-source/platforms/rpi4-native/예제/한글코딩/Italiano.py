"""nativo kernel_VALORE MicroPython에서 사용하는 한글 FUNZIONE_VALORE Nome."""
import jkoros as sistema_operativo
uscitaTesto = print
파일읽기 = sistema_operativo.read
scrivere_File = sistema_operativo.write
rimuovere_File = sistema_operativo.remove
입력읽기 = sistema_operativo.stdin
Disegno_rettangolo = sistema_operativo.rect
그림기다리기 = sistema_operativo.wait_key
밀리초 = sistema_operativo.ticks_ms
aperto_datagramma = sistema_operativo.udp_open
inviare_datagramma = sistema_operativo.udp_send
inviare_esterno_datagramma = sistema_operativo.udp_sendto
ricevere_datagramma = sistema_operativo.udp_recv
Chiudi_rete = sistema_operativo.udp_close

def 글해독(dati):
    return dati.decode("utf-8")
