from español import Salida, abrirDatagrama, enviarDatagramaExterno, recibirDatagrama, cerrarRed, milisegundos
from español import ErrorSistema, ErrorOtraVezIntentar, codificarTexto, argumentosComando, EnteroValor
extremo = abrirDatagrama(0)
try:
    datagrama = codificarTexto("PYTHON UDP Español")
    enviarDatagramaExterno(extremo, "10.0.2.2", EnteroValor(argumentosComando[1]), datagrama)
    ponerEnMarcha = milisegundos()
    while True:
        try:
            respuesta, valorPuerto = recibirDatagrama(extremo)
            break
        except ErrorSistema as error:
            if error.número != ErrorOtraVezIntentar or milisegundos() - ponerEnMarcha >= 700:
                raise
    assert respuesta == datagrama
    Salida("PYTHON 네트워크 verificar: UDP Español")
finally:
    cerrarRed(extremo)
