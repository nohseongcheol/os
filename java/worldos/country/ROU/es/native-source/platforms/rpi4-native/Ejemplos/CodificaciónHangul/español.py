"""propio valorNúcleo MicroPython에서 사용하는 한글 Función nombre."""
import jkoros as SistemaOperativo
Salida = print
leerArchivo = SistemaOperativo.read
escribirArchivo = SistemaOperativo.write
eliminarArchivo = SistemaOperativo.remove
leerEntrada = SistemaOperativo.stdin
dibujarRectángulo = SistemaOperativo.rect
esperarDibujoPara = SistemaOperativo.wait_key
milisegundos = SistemaOperativo.ticks_ms
abrirDatagrama = SistemaOperativo.udp_open
enviarDatagrama = SistemaOperativo.udp_send
enviarDatagramaExterno = SistemaOperativo.udp_sendto
recibirDatagrama = SistemaOperativo.udp_recv
cerrarRed = SistemaOperativo.udp_close

def decodificarTexto(Datos):
    return Datos.decode("utf-8")
