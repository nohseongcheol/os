"""nativo 커널의 file·comunicazione·schermata 호출과 Italiano eccezione. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistema_operativo
import sys as CLR

def uscitaTesto(*VALORE, separatore=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = separatore
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALORE, **기존인수)

intero = int
명령인수 = CLR.argv
다시시도오류 = 11

class errore_di_sistema(OSError):
    def __init__(자신, INDICE, 설명="sistema_operativo 작업에 실패했습니다."):
        super().__init__(INDICE, 설명)
        자신.INDICE = INDICE
        자신.설명 = 설명

def 운영호출(FUNZIONE_VALORE, *argomenti):
    try:
        return FUNZIONE_VALORE(*argomenti)
    except OSError as errore:
        INDICE = errore.args[0] if errore.args else 0
        raise errore_di_sistema(INDICE)

def codificare_SMS(testo):
    return testo.encode("utf-8")

def 글해독(dati):
    return dati.decode("utf-8")

def 파일읽기(Nome):
    return 운영호출(sistema_operativo.read, Nome)

def scrivere_File(Nome, dati):
    return 운영호출(sistema_operativo.write, Nome, dati)

def rimuovere_File(Nome):
    return 운영호출(sistema_operativo.remove, Nome)

def aperto_datagramma(numero_di_porta):
    return 운영호출(sistema_operativo.udp_open, numero_di_porta)

def inviare_datagramma(endpoint, numero_di_porta, dati):
    return 운영호출(sistema_operativo.udp_send, endpoint, numero_di_porta, dati)

def inviare_esterno_datagramma(endpoint, e_mail, numero_di_porta, dati):
    return 운영호출(sistema_operativo.udp_sendto, endpoint, e_mail, numero_di_porta, dati)

def ricevere_datagramma(endpoint):
    return 운영호출(sistema_operativo.udp_recv, endpoint)

def Chiudi_rete(endpoint):
    return 운영호출(sistema_operativo.udp_close, endpoint)

def Disegno_rettangolo(*argomenti):
    return 운영호출(sistema_operativo.rect, *argomenti)

def schermata_ridimensionare():
    return 운영호출(sistema_operativo.screen_size)

def 그림기다리기():
    return 운영호출(sistema_operativo.wait_key)

밀리초 = sistema_operativo.ticks_ms
