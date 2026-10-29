"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class DispositivoPruebaRepetirEntrada:
    def __enter__(valorPropio):
        valorPropio.controlConexión = socket.socket(); valorPropio.controlConexión.bind(('127.0.0.1', 0)); valorPropio.controlConexión.listen(1)
        valorPropio.controlDatagrama = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); valorPropio.controlDatagrama.bind(('127.0.0.1', 0))
        valorPropio.controlConexión.settimeout(30); valorPropio.controlDatagrama.settimeout(30)
        valorPropio.puertoTCP = valorPropio.controlConexión.getsockname()[1]; valorPropio.puertoUDP = valorPropio.controlDatagrama.getsockname()[1]
        valorPropio.errores = []; valorPropio.tieneRecibido = {}
        def controlConexión():
            try:
                conexión, _ = valorPropio.controlConexión.accept()
                with conexión:
                    conexión.settimeout(5); Datos = bytearray()
                    while b'\n' not in Datos:
                        valorFragmento = conexión.recv(512)
                        if not valorFragmento: raise RuntimeError('TCP EOF before request')
                        Datos.extend(valorFragmento)
                    valorPropio.tieneRecibido['tcp'] = bytes(Datos); conexión.sendall(Datos)
            except Exception as entradaElementoAuxiliar: valorPropio.errores.append(str(entradaElementoAuxiliar))
        def controlDatagrama():
            try:
                Datos, valorParRed = valorPropio.controlDatagrama.recvfrom(512); valorPropio.tieneRecibido['udp'] = Datos; valorPropio.controlDatagrama.sendto(Datos, valorParRed)
            except Exception as entradaElementoAuxiliar: valorPropio.errores.append(str(entradaElementoAuxiliar))
        valorPropio.hilosEjecución = [threading.Thread(target=entradaElementoArchivo, daemon=True) for entradaElementoArchivo in (controlConexión, controlDatagrama)]
        for entradaElementoTerminal in valorPropio.hilosEjecución: entradaElementoTerminal.start()
        return valorPropio

    def __exit__(valorPropio, *arregloArgumento):
        valorPropio.controlConexión.close(); valorPropio.controlDatagrama.close()
        for entradaElementoTerminal in valorPropio.hilosEjecución: entradaElementoTerminal.join(timeout=1)
