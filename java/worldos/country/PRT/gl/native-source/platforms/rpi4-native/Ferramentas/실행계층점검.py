#!/usr/bin/env python3
"""QEMU의 real_datos CPU permiso_VALOR, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from executar_comando import Project_raíz, Orde
from Rede_ponte import Rede_ponte
from 되돌림시험서버 import 되돌림시험서버


def Executar_2():
    Saída = Project_raíz / 'build/verification/execution-network-review'
    Saída.mkdir(parents=True, exist_ok=True)
    informe_VALOR = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_raíz / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    fonte_Ficheiros = {
        'permiso_cheque': '''public class permiso_cheque {
 public static void main(String[] Argumentos) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Rede_cheque': '''import java.net.*;
public class Rede_cheque {
 public static void main(String[] Argumentos) throws Exception {
  Socket Conectar = new Socket("10.0.2.2", Integer.parseInt(Argumentos[0]));
  Conectar.setSoTimeout(3000);
  byte[] Texto = "TCP 한글\\n".getBytes("UTF-8");
  Conectar.getOutputStream().write(Texto);
  for (int cargo_ÍNDICE = 0; cargo_ÍNDICE < Texto.length; cargo_ÍNDICE++)
   if (Conectar.getInputStream().read() != (Texto[cargo_ÍNDICE] & 255)) throw new RuntimeException("TCP mismatch");
  Conectar.close();
  DatagramSocket extremo = new DatagramSocket(); extremo.setSoTimeout(3000);
  Texto = "UDP 한글".getBytes("UTF-8");
  extremo.send(new DatagramPacket(Texto, Texto.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumentos[1])));
  byte[] resposta = new byte[64]; DatagramPacket 전문 = new DatagramPacket(resposta, resposta.length);
  extremo.receive(전문);
  if (전문.getLength() != Texto.length) throw new RuntimeException("UDP length");
  for (int cargo_ÍNDICE = 0; cargo_ÍNDICE < Texto.length; cargo_ÍNDICE++)
   if (resposta[cargo_ÍNDICE] != Texto[cargo_ÍNDICE]) throw new RuntimeException("UDP mismatch");
  extremo.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Argumentos) throws Exception {
  ServerSocket servidor_VALOR = new ServerSocket(9300); servidor_VALOR.setSoTimeout(5000);
  DatagramSocket extremo = new DatagramSocket(9301); extremo.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Conectar = servidor_VALOR.accept(); Conectar.setSoTimeout(5000);
  Conectar.getOutputStream().write(Conectar.getInputStream().read() + 1);
  Conectar.close(); servidor_VALOR.close();
  byte[] datos = new byte[64]; DatagramPacket 전문 = new DatagramPacket(datos, datos.length);
  extremo.receive(전문); extremo.send(전문); extremo.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nome, FONTE in fonte_Ficheiros.items():
        (Saída / (Nome + '.java')).write_text(FONTE, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Saída)] +
                          [str(Saída / (Nome + '.java')) for Nome in fonte_Ficheiros])
    LOG_fila = bytearray()
    def baleiro_número_do_porto(TIPO_Categoría=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TIPO_Categoría) as ACHAR_VALOR:
            ACHAR_VALOR.bind(('127.0.0.4', 0))
            return ACHAR_VALOR.getsockname()[1]
    Ficheiro_número_do_porto, TCP_porto, UDP_porto = baleiro_número_do_porto(), baleiro_número_do_porto(), baleiro_número_do_porto(socket.SOCK_DGRAM)
    Proceso_VALOR = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Rede_ponte(
                Ficheiro_número_do_porto, ['tcp:{}:9300'.format(TCP_porto), 'udp:{}:9301'.format(UDP_porto)],
                capturar=True, hospedar_ENDEREZO='127.0.0.4') as ponte_VALOR:
            control_camiño = Path(임시) / 'qmp.sock'
            Proceso_VALOR = subprocess.Popen(Orde() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(control_camiño)] + ponte_VALOR.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ESCOLLER_elemento = selectors.DefaultSelector()
            ESCOLLER_elemento.register(Proceso_VALOR.stdout, selectors.EVENT_READ)
            def 받기(mostrar_VALOR=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while mostrar_VALOR not in LOG_fila[처음:]:
                    if time.monotonic() > 끝 or Proceso_VALOR.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrar_VALOR) + '\n' + LOG_fila[처음:].decode('utf-8', 'replace'))
                    for Chave_VALOR, _ in ESCOLLER_elemento.select(.05):
                        조각 = Chave_VALOR.fileobj.read(65536)
                        if 조각:
                            LOG_fila.extend(조각)
                return LOG_fila[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def enviar(datos):
                Proceso_VALOR.stdin.write(datos)
                Proceso_VALOR.stdin.flush()
            def shell(Texto):
                print(Texto, flush=True)
                처음 = len(LOG_fila)
                enviar((Texto + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as control_VALOR:
                control_VALOR.settimeout(10)
                control_VALOR.connect(str(control_camiño))
                fluxo_VALOR = control_VALOR.makefile('rwb')
                json.loads(fluxo_VALOR.readline())
                def solicitude(instrución_VALOR_4c26ea1b, Argumentos=None):
                    datos = {'execute': instrución_VALOR_4c26ea1b}
                    if Argumentos is not None:
                        datos['arguments'] = Argumentos
                    fluxo_VALOR.write((json.dumps(datos) + '\n').encode())
                    fluxo_VALOR.flush()
                    while True:
                        resposta = json.loads(fluxo_VALOR.readline())
                        if 'error' in resposta:
                            raise AssertionError(resposta)
                        if 'return' in resposta:
                            return resposta['return']
                solicitude('qmp_capabilities')
                def 권한읽기():
                    solicitude('stop')
                    try:
                        return solicitude('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        solicitude('cont')
                informe_VALOR['shell_cpu'] = 권한읽기()
                assert 'EL1h' in informe_VALOR['shell_cpu'], informe_VALOR['shell_cpu']
                informe_VALOR['initial_ps'] = shell('ps')
                assert 'kernel/shell' in informe_VALOR['initial_ps']
                informe_VALOR['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in informe_VALOR['ipconfig']
                informe_VALOR['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in informe_VALOR['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as Transferir_VALOR:
                    Transferir_VALOR.encoding = 'utf-8'
                    Transferir_VALOR.connect('127.0.0.4', Ficheiro_número_do_porto, timeout=20)
                    Transferir_VALOR.login()
                    for Nome in fonte_Ficheiros:
                        Transferir_VALOR.storbinary('STOR ' + Nome + '.class', io.BytesIO((Saída / (Nome + '.class')).read_bytes()))
                처음 = len(LOG_fila)
                enviar('java permiso_cheque\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    informe_VALOR['java_cpu'] = 권한읽기()
                    if 'EL0t' in informe_VALOR['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in informe_VALOR['java_cpu'], informe_VALOR['java_cpu']
                받기(처음=처음)
                informe_VALOR['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', informe_VALOR['after_exit_ps'])
                informe_VALOR['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as punto_VALOR:
                    Texto = shell('java Rede_cheque {} {}'.format(punto_VALOR.TCP_porto, punto_VALOR.UDP_porto))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Texto and 'exit 0' in Texto, Texto
                    assert punto_VALOR.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, punto_VALOR.수신됨
                    assert not punto_VALOR.오류들, punto_VALOR.오류들
                    informe_VALOR['outbound_peers'] = {종류: datos.decode() for 종류, datos in punto_VALOR.수신됨.items()}
                처음 = len(LOG_fila)
                enviar('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_porto), timeout=5) as punto_VALOR:
                    punto_VALOR.sendall(b'A')
                    assert punto_VALOR.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as punto_VALOR:
                    punto_VALOR.settimeout(5)
                    punto_VALOR.sendto(b'UDP-IN', ('127.0.0.4', UDP_porto))
                    assert punto_VALOR.recvfrom(64)[0] == b'UDP-IN'
                Texto = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Texto and 'exit 0' in Texto, Texto
                informe_VALOR['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_fila)
                enviar('java 창예제\n'.encode())
                받기('GUI 예제 준비: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_fila)
                enviar(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                informe_VALOR['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', informe_VALOR['suspended_java_ps']), informe_VALOR['suspended_java_ps']
                informe_VALOR['top'] = shell('top -n 1')
                assert 'java 창예제' in informe_VALOR['top'] and 'kernel/shell' in informe_VALOR['top']
                informe_VALOR['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                informe_VALOR['network_trace'] = ponte_VALOR.traza_LOG
                assert not ponte_VALOR.ERRO, ponte_VALOR.ERRO
                enviar(b'poweroff\n')
                assert Proceso_VALOR.wait(timeout=15) == 0
                informe_VALOR['passed'] = True
            ESCOLLER_elemento.close()
    except Exception as ERRO:
        informe_VALOR['error'] = str(ERRO)
        raise
    finally:
        if Proceso_VALOR is not None and Proceso_VALOR.poll() is None:
            Proceso_VALOR.terminate()
            try:
                Proceso_VALOR.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proceso_VALOR.kill()
                Proceso_VALOR.wait()
        (Saída / 'serial.log').write_bytes(LOG_fila)
        (Saída / 'report.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Chave_VALOR: informe_VALOR[Chave_VALOR] for Chave_VALOR in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Executar_2()
