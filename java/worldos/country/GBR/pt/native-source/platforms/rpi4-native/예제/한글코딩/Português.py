"""nativo kernel_VALOR MicroPython에서 사용하는 한글 FUNÇÃO_VALOR Nome."""
import jkoros as SO
saídaTexto = print
leitura_Arquivo = SO.read
gravar_Arquivo = SO.write
remover_Arquivo = SO.remove
leitura_entrada = SO.stdin
emitir_retângulo = SO.rect
그림기다리기 = SO.wait_key
밀리초 = SO.ticks_ms
abrir_datagrama = SO.udp_open
enviar_datagrama = SO.udp_send
enviar_externo_datagrama = SO.udp_sendto
receber_datagrama = SO.udp_recv
Close_rede = SO.udp_close

def 글해독(dados):
    return dados.decode("utf-8")
