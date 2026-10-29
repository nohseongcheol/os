"""savs 커널의 Fails·통신·화면 호출과 Latviešu izņēmums. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as operētājsistēma
import sys as CLR

def Izvade(*VALUE, atdalītājs=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = atdalītājs
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

vesels_skaitlis = int
명령인수 = CLR.argv
다시시도오류 = 11

class sistēma_kļūda(OSError):
    def __init__(자신, INDEX, 설명="operētājsistēma 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *Parametri):
    try:
        return FUNCTION_VALUE(*Parametri)
    except OSError as Kļūda:
        INDEX = Kļūda.args[0] if Kļūda.args else 0
        raise sistēma_kļūda(INDEX)

def kodēt_SMS(Teksts):
    return Teksts.encode("utf-8")

def 글해독(dati):
    return dati.decode("utf-8")

def 파일읽기(Nosaukums):
    return 운영호출(operētājsistēma.read, Nosaukums)

def rakstīšana_Fails(Nosaukums, dati):
    return 운영호출(operētājsistēma.write, Nosaukums, dati)

def noņemt_Fails(Nosaukums):
    return 운영호출(operētājsistēma.remove, Nosaukums)

def atvērt_datogramma(porta_numurs):
    return 운영호출(operētājsistēma.udp_open, porta_numurs)

def sūtīt_datogramma(dalībnieks, porta_numurs, dati):
    return 운영호출(operētājsistēma.udp_send, dalībnieks, porta_numurs, dati)

def sūtīt_ārējs_datogramma(dalībnieks, adrese, porta_numurs, dati):
    return 운영호출(operētājsistēma.udp_sendto, dalībnieks, adrese, porta_numurs, dati)

def saņemt_datogramma(dalībnieks):
    return 운영호출(operētājsistēma.udp_recv, dalībnieks)

def Aizvērt_tīkls(dalībnieks):
    return 운영호출(operētājsistēma.udp_close, dalībnieks)

def zīmēt_taisnstūris(*Parametri):
    return 운영호출(operētājsistēma.rect, *Parametri)

def 화면크기():
    return 운영호출(operētājsistēma.screen_size)

def 그림기다리기():
    return 운영호출(operētājsistēma.wait_key)

밀리초 = operētājsistēma.ticks_ms
