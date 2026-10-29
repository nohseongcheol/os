"""nativo 커널의 ficheiro·comunicação·tela 호출과 Português exceção. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as SO
import sys as CLR

def saídaTexto(*VALOR, separador=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = separador
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALOR, **기존인수)

inteiro = int
명령인수 = CLR.argv
다시시도오류 = 11

class erro_do_sistema(OSError):
    def __init__(자신, ÍNDICE, 설명="SO 작업에 실패했습니다."):
        super().__init__(ÍNDICE, 설명)
        자신.ÍNDICE = ÍNDICE
        자신.설명 = 설명

def 운영호출(FUNÇÃO_VALOR, *argumentos):
    try:
        return FUNÇÃO_VALOR(*argumentos)
    except OSError as erro:
        ÍNDICE = erro.args[0] if erro.args else 0
        raise erro_do_sistema(ÍNDICE)

def codificar_SMS(texto):
    return texto.encode("utf-8")

def 글해독(dados):
    return dados.decode("utf-8")

def leitura_Arquivo(Nome):
    return 운영호출(SO.read, Nome)

def gravar_Arquivo(Nome, dados):
    return 운영호출(SO.write, Nome, dados)

def remover_Arquivo(Nome):
    return 운영호출(SO.remove, Nome)

def abrir_datagrama(número_da_porta):
    return 운영호출(SO.udp_open, número_da_porta)

def enviar_datagrama(empresa, número_da_porta, dados):
    return 운영호출(SO.udp_send, empresa, número_da_porta, dados)

def enviar_externo_datagrama(empresa, Endereço, número_da_porta, dados):
    return 운영호출(SO.udp_sendto, empresa, Endereço, número_da_porta, dados)

def receber_datagrama(empresa):
    return 운영호출(SO.udp_recv, empresa)

def Close_rede(empresa):
    return 운영호출(SO.udp_close, empresa)

def emitir_retângulo(*argumentos):
    return 운영호출(SO.rect, *argumentos)

def tela_dimensionar():
    return 운영호출(SO.screen_size)

def 그림기다리기():
    return 운영호출(SO.wait_key)

밀리초 = SO.ticks_ms
