#!/usr/bin/env python3
"""QEMU의 faktisks_dati CPU atļauja_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Izpildīt_komanda import Project_sakne, Komanda
from tilts_3de4fe3a import tilts_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Palaist():
    Izvade = Project_sakne / 'build/verification/execution-network-review'
    Izvade.mkdir(parents=True, exist_ok=True)
    ziņot_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_sakne / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    avots_Faili = {
        'atļauja_čeks': '''public class atļauja_čeks {
 public static void main(String[] Parametri) {
  System.out.println("EL0_PROBE_READY");
  int numurs = 0; while (true) { numurs++; }
 }
}''',
        'tīkls_čeks': '''import java.net.*;
public class tīkls_čeks {
 public static void main(String[] Parametri) throws Exception {
  Socket Savienoties = new Socket("10.0.2.2", Integer.parseInt(Parametri[0]));
  Savienoties.setSoTimeout(3000);
  byte[] Teksts = "TCP 한글\\n".getBytes("UTF-8");
  Savienoties.getOutputStream().write(Teksts);
  for (int pozīcijas_indekss = 0; pozīcijas_indekss < Teksts.length; pozīcijas_indekss++)
   if (Savienoties.getInputStream().read() != (Teksts[pozīcijas_indekss] & 255)) throw new RuntimeException("TCP mismatch");
  Savienoties.close();
  DatagramSocket dalībnieks = new DatagramSocket(); dalībnieks.setSoTimeout(3000);
  Teksts = "UDP 한글".getBytes("UTF-8");
  dalībnieks.send(new DatagramPacket(Teksts, Teksts.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Parametri[1])));
  byte[] atbilde = new byte[64]; DatagramPacket datogramma = new DatagramPacket(atbilde, atbilde.length);
  dalībnieks.receive(datogramma);
  if (datogramma.getLength() != Teksts.length) throw new RuntimeException("UDP length");
  for (int pozīcijas_indekss = 0; pozīcijas_indekss < Teksts.length; pozīcijas_indekss++)
   if (atbilde[pozīcijas_indekss] != Teksts[pozīcijas_indekss]) throw new RuntimeException("UDP mismatch");
  dalībnieks.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'saņemt_čeks': '''import java.net.*;
public class saņemt_čeks {
 public static void main(String[] Parametri) throws Exception {
  ServerSocket serveris_VALUE = new ServerSocket(9300); serveris_VALUE.setSoTimeout(5000);
  DatagramSocket dalībnieks = new DatagramSocket(9301); dalībnieks.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Savienoties = serveris_VALUE.accept(); Savienoties.setSoTimeout(5000);
  Savienoties.getOutputStream().write(Savienoties.getInputStream().read() + 1);
  Savienoties.close(); serveris_VALUE.close();
  byte[] dati = new byte[64]; DatagramPacket datogramma = new DatagramPacket(dati, dati.length);
  dalībnieks.receive(datogramma); dalībnieks.send(datogramma); dalībnieks.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nosaukums, AVOTS in avots_Faili.items():
        (Izvade / (Nosaukums + '.java')).write_text(AVOTS, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Izvade)] +
                          [str(Izvade / (Nosaukums + '.java')) for Nosaukums in avots_Faili])
    LOG_RECORD = bytearray()
    def 빈접속번호(TYPE_joma=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_joma) as Meklēt_VALUE:
            Meklēt_VALUE.bind(('127.0.0.4', 0))
            return Meklēt_VALUE.getsockname()[1]
    Fails_porta_numurs, TCP_ports, UDP_ports = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Process_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, tilts_3de4fe3a(
                Fails_porta_numurs, ['tcp:{}:9300'.format(TCP_ports), 'udp:{}:9301'.format(UDP_ports)],
                tvert=True, viesot_adrese='127.0.0.4') as tilts_VALUE:
            vadība_ceļš = Path(임시) / 'qmp.sock'
            Process_VALUE = subprocess.Popen(Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(vadība_ceļš)] + tilts_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_krājums = selectors.DefaultSelector()
            CHOOSE_krājums.register(Process_VALUE.stdout, selectors.EVENT_READ)
            def saņemt(rādīt_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while rādīt_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Process_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(rādīt_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for Atslēga_VALUE, _ in CHOOSE_krājums.select(.05):
                        조각 = Atslēga_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def sūtīt(dati):
                Process_VALUE.stdin.write(dati)
                Process_VALUE.stdin.flush()
            def čaula(Teksts):
                print(Teksts, flush=True)
                처음 = len(LOG_RECORD)
                sūtīt((Teksts + '\n').encode())
                return saņemt(처음=처음)
            saņemt()
            with socket.socket(socket.AF_UNIX) as vadība_VALUE:
                vadība_VALUE.settimeout(10)
                vadība_VALUE.connect(str(vadība_ceļš))
                Stream_VALUE = vadība_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def pieprasījums(명령어, Parametri=None):
                    dati = {'execute': 명령어}
                    if Parametri is not None:
                        dati['arguments'] = Parametri
                    Stream_VALUE.write((json.dumps(dati) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        atbilde = json.loads(Stream_VALUE.readline())
                        if 'error' in atbilde:
                            raise AssertionError(atbilde)
                        if 'return' in atbilde:
                            return atbilde['return']
                pieprasījums('qmp_capabilities')
                def 권한읽기():
                    pieprasījums('stop')
                    try:
                        return pieprasījums('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        pieprasījums('cont')
                ziņot_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ziņot_VALUE['shell_cpu'], ziņot_VALUE['shell_cpu']
                ziņot_VALUE['initial_ps'] = čaula('ps')
                assert 'kernel/shell' in ziņot_VALUE['initial_ps']
                ziņot_VALUE['ipconfig'] = čaula('ipconfig')
                assert 'inet 10.0.2.15' in ziņot_VALUE['ipconfig']
                ziņot_VALUE['gateway_ping'] = čaula('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ziņot_VALUE['gateway_ping']
                assert 'FTP listening' in čaula('ftpd start')
                with ftplib.FTP() as nodot_VALUE_630ba093:
                    nodot_VALUE_630ba093.encoding = 'utf-8'
                    nodot_VALUE_630ba093.connect('127.0.0.4', Fails_porta_numurs, timeout=20)
                    nodot_VALUE_630ba093.login()
                    for Nosaukums in avots_Faili:
                        nodot_VALUE_630ba093.storbinary('STOR ' + Nosaukums + '.class', io.BytesIO((Izvade / (Nosaukums + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                sūtīt('java atļauja_čeks\n'.encode())
                saņemt(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ziņot_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in ziņot_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ziņot_VALUE['java_cpu'], ziņot_VALUE['java_cpu']
                saņemt(처음=처음)
                ziņot_VALUE['after_exit_ps'] = čaula('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ziņot_VALUE['after_exit_ps'])
                ziņot_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as vienranga_VALUE:
                    Teksts = čaula('java tīkls_čeks {} {}'.format(vienranga_VALUE.TCP_ports, vienranga_VALUE.UDP_ports))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Teksts and 'exit 0' in Teksts, Teksts
                    assert vienranga_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, vienranga_VALUE.수신됨
                    assert not vienranga_VALUE.오류들, vienranga_VALUE.오류들
                    ziņot_VALUE['outbound_peers'] = {종류: dati.decode() for 종류, dati in vienranga_VALUE.수신됨.items()}
                처음 = len(LOG_RECORD)
                sūtīt('java saņemt_čeks\n'.encode())
                saņemt(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_ports), timeout=5) as vienranga_VALUE:
                    vienranga_VALUE.sendall(b'A')
                    assert vienranga_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as vienranga_VALUE:
                    vienranga_VALUE.settimeout(5)
                    vienranga_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_ports))
                    assert vienranga_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Teksts = saņemt(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Teksts and 'exit 0' in Teksts, Teksts
                ziņot_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in čaula('terminal')
                čaula('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                sūtīt('java LogaPiemērs\n'.encode())
                saņemt('GUI 예제 Sagatavot: LogaPiemērs\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                sūtīt(bytes([30, 2, 1, 0, 0, 0, 0]))
                saņemt(처음=처음)
                ziņot_VALUE['suspended_java_ps'] = čaula('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java LogaPiemērs', ziņot_VALUE['suspended_java_ps']), ziņot_VALUE['suspended_java_ps']
                ziņot_VALUE['top'] = čaula('top -n 1')
                assert 'java LogaPiemērs' in ziņot_VALUE['top'] and 'kernel/shell' in ziņot_VALUE['top']
                ziņot_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ziņot_VALUE['network_trace'] = tilts_VALUE.trasēšanas_žurnāls
                assert not tilts_VALUE.Kļūda, tilts_VALUE.Kļūda
                sūtīt(b'poweroff\n')
                assert Process_VALUE.wait(timeout=15) == 0
                ziņot_VALUE['passed'] = True
            CHOOSE_krājums.close()
    except Exception as Kļūda:
        ziņot_VALUE['error'] = str(Kļūda)
        raise
    finally:
        if Process_VALUE is not None and Process_VALUE.poll() is None:
            Process_VALUE.terminate()
            try:
                Process_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Process_VALUE.kill()
                Process_VALUE.wait()
        (Izvade / 'serial.log').write_bytes(LOG_RECORD)
        (Izvade / 'report.json').write_text(json.dumps(ziņot_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Atslēga_VALUE: ziņot_VALUE[Atslēga_VALUE] for Atslēga_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Palaist()
