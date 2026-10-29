#!/usr/bin/env python3
"""QEMU의 real_dades CPU permís_VALOR, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Executa_ordre import Project_rel, Ordre
from xarxa_pont import xarxa_pont
from 되돌림시험서버 import 되돌림시험서버


def Executa_2():
    Sortida = Project_rel / 'build/verification/execution-network-review'
    Sortida.mkdir(parents=True, exist_ok=True)
    informe_VALOR = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_rel / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    font_Fitxers = {
        'permís_xec': '''public class permís_xec {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'xarxa_xec': '''import java.net.*;
public class xarxa_xec {
 public static void main(String[] 인수) throws Exception {
  Socket Connecta = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Connecta.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  Connecta.getOutputStream().write(SMS);
  for (int càrrec_INDEX = 0; càrrec_INDEX < SMS.length; càrrec_INDEX++)
   if (Connecta.getInputStream().read() != (SMS[càrrec_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Connecta.close();
  DatagramSocket extrem = new DatagramSocket(); extrem.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  extrem.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] resposta = new byte[64]; DatagramPacket 전문 = new DatagramPacket(resposta, resposta.length);
  extrem.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int càrrec_INDEX = 0; càrrec_INDEX < SMS.length; càrrec_INDEX++)
   if (resposta[càrrec_INDEX] != SMS[càrrec_INDEX]) throw new RuntimeException("UDP mismatch");
  extrem.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'rebre_xec': '''import java.net.*;
public class rebre_xec {
 public static void main(String[] 인수) throws Exception {
  ServerSocket servidor_VALOR = new ServerSocket(9300); servidor_VALOR.setSoTimeout(5000);
  DatagramSocket extrem = new DatagramSocket(9301); extrem.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Connecta = servidor_VALOR.accept(); Connecta.setSoTimeout(5000);
  Connecta.getOutputStream().write(Connecta.getInputStream().read() + 1);
  Connecta.close(); servidor_VALOR.close();
  byte[] dades = new byte[64]; DatagramPacket 전문 = new DatagramPacket(dades, dades.length);
  extrem.receive(전문); extrem.send(전문); extrem.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nom, FONT in font_Fitxers.items():
        (Sortida / (Nom + '.java')).write_text(FONT, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Sortida)] +
                          [str(Sortida / (Nom + '.java')) for Nom in font_Fitxers])
    LOG_fila = bytearray()
    def 빈접속번호(TIPUS_Categoria=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TIPUS_Categoria) as Cerca_VALOR:
            Cerca_VALOR.bind(('127.0.0.4', 0))
            return Cerca_VALOR.getsockname()[1]
    arxiu_número_de_port, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Procés_VALOR = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, xarxa_pont(
                arxiu_número_de_port, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                capturar=True, allotjar_ADREÇA='127.0.0.4') as pont_VALOR:
            control_camí = Path(임시) / 'qmp.sock'
            Procés_VALOR = subprocess.Popen(Ordre() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(control_camí)] + pont_VALOR.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            TRIA_element = selectors.DefaultSelector()
            TRIA_element.register(Procés_VALOR.stdout, selectors.EVENT_READ)
            def rebre(mostrar_VALOR=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while mostrar_VALOR not in LOG_fila[처음:]:
                    if time.monotonic() > 끝 or Procés_VALOR.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrar_VALOR) + '\n' + LOG_fila[처음:].decode('utf-8', 'replace'))
                    for Clau_VALOR, _ in TRIA_element.select(.05):
                        조각 = Clau_VALOR.fileobj.read(65536)
                        if 조각:
                            LOG_fila.extend(조각)
                return LOG_fila[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def enviar(dades):
                Procés_VALOR.stdin.write(dades)
                Procés_VALOR.stdin.flush()
            def shell(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_fila)
                enviar((SMS + '\n').encode())
                return rebre(처음=처음)
            rebre()
            with socket.socket(socket.AF_UNIX) as control_VALOR:
                control_VALOR.settimeout(10)
                control_VALOR.connect(str(control_camí))
                flux_VALOR = control_VALOR.makefile('rwb')
                json.loads(flux_VALOR.readline())
                def sol_licitud(instrucció_VALOR_4c26ea1b, 인수=None):
                    dades = {'execute': instrucció_VALOR_4c26ea1b}
                    if 인수 is not None:
                        dades['arguments'] = 인수
                    flux_VALOR.write((json.dumps(dades) + '\n').encode())
                    flux_VALOR.flush()
                    while True:
                        resposta = json.loads(flux_VALOR.readline())
                        if 'error' in resposta:
                            raise AssertionError(resposta)
                        if 'return' in resposta:
                            return resposta['return']
                sol_licitud('qmp_capabilities')
                def tancar_permís():
                    sol_licitud('stop')
                    try:
                        return sol_licitud('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        sol_licitud('cont')
                informe_VALOR['shell_cpu'] = tancar_permís()
                assert 'EL1h' in informe_VALOR['shell_cpu'], informe_VALOR['shell_cpu']
                informe_VALOR['initial_ps'] = shell('ps')
                assert 'kernel/shell' in informe_VALOR['initial_ps']
                informe_VALOR['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in informe_VALOR['ipconfig']
                informe_VALOR['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in informe_VALOR['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as transferir_VALOR:
                    transferir_VALOR.encoding = 'utf-8'
                    transferir_VALOR.connect('127.0.0.4', arxiu_número_de_port, timeout=20)
                    transferir_VALOR.login()
                    for Nom in font_Fitxers:
                        transferir_VALOR.storbinary('STOR ' + Nom + '.class', io.BytesIO((Sortida / (Nom + '.class')).read_bytes()))
                처음 = len(LOG_fila)
                enviar('java permís_xec\n'.encode())
                rebre(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    informe_VALOR['java_cpu'] = tancar_permís()
                    if 'EL0t' in informe_VALOR['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in informe_VALOR['java_cpu'], informe_VALOR['java_cpu']
                rebre(처음=처음)
                informe_VALOR['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', informe_VALOR['after_exit_ps'])
                informe_VALOR['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as homòleg_VALOR:
                    SMS = shell('java xarxa_xec {} {}'.format(homòleg_VALOR.TCP_port, homòleg_VALOR.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert homòleg_VALOR.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, homòleg_VALOR.수신됨
                    assert not homòleg_VALOR.오류들, homòleg_VALOR.오류들
                    informe_VALOR['outbound_peers'] = {종류: dades.decode() for 종류, dades in homòleg_VALOR.수신됨.items()}
                처음 = len(LOG_fila)
                enviar('java rebre_xec\n'.encode())
                rebre(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as homòleg_VALOR:
                    homòleg_VALOR.sendall(b'A')
                    assert homòleg_VALOR.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as homòleg_VALOR:
                    homòleg_VALOR.settimeout(5)
                    homòleg_VALOR.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert homòleg_VALOR.recvfrom(64)[0] == b'UDP-IN'
                SMS = rebre(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                informe_VALOR['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_fila)
                enviar('java ExempleFinestra\n'.encode())
                rebre('GUI 예제 Prepara: ExempleFinestra\r\n'.encode(), 처음)
                처음 = len(LOG_fila)
                enviar(bytes([30, 2, 1, 0, 0, 0, 0]))
                rebre(처음=처음)
                informe_VALOR['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ExempleFinestra', informe_VALOR['suspended_java_ps']), informe_VALOR['suspended_java_ps']
                informe_VALOR['top'] = shell('top -n 1')
                assert 'java ExempleFinestra' in informe_VALOR['top'] and 'kernel/shell' in informe_VALOR['top']
                informe_VALOR['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                informe_VALOR['network_trace'] = pont_VALOR.traça_LOG
                assert not pont_VALOR.s_ha_produït_un_error, pont_VALOR.s_ha_produït_un_error
                enviar(b'poweroff\n')
                assert Procés_VALOR.wait(timeout=15) == 0
                informe_VALOR['passed'] = True
            TRIA_element.close()
    except Exception as s_ha_produït_un_error:
        informe_VALOR['error'] = str(s_ha_produït_un_error)
        raise
    finally:
        if Procés_VALOR is not None and Procés_VALOR.poll() is None:
            Procés_VALOR.terminate()
            try:
                Procés_VALOR.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Procés_VALOR.kill()
                Procés_VALOR.wait()
        (Sortida / 'serial.log').write_bytes(LOG_fila)
        (Sortida / 'report.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Clau_VALOR: informe_VALOR[Clau_VALOR] for Clau_VALOR in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Executa_2()
