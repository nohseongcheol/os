"""자체 커널의 Ficheiro·통신·화면 호출과 Galego excepción. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistema_operativo
import sys as 실행환경

def Saída(*VALOR, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALOR, **기존인수)

número_enteiro = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class sistema_erro(OSError):
    def __init__(자신, ÍNDICE, 설명="sistema_operativo 작업에 실패했습니다."):
        super().__init__(ÍNDICE, 설명)
        자신.ÍNDICE = ÍNDICE
        자신.설명 = 설명

def 운영호출(FUNCIÓN_VALOR, *Argumentos):
    try:
        return FUNCIÓN_VALOR(*Argumentos)
    except OSError as ERRO:
        ÍNDICE = ERRO.args[0] if ERRO.args else 0
        raise sistema_erro(ÍNDICE)

def 글부호화(Texto):
    return Texto.encode("utf-8")

def 글해독(datos):
    return datos.decode("utf-8")

def 파일읽기(Nome):
    return 운영호출(sistema_operativo.read, Nome)

def escribir_Ficheiro(Nome, datos):
    return 운영호출(sistema_operativo.write, Nome, datos)

def eliminar_Ficheiro(Nome):
    return 운영호출(sistema_operativo.remove, Nome)

def 전문통신열기(número_do_porto):
    return 운영호출(sistema_operativo.udp_open, número_do_porto)

def 전문보내기(extremo, número_do_porto, datos):
    return 운영호출(sistema_operativo.udp_send, extremo, número_do_porto, datos)

def 바깥전문보내기(extremo, ENDEREZO, número_do_porto, datos):
    return 운영호출(sistema_operativo.udp_sendto, extremo, ENDEREZO, número_do_porto, datos)

def 전문받기(extremo):
    return 운영호출(sistema_operativo.udp_recv, extremo)

def peche_Rede(extremo):
    return 운영호출(sistema_operativo.udp_close, extremo)

def 네모그리기(*Argumentos):
    return 운영호출(sistema_operativo.rect, *Argumentos)

def 화면크기():
    return 운영호출(sistema_operativo.screen_size)

def 그림기다리기():
    return 운영호출(sistema_operativo.wait_key)

밀리초 = sistema_operativo.ticks_ms
