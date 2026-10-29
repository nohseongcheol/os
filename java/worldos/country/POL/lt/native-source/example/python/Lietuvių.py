"""savas 커널의 Failas·통신·화면 호출과 Lietuvių išimtis. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operacinė_sistema
import sys as CLR

def Išvestis(*VALUE, skyriklis=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = skyriklis
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

sveikasis_skaičius = int
명령인수 = CLR.argv
다시시도오류 = 11

class 운영체제오류(OSError):
    def __init__(자신, INDEX, aprašas="operacinė_sistema 작업에 실패했습니다."):
        super().__init__(INDEX, aprašas)
        자신.INDEX = INDEX
        자신.aprašas = aprašas

def 운영호출(FUNCTION_VALUE, *Argumentai):
    try:
        return FUNCTION_VALUE(*Argumentai)
    except OSError as KLAIDA:
        INDEX = KLAIDA.args[0] if KLAIDA.args else 0
        raise 운영체제오류(INDEX)

def koduoti_SMS(Tekstas):
    return Tekstas.encode("utf-8")

def 글해독(duomenys):
    return duomenys.decode("utf-8")

def 파일읽기(Pavadinimas_2):
    return 운영호출(operacinė_sistema.read, Pavadinimas_2)

def rašymas_Failas(Pavadinimas_2, duomenys):
    return 운영호출(operacinė_sistema.write, Pavadinimas_2, duomenys)

def pašalinti_Failas(Pavadinimas_2):
    return 운영호출(operacinė_sistema.remove, Pavadinimas_2)

def kurti_paketų_kelio_schema(prievado_numeris):
    return 운영호출(operacinė_sistema.udp_open, prievado_numeris)

def siųsti_paketų_kelio_schema(dalyvis, prievado_numeris, duomenys):
    return 운영호출(operacinė_sistema.udp_send, dalyvis, prievado_numeris, duomenys)

def siųsti_išorinis_paketų_kelio_schema(dalyvis, ADDRESS, prievado_numeris, duomenys):
    return 운영호출(operacinė_sistema.udp_sendto, dalyvis, ADDRESS, prievado_numeris, duomenys)

def gauti_paketų_kelio_schema(dalyvis):
    return 운영호출(operacinė_sistema.udp_recv, dalyvis)

def Uždaryti_tinklas(dalyvis):
    return 운영호출(operacinė_sistema.udp_close, dalyvis)

def piešti_stačiakampis(*Argumentai):
    return 운영호출(operacinė_sistema.rect, *Argumentai)

def 화면크기():
    return 운영호출(operacinė_sistema.screen_size)

def 그림기다리기():
    return 운영호출(operacinė_sistema.wait_key)

밀리초 = operacinė_sistema.ticks_ms
