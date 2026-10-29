"""propio 커널의 Archivo·Comunicación·Pantalla 호출과 español excepción. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as SistemaOperativo
import sys as EntornoEjecución

def Salida(*valor, separador=" ", terminación="\n", **argumentosSistemaAntiguo):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in argumentosSistemaAntiguo: argumentosSistemaAntiguo["sep"] = separador
    if "end" not in argumentosSistemaAntiguo: argumentosSistemaAntiguo["end"] = terminación
    print(*valor, **argumentosSistemaAntiguo)

EnteroValor = int
argumentosComando = EntornoEjecución.argv
ErrorOtraVezIntentar = 11

class ErrorSistema(OSError):
    def __init__(valorPropio, número, descripción="SistemaOperativo 작업에 실패했습니다."):
        super().__init__(número, descripción)
        valorPropio.número = número
        valorPropio.descripción = descripción

def invocarSistema(Función, *argumentos):
    try:
        return Función(*argumentos)
    except OSError as error:
        número = error.args[0] if error.args else 0
        raise ErrorSistema(número)

def codificarTexto(texto):
    return texto.encode("utf-8")

def decodificarTexto(Datos):
    return Datos.decode("utf-8")

def leerArchivo(nombre):
    return invocarSistema(SistemaOperativo.read, nombre)

def escribirArchivo(nombre, Datos):
    return invocarSistema(SistemaOperativo.write, nombre, Datos)

def eliminarArchivo(nombre):
    return invocarSistema(SistemaOperativo.remove, nombre)

def abrirDatagrama(númeroPuerto):
    return invocarSistema(SistemaOperativo.udp_open, númeroPuerto)

def enviarDatagrama(extremo, númeroPuerto, Datos):
    return invocarSistema(SistemaOperativo.udp_send, extremo, númeroPuerto, Datos)

def enviarDatagramaExterno(extremo, dirección, númeroPuerto, Datos):
    return invocarSistema(SistemaOperativo.udp_sendto, extremo, dirección, númeroPuerto, Datos)

def recibirDatagrama(extremo):
    return invocarSistema(SistemaOperativo.udp_recv, extremo)

def cerrarRed(extremo):
    return invocarSistema(SistemaOperativo.udp_close, extremo)

def dibujarRectángulo(*argumentos):
    return invocarSistema(SistemaOperativo.rect, *argumentos)

def tamañoPantalla():
    return invocarSistema(SistemaOperativo.screen_size)

def esperarDibujoPara():
    return invocarSistema(SistemaOperativo.wait_key)

milisegundos = SistemaOperativo.ticks_ms
