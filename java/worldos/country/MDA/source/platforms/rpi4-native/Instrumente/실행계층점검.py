#!/usr/bin/env python3
"""QEMU의 real_date CPU permisiune_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from executa_comandă import Project_rădăcină, Comandă
from punte_3de4fe3a import punte_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Pornește():
    Rezultat = Project_rădăcină / 'build/verification/execution-network-review'
    Rezultat.mkdir(parents=True, exist_ok=True)
    raport_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_rădăcină / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    sursă_Fișiere = {
        'permisiune_verifica': '''public class permisiune_verifica {
 public static void main(String[] Argumente) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'rețea_verifica': '''import java.net.*;
public class rețea_verifica {
 public static void main(String[] Argumente) throws Exception {
  Socket Conectează = new Socket("10.0.2.2", Integer.parseInt(Argumente[0]));
  Conectează.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  Conectează.getOutputStream().write(SMS);
  for (int index_de_poziție = 0; index_de_poziție < SMS.length; index_de_poziție++)
   if (Conectează.getInputStream().read() != (SMS[index_de_poziție] & 255)) throw new RuntimeException("TCP mismatch");
  Conectează.close();
  DatagramSocket participant = new DatagramSocket(); participant.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  participant.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumente[1])));
  byte[] replică = new byte[64]; DatagramPacket diagramă_informații = new DatagramPacket(replică, replică.length);
  participant.receive(diagramă_informații);
  if (diagramă_informații.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int index_de_poziție = 0; index_de_poziție < SMS.length; index_de_poziție++)
   if (replică[index_de_poziție] != SMS[index_de_poziție]) throw new RuntimeException("UDP mismatch");
  participant.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'primi_verifica': '''import java.net.*;
public class primi_verifica {
 public static void main(String[] Argumente) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket participant = new DatagramSocket(9301); participant.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Conectează = server_VALUE.accept(); Conectează.setSoTimeout(5000);
  Conectează.getOutputStream().write(Conectează.getInputStream().read() + 1);
  Conectează.close(); server_VALUE.close();
  byte[] date = new byte[64]; DatagramPacket diagramă_informații = new DatagramPacket(date, date.length);
  participant.receive(diagramă_informații); participant.send(diagramă_informații); participant.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nume, SURSĂ in sursă_Fișiere.items():
        (Rezultat / (Nume + '.java')).write_text(SURSĂ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Rezultat)] +
                          [str(Rezultat / (Nume + '.java')) for Nume in sursă_Fișiere])
    LOG_RECORD = bytearray()
    def 빈접속번호(Tip_zonă=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Tip_zonă) as căuta_VALUE:
            căuta_VALUE.bind(('127.0.0.4', 0))
            return căuta_VALUE.getsockname()[1]
    Fișier_număr_port, TCP_muta, UDP_muta = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, punte_3de4fe3a(
                Fișier_număr_port, ['tcp:{}:9300'.format(TCP_muta), 'udp:{}:9301'.format(UDP_muta)],
                captura=True, gazdă_adresa='127.0.0.4') as punte_VALUE:
            control_cale = Path(임시) / 'qmp.sock'
            Proces_VALUE = subprocess.Popen(Comandă() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(control_cale)] + punte_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            alege_element = selectors.DefaultSelector()
            alege_element.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def primi(afișa_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while afișa_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(afișa_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for Cheie_VALUE, _ in alege_element.select(.05):
                        조각 = Cheie_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def trimite(date):
                Proces_VALUE.stdin.write(date)
                Proces_VALUE.stdin.flush()
            def shell(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_RECORD)
                trimite((SMS + '\n').encode())
                return primi(처음=처음)
            primi()
            with socket.socket(socket.AF_UNIX) as control_VALUE:
                control_VALUE.settimeout(10)
                control_VALUE.connect(str(control_cale))
                flux_VALUE = control_VALUE.makefile('rwb')
                json.loads(flux_VALUE.readline())
                def cerere(명령어, Argumente=None):
                    date = {'execute': 명령어}
                    if Argumente is not None:
                        date['arguments'] = Argumente
                    flux_VALUE.write((json.dumps(date) + '\n').encode())
                    flux_VALUE.flush()
                    while True:
                        replică = json.loads(flux_VALUE.readline())
                        if 'error' in replică:
                            raise AssertionError(replică)
                        if 'return' in replică:
                            return replică['return']
                cerere('qmp_capabilities')
                def 권한읽기():
                    cerere('stop')
                    try:
                        return cerere('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        cerere('cont')
                raport_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in raport_VALUE['shell_cpu'], raport_VALUE['shell_cpu']
                raport_VALUE['initial_ps'] = shell('ps')
                assert 'kernel/shell' in raport_VALUE['initial_ps']
                raport_VALUE['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in raport_VALUE['ipconfig']
                raport_VALUE['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in raport_VALUE['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as Transfer_VALUE:
                    Transfer_VALUE.encoding = 'utf-8'
                    Transfer_VALUE.connect('127.0.0.4', Fișier_număr_port, timeout=20)
                    Transfer_VALUE.login()
                    for Nume in sursă_Fișiere:
                        Transfer_VALUE.storbinary('STOR ' + Nume + '.class', io.BytesIO((Rezultat / (Nume + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                trimite('java permisiune_verifica\n'.encode())
                primi(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    raport_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in raport_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in raport_VALUE['java_cpu'], raport_VALUE['java_cpu']
                primi(처음=처음)
                raport_VALUE['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', raport_VALUE['after_exit_ps'])
                raport_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as pereche_VALUE:
                    SMS = shell('java rețea_verifica {} {}'.format(pereche_VALUE.TCP_muta, pereche_VALUE.UDP_muta))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert pereche_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, pereche_VALUE.수신됨
                    assert not pereche_VALUE.오류들, pereche_VALUE.오류들
                    raport_VALUE['outbound_peers'] = {종류: date.decode() for 종류, date in pereche_VALUE.수신됨.items()}
                처음 = len(LOG_RECORD)
                trimite('java primi_verifica\n'.encode())
                primi(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_muta), timeout=5) as pereche_VALUE:
                    pereche_VALUE.sendall(b'A')
                    assert pereche_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as pereche_VALUE:
                    pereche_VALUE.settimeout(5)
                    pereche_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_muta))
                    assert pereche_VALUE.recvfrom(64)[0] == b'UDP-IN'
                SMS = primi(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                raport_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                trimite('java ExempluFereastră\n'.encode())
                primi('GUI 예제 Pregătiți: ExempluFereastră\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                trimite(bytes([30, 2, 1, 0, 0, 0, 0]))
                primi(처음=처음)
                raport_VALUE['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ExempluFereastră', raport_VALUE['suspended_java_ps']), raport_VALUE['suspended_java_ps']
                raport_VALUE['top'] = shell('top -n 1')
                assert 'java ExempluFereastră' in raport_VALUE['top'] and 'kernel/shell' in raport_VALUE['top']
                raport_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                raport_VALUE['network_trace'] = punte_VALUE.jurnal_de_urmărire
                assert not punte_VALUE.eroare, punte_VALUE.eroare
                trimite(b'poweroff\n')
                assert Proces_VALUE.wait(timeout=15) == 0
                raport_VALUE['passed'] = True
            alege_element.close()
    except Exception as eroare:
        raport_VALUE['error'] = str(eroare)
        raise
    finally:
        if Proces_VALUE is not None and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:
                Proces_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_VALUE.kill()
                Proces_VALUE.wait()
        (Rezultat / 'serial.log').write_bytes(LOG_RECORD)
        (Rezultat / 'report.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Cheie_VALUE: raport_VALUE[Cheie_VALUE] for Cheie_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Pornește()
