"""propriu 커널의 Fișier·통신·화면 호출과 Română excepție. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistem_de_operare
import sys as CLR

def Rezultat(*VALUE, separator=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = separator
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

întreg = int
명령인수 = CLR.argv
다시시도오류 = 11

class sistem_eroare(OSError):
    def __init__(자신, INDEX, 설명="sistem_de_operare 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(funcție_VALUE, *Argumente):
    try:
        return funcție_VALUE(*Argumente)
    except OSError as eroare:
        INDEX = eroare.args[0] if eroare.args else 0
        raise sistem_eroare(INDEX)

def codifica_SMS(SMS):
    return SMS.encode("utf-8")

def 글해독(date):
    return date.decode("utf-8")

def 파일읽기(Nume):
    return 운영호출(sistem_de_operare.read, Nume)

def scriere_Fișier(Nume, date):
    return 운영호출(sistem_de_operare.write, Nume, date)

def elimina_Fișier(Nume):
    return 운영호출(sistem_de_operare.remove, Nume)

def crea_diagramă_informații(număr_port):
    return 운영호출(sistem_de_operare.udp_open, număr_port)

def trimite_diagramă_informații(participant, număr_port, date):
    return 운영호출(sistem_de_operare.udp_send, participant, număr_port, date)

def trimite_extern_diagramă_informații(participant, adresa, număr_port, date):
    return 운영호출(sistem_de_operare.udp_sendto, participant, adresa, număr_port, date)

def primi_diagramă_informații(participant):
    return 운영호출(sistem_de_operare.udp_recv, participant)

def închide_rețea(participant):
    return 운영호출(sistem_de_operare.udp_close, participant)

def Desen_dreptunghi(*Argumente):
    return 운영호출(sistem_de_operare.rect, *Argumente)

def 화면크기():
    return 운영호출(sistem_de_operare.screen_size)

def 그림기다리기():
    return 운영호출(sistem_de_operare.wait_key)

밀리초 = sistem_de_operare.ticks_ms
