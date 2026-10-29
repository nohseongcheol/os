#!/usr/bin/env python3
"""QEMU의 aktuell_Daten CPU Geneemegung_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ausféieren_Befeel import projezéieren_Racinn, Befeel
from Reseau_Bréck import Reseau_Bréck
from 되돌림시험서버 import 되돌림시험서버


def Laf():
    출력 = projezéieren_Racinn / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    mellen_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projezéieren_Racinn / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    Quell_Fichieren = {
        'Geneemegung_Scheck': '''public class Geneemegung_Scheck {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Reseau_Scheck': '''import java.net.*;
public class Reseau_Scheck {
 public static void main(String[] 인수) throws Exception {
  Socket Verbannen = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Verbannen.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  Verbannen.getOutputStream().write(SMS);
  for (int positionéieren_INDEX = 0; positionéieren_INDEX < SMS.length; positionéieren_INDEX++)
   if (Verbannen.getInputStream().read() != (SMS[positionéieren_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Verbannen.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] äntweren = new byte[64]; DatagramPacket 전문 = new DatagramPacket(äntweren, äntweren.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int positionéieren_INDEX = 0; positionéieren_INDEX < SMS.length; positionéieren_INDEX++)
   if (äntweren[positionéieren_INDEX] != SMS[positionéieren_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket Server_VALUE = new ServerSocket(9300); Server_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Verbannen = Server_VALUE.accept(); Verbannen.setSoTimeout(5000);
  Verbannen.getOutputStream().write(Verbannen.getInputStream().read() + 1);
  Verbannen.close(); Server_VALUE.close();
  byte[] Daten = new byte[64]; DatagramPacket 전문 = new DatagramPacket(Daten, Daten.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Numm, Quell in Quell_Fichieren.items():
        (출력 / (Numm + '.java')).write_text(Quell, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Numm + '.java')) for Numm in Quell_Fichieren])
    LOG_Rei = bytearray()
    def 빈접속번호(TYPE_Kategorie=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_Kategorie) as Sich_VALUE:
            Sich_VALUE.bind(('127.0.0.4', 0))
            return Sich_VALUE.getsockname()[1]
    파일접속번호, TCP_Port, UDP_Port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Prozess_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Reseau_Bréck(
                파일접속번호, ['tcp:{}:9300'.format(TCP_Port), 'udp:{}:9301'.format(UDP_Port)],
                ophuelen=True, Host_Adress='127.0.0.4') as Bréck_VALUE:
            Kontroll_Wee = Path(임시) / 'qmp.sock'
            Prozess_VALUE = subprocess.Popen(Befeel() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(Kontroll_Wee)] + Bréck_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_Element = selectors.DefaultSelector()
            CHOOSE_Element.register(Prozess_VALUE.stdout, selectors.EVENT_READ)
            def 받기(Show_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Show_VALUE not in LOG_Rei[처음:]:
                    if time.monotonic() > 끝 or Prozess_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(Show_VALUE) + '\n' + LOG_Rei[처음:].decode('utf-8', 'replace'))
                    for Tast_VALUE, _ in CHOOSE_Element.select(.05):
                        조각 = Tast_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_Rei.extend(조각)
                return LOG_Rei[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def mailen(Daten):
                Prozess_VALUE.stdin.write(Daten)
                Prozess_VALUE.stdin.flush()
            def Shell(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_Rei)
                mailen((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as Kontroll_VALUE:
                Kontroll_VALUE.settimeout(10)
                Kontroll_VALUE.connect(str(Kontroll_Wee))
                Stream_VALUE = Kontroll_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def 요청(Instruktioun_VALUE, 인수=None):
                    Daten = {'execute': Instruktioun_VALUE}
                    if 인수 is not None:
                        Daten['arguments'] = 인수
                    Stream_VALUE.write((json.dumps(Daten) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        äntweren = json.loads(Stream_VALUE.readline())
                        if 'error' in äntweren:
                            raise AssertionError(äntweren)
                        if 'return' in äntweren:
                            return äntweren['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                mellen_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in mellen_VALUE['shell_cpu'], mellen_VALUE['shell_cpu']
                mellen_VALUE['initial_ps'] = Shell('ps')
                assert 'kernel/shell' in mellen_VALUE['initial_ps']
                mellen_VALUE['ipconfig'] = Shell('ipconfig')
                assert 'inet 10.0.2.15' in mellen_VALUE['ipconfig']
                mellen_VALUE['gateway_ping'] = Shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in mellen_VALUE['gateway_ping']
                assert 'FTP listening' in Shell('ftpd start')
                with ftplib.FTP() as Transfer_VALUE:
                    Transfer_VALUE.encoding = 'utf-8'
                    Transfer_VALUE.connect('127.0.0.4', 파일접속번호, timeout=20)
                    Transfer_VALUE.login()
                    for Numm in Quell_Fichieren:
                        Transfer_VALUE.storbinary('STOR ' + Numm + '.class', io.BytesIO((출력 / (Numm + '.class')).read_bytes()))
                처음 = len(LOG_Rei)
                mailen('java Geneemegung_Scheck\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    mellen_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in mellen_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in mellen_VALUE['java_cpu'], mellen_VALUE['java_cpu']
                받기(처음=처음)
                mellen_VALUE['after_exit_ps'] = Shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', mellen_VALUE['after_exit_ps'])
                mellen_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as Peer_VALUE:
                    SMS = Shell('java Reseau_Scheck {} {}'.format(Peer_VALUE.TCP_Port, Peer_VALUE.UDP_Port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert Peer_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, Peer_VALUE.수신됨
                    assert not Peer_VALUE.오류들, Peer_VALUE.오류들
                    mellen_VALUE['outbound_peers'] = {종류: Daten.decode() for 종류, Daten in Peer_VALUE.수신됨.items()}
                처음 = len(LOG_Rei)
                mailen('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_Port), timeout=5) as Peer_VALUE:
                    Peer_VALUE.sendall(b'A')
                    assert Peer_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Peer_VALUE:
                    Peer_VALUE.settimeout(5)
                    Peer_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_Port))
                    assert Peer_VALUE.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                mellen_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Shell('terminal')
                Shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_Rei)
                mailen('java 창예제\n'.encode())
                받기('GUI 예제 Préparéieren: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_Rei)
                mailen(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                mellen_VALUE['suspended_java_ps'] = Shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', mellen_VALUE['suspended_java_ps']), mellen_VALUE['suspended_java_ps']
                mellen_VALUE['top'] = Shell('top -n 1')
                assert 'java 창예제' in mellen_VALUE['top'] and 'kernel/shell' in mellen_VALUE['top']
                mellen_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                mellen_VALUE['network_trace'] = Bréck_VALUE.추적기록
                assert not Bréck_VALUE.Feeler, Bréck_VALUE.Feeler
                mailen(b'poweroff\n')
                assert Prozess_VALUE.wait(timeout=15) == 0
                mellen_VALUE['passed'] = True
            CHOOSE_Element.close()
    except Exception as Feeler:
        mellen_VALUE['error'] = str(Feeler)
        raise
    finally:
        if Prozess_VALUE is not None and Prozess_VALUE.poll() is None:
            Prozess_VALUE.terminate()
            try:
                Prozess_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Prozess_VALUE.kill()
                Prozess_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_Rei)
        (출력 / 'report.json').write_text(json.dumps(mellen_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Tast_VALUE: mellen_VALUE[Tast_VALUE] for Tast_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Laf()
