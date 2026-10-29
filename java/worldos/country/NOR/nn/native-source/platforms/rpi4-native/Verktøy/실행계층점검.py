#!/usr/bin/env python3
"""QEMU의 faktisk_data CPU løyve_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Utfør_kommando import spegle_rot, Kommando
from Nettverk_bru import Nettverk_bru
from 되돌림시험서버 import 되돌림시험서버


def Køyr_2():
    Utdata = spegle_rot / 'build/verification/execution-network-review'
    Utdata.mkdir(parents=True, exist_ok=True)
    rapport_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((spegle_rot / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    kjelde_Filer = {
        'løyve_sjekk': '''public class løyve_sjekk {
 public static void main(String[] Argument) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Nettverk_sjekk': '''import java.net.*;
public class Nettverk_sjekk {
 public static void main(String[] Argument) throws Exception {
  Socket Kopla_til = new Socket("10.0.2.2", Integer.parseInt(Argument[0]));
  Kopla_til.setSoTimeout(3000);
  byte[] Tekst = "TCP 한글\\n".getBytes("UTF-8");
  Kopla_til.getOutputStream().write(Tekst);
  for (int plassere_INDEX = 0; plassere_INDEX < Tekst.length; plassere_INDEX++)
   if (Kopla_til.getInputStream().read() != (Tekst[plassere_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Kopla_til.close();
  DatagramSocket endepunkt = new DatagramSocket(); endepunkt.setSoTimeout(3000);
  Tekst = "UDP 한글".getBytes("UTF-8");
  endepunkt.send(new DatagramPacket(Tekst, Tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argument[1])));
  byte[] svare = new byte[64]; DatagramPacket 전문 = new DatagramPacket(svare, svare.length);
  endepunkt.receive(전문);
  if (전문.getLength() != Tekst.length) throw new RuntimeException("UDP length");
  for (int plassere_INDEX = 0; plassere_INDEX < Tekst.length; plassere_INDEX++)
   if (svare[plassere_INDEX] != Tekst[plassere_INDEX]) throw new RuntimeException("UDP mismatch");
  endepunkt.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Argument) throws Exception {
  ServerSocket tenar_VALUE = new ServerSocket(9300); tenar_VALUE.setSoTimeout(5000);
  DatagramSocket endepunkt = new DatagramSocket(9301); endepunkt.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Kopla_til = tenar_VALUE.accept(); Kopla_til.setSoTimeout(5000);
  Kopla_til.getOutputStream().write(Kopla_til.getInputStream().read() + 1);
  Kopla_til.close(); tenar_VALUE.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  endepunkt.receive(전문); endepunkt.send(전문); endepunkt.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Namn, KJELDE in kjelde_Filer.items():
        (Utdata / (Namn + '.java')).write_text(KJELDE, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Utdata)] +
                          [str(Utdata / (Namn + '.java')) for Namn in kjelde_Filer])
    LOG_rad = bytearray()
    def tom_portnummer(TYPE_kategori=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_kategori) as Søk_VALUE:
            Søk_VALUE.bind(('127.0.0.4', 0))
            return Søk_VALUE.getsockname()[1]
    fil_portnummer, TCP_port, 전문접속번호 = tom_portnummer(), tom_portnummer(), tom_portnummer(socket.SOCK_DGRAM)
    Prosess_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Nettverk_bru(
                fil_portnummer, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(전문접속번호)],
                ta_opp=True, vert_ADDRESS='127.0.0.4') as bru_VALUE:
            styring_bane = Path(임시) / 'qmp.sock'
            Prosess_VALUE = subprocess.Popen(Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(styring_bane)] + bru_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            velje_vare = selectors.DefaultSelector()
            velje_vare.register(Prosess_VALUE.stdout, selectors.EVENT_READ)
            def 받기(vise_VALUE_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while vise_VALUE_487749b8 not in LOG_rad[처음:]:
                    if time.monotonic() > 끝 or Prosess_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(vise_VALUE_487749b8) + '\n' + LOG_rad[처음:].decode('utf-8', 'replace'))
                    for tast_VALUE, _ in velje_vare.select(.05):
                        조각 = tast_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_rad.extend(조각)
                return LOG_rad[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def sende(data):
                Prosess_VALUE.stdin.write(data)
                Prosess_VALUE.stdin.flush()
            def grensesnitt(Tekst):
                print(Tekst, flush=True)
                처음 = len(LOG_rad)
                sende((Tekst + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as styring_VALUE:
                styring_VALUE.settimeout(10)
                styring_VALUE.connect(str(styring_bane))
                Stream_VALUE = styring_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def 요청(instruksjon_VALUE, Argument=None):
                    data = {'execute': instruksjon_VALUE}
                    if Argument is not None:
                        data['arguments'] = Argument
                    Stream_VALUE.write((json.dumps(data) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        svare = json.loads(Stream_VALUE.readline())
                        if 'error' in svare:
                            raise AssertionError(svare)
                        if 'return' in svare:
                            return svare['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                rapport_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in rapport_VALUE['shell_cpu'], rapport_VALUE['shell_cpu']
                rapport_VALUE['initial_ps'] = grensesnitt('ps')
                assert 'kernel/shell' in rapport_VALUE['initial_ps']
                rapport_VALUE['ipconfig'] = grensesnitt('ipconfig')
                assert 'inet 10.0.2.15' in rapport_VALUE['ipconfig']
                rapport_VALUE['gateway_ping'] = grensesnitt('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in rapport_VALUE['gateway_ping']
                assert 'FTP listening' in grensesnitt('ftpd start')
                with ftplib.FTP() as Overfør_VALUE:
                    Overfør_VALUE.encoding = 'utf-8'
                    Overfør_VALUE.connect('127.0.0.4', fil_portnummer, timeout=20)
                    Overfør_VALUE.login()
                    for Namn in kjelde_Filer:
                        Overfør_VALUE.storbinary('STOR ' + Namn + '.class', io.BytesIO((Utdata / (Namn + '.class')).read_bytes()))
                처음 = len(LOG_rad)
                sende('java løyve_sjekk\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    rapport_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in rapport_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in rapport_VALUE['java_cpu'], rapport_VALUE['java_cpu']
                받기(처음=처음)
                rapport_VALUE['after_exit_ps'] = grensesnitt('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', rapport_VALUE['after_exit_ps'])
                rapport_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as node_VALUE_6a3b6fa7:
                    Tekst = grensesnitt('java Nettverk_sjekk {} {}'.format(node_VALUE_6a3b6fa7.TCP_port, node_VALUE_6a3b6fa7.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                    assert node_VALUE_6a3b6fa7.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, node_VALUE_6a3b6fa7.수신됨
                    assert not node_VALUE_6a3b6fa7.오류들, node_VALUE_6a3b6fa7.오류들
                    rapport_VALUE['outbound_peers'] = {종류: data.decode() for 종류, data in node_VALUE_6a3b6fa7.수신됨.items()}
                처음 = len(LOG_rad)
                sende('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as node_VALUE_6a3b6fa7:
                    node_VALUE_6a3b6fa7.sendall(b'A')
                    assert node_VALUE_6a3b6fa7.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as node_VALUE_6a3b6fa7:
                    node_VALUE_6a3b6fa7.settimeout(5)
                    node_VALUE_6a3b6fa7.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert node_VALUE_6a3b6fa7.recvfrom(64)[0] == b'UDP-IN'
                Tekst = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                rapport_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in grensesnitt('terminal')
                grensesnitt('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_rad)
                sende('java 창예제\n'.encode())
                받기('GUI 예제 Klargjer: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_rad)
                sende(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                rapport_VALUE['suspended_java_ps'] = grensesnitt('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', rapport_VALUE['suspended_java_ps']), rapport_VALUE['suspended_java_ps']
                rapport_VALUE['top'] = grensesnitt('top -n 1')
                assert 'java 창예제' in rapport_VALUE['top'] and 'kernel/shell' in rapport_VALUE['top']
                rapport_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                rapport_VALUE['network_trace'] = bru_VALUE.spor_LOG
                assert not bru_VALUE.FEIL, bru_VALUE.FEIL
                sende(b'poweroff\n')
                assert Prosess_VALUE.wait(timeout=15) == 0
                rapport_VALUE['passed'] = True
            velje_vare.close()
    except Exception as FEIL:
        rapport_VALUE['error'] = str(FEIL)
        raise
    finally:
        if Prosess_VALUE is not None and Prosess_VALUE.poll() is None:
            Prosess_VALUE.terminate()
            try:
                Prosess_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Prosess_VALUE.kill()
                Prosess_VALUE.wait()
        (Utdata / 'serial.log').write_bytes(LOG_rad)
        (Utdata / 'report.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tast_VALUE: rapport_VALUE[tast_VALUE] for tast_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Køyr_2()
