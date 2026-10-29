#!/usr/bin/env python3
"""QEMU의 attwali_data CPU permess_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from eżegwixxa_kmand import pprojetta_għerq, kmand
from netwerk_pont import netwerk_pont
from 되돌림시험서버 import 되돌림시험서버


def serje():
    출력 = pprojetta_għerq / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    rapport_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((pprojetta_għerq / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    sors_Fajls = {
        'permess_ċekk': '''public class permess_ċekk {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'netwerk_ċekk': '''import java.net.*;
public class netwerk_ċekk {
 public static void main(String[] 인수) throws Exception {
  Socket AQBAD = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  AQBAD.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  AQBAD.getOutputStream().write(SMS);
  for (int pożizzjoni_INDEX = 0; pożizzjoni_INDEX < SMS.length; pożizzjoni_INDEX++)
   if (AQBAD.getInputStream().read() != (SMS[pożizzjoni_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  AQBAD.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] wieġeb = new byte[64]; DatagramPacket 전문 = new DatagramPacket(wieġeb, wieġeb.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int pożizzjoni_INDEX = 0; pożizzjoni_INDEX < SMS.length; pożizzjoni_INDEX++)
   if (wieġeb[pożizzjoni_INDEX] != SMS[pożizzjoni_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket AQBAD = server_VALUE.accept(); AQBAD.setSoTimeout(5000);
  AQBAD.getOutputStream().write(AQBAD.getInputStream().read() + 1);
  AQBAD.close(); server_VALUE.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for isem, sors in sors_Fajls.items():
        (출력 / (isem + '.java')).write_text(sors, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (isem + '.java')) for isem in sors_Fajls])
    LOG_RECORD = bytearray()
    def 빈접속번호(TYPE_kategorija=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_kategorija) as SEARCH_VALUE:
            SEARCH_VALUE.bind(('127.0.0.4', 0))
            return SEARCH_VALUE.getsockname()[1]
    파일접속번호, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proċess_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, netwerk_pont(
                파일접속번호, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                iġbed=True, host_ADDRESS='127.0.0.4') as pont_VALUE:
            kontroll_mogħdija = Path(임시) / 'qmp.sock'
            Proċess_VALUE = subprocess.Popen(kmand() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontroll_mogħdija)] + pont_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_element = selectors.DefaultSelector()
            CHOOSE_element.register(Proċess_VALUE.stdout, selectors.EVENT_READ)
            def 받기(wera_VALUE_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while wera_VALUE_487749b8 not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proċess_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(wera_VALUE_487749b8) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for tast_VALUE, _ in CHOOSE_element.select(.05):
                        조각 = tast_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def bagħat(data):
                Proċess_VALUE.stdin.write(data)
                Proċess_VALUE.stdin.flush()
            def shell(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_RECORD)
                bagħat((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as kontroll_VALUE:
                kontroll_VALUE.settimeout(10)
                kontroll_VALUE.connect(str(kontroll_mogħdija))
                Stream_VALUE = kontroll_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def 요청(istruzzjoni_VALUE, 인수=None):
                    data = {'execute': istruzzjoni_VALUE}
                    if 인수 is not None:
                        data['arguments'] = 인수
                    Stream_VALUE.write((json.dumps(data) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        wieġeb = json.loads(Stream_VALUE.readline())
                        if 'error' in wieġeb:
                            raise AssertionError(wieġeb)
                        if 'return' in wieġeb:
                            return wieġeb['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                rapport_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in rapport_VALUE['shell_cpu'], rapport_VALUE['shell_cpu']
                rapport_VALUE['initial_ps'] = shell('ps')
                assert 'kernel/shell' in rapport_VALUE['initial_ps']
                rapport_VALUE['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in rapport_VALUE['ipconfig']
                rapport_VALUE['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in rapport_VALUE['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as trasferiment_VALUE:
                    trasferiment_VALUE.encoding = 'utf-8'
                    trasferiment_VALUE.connect('127.0.0.4', 파일접속번호, timeout=20)
                    trasferiment_VALUE.login()
                    for isem in sors_Fajls:
                        trasferiment_VALUE.storbinary('STOR ' + isem + '.class', io.BytesIO((출력 / (isem + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                bagħat('java permess_ċekk\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    rapport_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in rapport_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in rapport_VALUE['java_cpu'], rapport_VALUE['java_cpu']
                받기(처음=처음)
                rapport_VALUE['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', rapport_VALUE['after_exit_ps'])
                rapport_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as peer_VALUE:
                    SMS = shell('java netwerk_ċekk {} {}'.format(peer_VALUE.TCP_port, peer_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert peer_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_VALUE.수신됨
                    assert not peer_VALUE.오류들, peer_VALUE.오류들
                    rapport_VALUE['outbound_peers'] = {종류: data.decode() for 종류, data in peer_VALUE.수신됨.items()}
                처음 = len(LOG_RECORD)
                bagħat('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as peer_VALUE:
                    peer_VALUE.sendall(b'A')
                    assert peer_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_VALUE:
                    peer_VALUE.settimeout(5)
                    peer_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert peer_VALUE.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                rapport_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                bagħat('java 창예제\n'.encode())
                받기('GUI 예제 Ħejji: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                bagħat(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                rapport_VALUE['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', rapport_VALUE['suspended_java_ps']), rapport_VALUE['suspended_java_ps']
                rapport_VALUE['top'] = shell('top -n 1')
                assert 'java 창예제' in rapport_VALUE['top'] and 'kernel/shell' in rapport_VALUE['top']
                rapport_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                rapport_VALUE['network_trace'] = pont_VALUE.traċċar_LOG
                assert not pont_VALUE.żball, pont_VALUE.żball
                bagħat(b'poweroff\n')
                assert Proċess_VALUE.wait(timeout=15) == 0
                rapport_VALUE['passed'] = True
            CHOOSE_element.close()
    except Exception as żball:
        rapport_VALUE['error'] = str(żball)
        raise
    finally:
        if Proċess_VALUE is not None and Proċess_VALUE.poll() is None:
            Proċess_VALUE.terminate()
            try:
                Proċess_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proċess_VALUE.kill()
                Proċess_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_RECORD)
        (출력 / 'report.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tast_VALUE: rapport_VALUE[tast_VALUE] for tast_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    serje()
