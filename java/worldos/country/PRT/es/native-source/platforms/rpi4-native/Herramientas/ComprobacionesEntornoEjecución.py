#!/usr/bin/env python3
"""QEMU의 datosEfectivo CPU valorPermiso, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
import ftplib
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time

from ejecutarComando import raízProyecto, comando
from puenteRed import puenteRed
from DispositivoPruebaRepetirEntrada import DispositivoPruebaRepetirEntrada


def ponerEnMarcha():
    Salida = raízProyecto / 'build/verification/execution-network-review'
    Salida.mkdir(parents=True, exist_ok=True)
    valorInforme = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((raízProyecto / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    archivosFuente = {
        'ComprobarPrivilegio': '''public class ComprobarPrivilegio {
 public static void main(String[] argumentos) {
  System.out.println("EL0_PROBE_READY");
  int númeroValor = 0; while (true) { númeroValor++; }
 }
}''',
        'ComprobarRed': '''import java.net.*;
public class ComprobarRed {
 public static void main(String[] argumentos) throws Exception {
  Socket conectar = new Socket("10.0.2.2", Integer.parseInt(argumentos[0]));
  conectar.setSoTimeout(3000);
  byte[] texto = "TCP 한글\\n".getBytes("UTF-8");
  conectar.getOutputStream().write(texto);
  for (int índicePosición = 0; índicePosición < texto.length; índicePosición++)
   if (conectar.getInputStream().read() != (texto[índicePosición] & 255)) throw new RuntimeException("TCP mismatch");
  conectar.close();
  DatagramSocket extremo = new DatagramSocket(); extremo.setSoTimeout(3000);
  texto = "UDP 한글".getBytes("UTF-8");
  extremo.send(new DatagramPacket(texto, texto.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumentos[1])));
  byte[] respuesta = new byte[64]; DatagramPacket datagrama = new DatagramPacket(respuesta, respuesta.length);
  extremo.receive(datagrama);
  if (datagrama.getLength() != texto.length) throw new RuntimeException("UDP length");
  for (int índicePosición = 0; índicePosición < texto.length; índicePosición++)
   if (respuesta[índicePosición] != texto[índicePosición]) throw new RuntimeException("UDP mismatch");
  extremo.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'ComprobarRecibir': '''import java.net.*;
public class ComprobarRecibir {
 public static void main(String[] argumentos) throws Exception {
  ServerSocket valorServidor = new ServerSocket(9300); valorServidor.setSoTimeout(5000);
  DatagramSocket extremo = new DatagramSocket(9301); extremo.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket conectar = valorServidor.accept(); conectar.setSoTimeout(5000);
  conectar.getOutputStream().write(conectar.getInputStream().read() + 1);
  conectar.close(); valorServidor.close();
  byte[] Datos = new byte[64]; DatagramPacket datagrama = new DatagramPacket(Datos, Datos.length);
  extremo.receive(datagrama); extremo.send(datagrama); extremo.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for nombre, fuente in archivosFuente.items():
        (Salida / (nombre + '.java')).write_text(fuente, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Salida)] +
                          [str(Salida / (nombre + '.java')) for nombre in archivosFuente])
    registroEntradaDiario = bytearray()
    def númeroPuertoVacíoEstado(categoríaTipo=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, categoríaTipo) as buscarCoincidenciaValor:
            buscarCoincidenciaValor.bind(('127.0.0.4', 0))
            return buscarCoincidenciaValor.getsockname()[1]
    númeroPuertoArchivo, puertoTCP, puertoUDP = númeroPuertoVacíoEstado(), númeroPuertoVacíoEstado(), númeroPuertoVacíoEstado(socket.SOCK_DGRAM)
    valorProceso = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as valorTemporal, puenteRed(
                númeroPuertoArchivo, ['tcp:{}:9300'.format(puertoTCP), 'udp:{}:9301'.format(puertoUDP)],
                capturarDatos=True, direcciónAnfitrión='127.0.0.4') as valorPuente:
            rutaControl = Path(valorTemporal) / 'qmp.sock'
            valorProceso = subprocess.Popen(comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(rutaControl)] + valorPuente.argumentoReenviado(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            elementoListaElegir = selectors.DefaultSelector()
            elementoListaElegir.register(valorProceso.stdout, selectors.EVENT_READ)
            def recibir(mostrarValor=b'jkoros-native> ', elementoListaInicialValor=0, valorLímite=60):
                terminación = time.monotonic() + valorLímite
                while mostrarValor not in registroEntradaDiario[elementoListaInicialValor:]:
                    if time.monotonic() > terminación or valorProceso.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrarValor) + '\n' + registroEntradaDiario[elementoListaInicialValor:].decode('utf-8', 'replace'))
                    for valorTecla, _ in elementoListaElegir.select(.05):
                        valorFragmento = valorTecla.fileobj.read(65536)
                        if valorFragmento:
                            registroEntradaDiario.extend(valorFragmento)
                return registroEntradaDiario[elementoListaInicialValor:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def enviar(Datos):
                valorProceso.stdin.write(Datos)
                valorProceso.stdin.flush()
            def intérpreteComandos(texto):
                print(texto, flush=True)
                elementoListaInicialValor = len(registroEntradaDiario)
                enviar((texto + '\n').encode())
                return recibir(elementoListaInicialValor=elementoListaInicialValor)
            recibir()
            with socket.socket(socket.AF_UNIX) as valorControl:
                valorControl.settimeout(10)
                valorControl.connect(str(rutaControl))
                valorFlujo = valorControl.makefile('rwb')
                json.loads(valorFlujo.readline())
                def petición(valorInstrucciónMáquina, argumentos=None):
                    Datos = {'execute': valorInstrucciónMáquina}
                    if argumentos is not None:
                        Datos['arguments'] = argumentos
                    valorFlujo.write((json.dumps(Datos) + '\n').encode())
                    valorFlujo.flush()
                    while True:
                        respuesta = json.loads(valorFlujo.readline())
                        if 'error' in respuesta:
                            raise AssertionError(respuesta)
                        if 'return' in respuesta:
                            return respuesta['return']
                petición('qmp_capabilities')
                def leerPermiso():
                    petición('stop')
                    try:
                        return petición('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        petición('cont')
                valorInforme['shell_cpu'] = leerPermiso()
                assert 'EL1h' in valorInforme['shell_cpu'], valorInforme['shell_cpu']
                valorInforme['initial_ps'] = intérpreteComandos('ps')
                assert 'kernel/shell' in valorInforme['initial_ps']
                valorInforme['ipconfig'] = intérpreteComandos('ipconfig')
                assert 'inet 10.0.2.15' in valorInforme['ipconfig']
                valorInforme['gateway_ping'] = intérpreteComandos('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in valorInforme['gateway_ping']
                assert 'FTP listening' in intérpreteComandos('ftpd start')
                with ftplib.FTP() as valorTransferencia:
                    valorTransferencia.encoding = 'utf-8'
                    valorTransferencia.connect('127.0.0.4', númeroPuertoArchivo, timeout=20)
                    valorTransferencia.login()
                    for nombre in archivosFuente:
                        valorTransferencia.storbinary('STOR ' + nombre + '.class', io.BytesIO((Salida / (nombre + '.class')).read_bytes()))
                elementoListaInicialValor = len(registroEntradaDiario)
                enviar('java ComprobarPrivilegio\n'.encode())
                recibir(b'EL0_PROBE_READY\r\n', elementoListaInicialValor)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    valorInforme['java_cpu'] = leerPermiso()
                    if 'EL0t' in valorInforme['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in valorInforme['java_cpu'], valorInforme['java_cpu']
                recibir(elementoListaInicialValor=elementoListaInicialValor)
                valorInforme['after_exit_ps'] = intérpreteComandos('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', valorInforme['after_exit_ps'])
                valorInforme['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with DispositivoPruebaRepetirEntrada() as valorParRed:
                    texto = intérpreteComandos('java ComprobarRed {} {}'.format(valorParRed.puertoTCP, valorParRed.puertoUDP))
                    assert 'OUTBOUND_TCP_UDP_PASS' in texto and 'exit 0' in texto, texto
                    assert valorParRed.tieneRecibido == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, valorParRed.tieneRecibido
                    assert not valorParRed.errores, valorParRed.errores
                    valorInforme['outbound_peers'] = {valorClaseTipo: Datos.decode() for valorClaseTipo, Datos in valorParRed.tieneRecibido.items()}
                elementoListaInicialValor = len(registroEntradaDiario)
                enviar('java ComprobarRecibir\n'.encode())
                recibir(b'INBOUND_READY\r\n', elementoListaInicialValor)
                with socket.create_connection(('127.0.0.4', puertoTCP), timeout=5) as valorParRed:
                    valorParRed.sendall(b'A')
                    assert valorParRed.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as valorParRed:
                    valorParRed.settimeout(5)
                    valorParRed.sendto(b'UDP-IN', ('127.0.0.4', puertoUDP))
                    assert valorParRed.recvfrom(64)[0] == b'UDP-IN'
                texto = recibir(elementoListaInicialValor=elementoListaInicialValor)
                assert 'INBOUND_TCP_UDP_PASS' in texto and 'exit 0' in texto, texto
                valorInforme['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in intérpreteComandos('terminal')
                intérpreteComandos('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                elementoListaInicialValor = len(registroEntradaDiario)
                enviar('java EjemploVentana\n'.encode())
                recibir('GUI Ejemplos preparar: EjemploVentana\r\n'.encode(), elementoListaInicialValor)
                elementoListaInicialValor = len(registroEntradaDiario)
                enviar(bytes([30, 2, 1, 0, 0, 0, 0]))
                recibir(elementoListaInicialValor=elementoListaInicialValor)
                valorInforme['suspended_java_ps'] = intérpreteComandos('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java EjemploVentana', valorInforme['suspended_java_ps']), valorInforme['suspended_java_ps']
                valorInforme['top'] = intérpreteComandos('top -n 1')
                assert 'java EjemploVentana' in valorInforme['top'] and 'kernel/shell' in valorInforme['top']
                valorInforme['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                valorInforme['network_trace'] = valorPuente.diarioTraza
                assert not valorPuente.error, valorPuente.error
                enviar(b'poweroff\n')
                assert valorProceso.wait(timeout=15) == 0
                valorInforme['passed'] = True
            elementoListaElegir.close()
    except Exception as error:
        valorInforme['error'] = str(error)
        raise
    finally:
        if valorProceso is not None and valorProceso.poll() is None:
            valorProceso.terminate()
            try:
                valorProceso.wait(timeout=10)
            except subprocess.TimeoutExpired:
                valorProceso.kill()
                valorProceso.wait()
        (Salida / 'serial.log').write_bytes(registroEntradaDiario)
        (Salida / 'report.json').write_text(json.dumps(valorInforme, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({valorTecla: valorInforme[valorTecla] for valorTecla in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ponerEnMarcha()
