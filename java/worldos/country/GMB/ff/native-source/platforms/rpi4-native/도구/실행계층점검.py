#!/usr/bin/env python3
"""QEMU의 laatii_keɓe CPU 권한, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from 실행 import 기준, ginol
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def huutoraade():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ciimtol_njaru = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    원문들 = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'laylaytol_sek': '''import java.net.*;
public class laylaytol_sek {
 public static void main(String[] 인수) throws Exception {
  Socket seŋaade = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  seŋaade.setSoTimeout(3000);
  byte[] binndi = "TCP 한글\\n".getBytes("UTF-8");
  seŋaade.getOutputStream().write(binndi);
  for (int 자리 = 0; 자리 < binndi.length; 자리++)
   if (seŋaade.getInputStream().read() != (binndi[자리] & 255)) throw new RuntimeException("TCP mismatch");
  seŋaade.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  binndi = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(binndi, binndi.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] 응답 = new byte[64]; DatagramPacket 전문 = new DatagramPacket(응답, 응답.length);
  종단.receive(전문);
  if (전문.getLength() != binndi.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < binndi.length; 자리++)
   if (응답[자리] != binndi[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket sarworde_njaru = new ServerSocket(9300); sarworde_njaru.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket seŋaade = sarworde_njaru.accept(); seŋaade.setSoTimeout(5000);
  seŋaade.getOutputStream().write(seŋaade.getInputStream().read() + 1);
  seŋaade.close(); sarworde_njaru.close();
  byte[] keɓe = new byte[64]; DatagramPacket 전문 = new DatagramPacket(keɓe, keɓe.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for innde, sewnde in 원문들.items():
        (출력 / (innde + '.java')).write_text(sewnde, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (innde + '.java')) for innde in 원문들])
    suurnal_winndande = bytearray()
    def 빈접속번호(유형=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 유형) as njiilawu_njaru:
            njiilawu_njaru.bind(('127.0.0.4', 0))
            return njiilawu_njaru.getsockname()[1]
    파일접속번호, TCP_poor, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Yuɓɓo_golle_njaru = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_poor), 'udp:{}:9301'.format(전문접속번호)],
                포착여부=True, njaatigi_ñiiɓirde='127.0.0.4') as 다리:
            yuurnitorde_laawol = Path(임시) / 'qmp.sock'
            Yuɓɓo_golle_njaru = subprocess.Popen(ginol() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(yuurnitorde_laawol)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            labaade_geɗal = selectors.DefaultSelector()
            labaade_geɗal.register(Yuɓɓo_golle_njaru.stdout, selectors.EVENT_READ)
            def 받기(hollirde_njaru=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while hollirde_njaru not in suurnal_winndande[처음:]:
                    if time.monotonic() > 끝 or Yuɓɓo_golle_njaru.poll() is not None:
                        raise AssertionError('Missing ' + repr(hollirde_njaru) + '\n' + suurnal_winndande[처음:].decode('utf-8', 'replace'))
                    for kelal_njaru, _ in labaade_geɗal.select(.05):
                        조각 = kelal_njaru.fileobj.read(65536)
                        if 조각:
                            suurnal_winndande.extend(조각)
                return suurnal_winndande[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def neldude(keɓe):
                Yuɓɓo_golle_njaru.stdin.write(keɓe)
                Yuɓɓo_golle_njaru.stdin.flush()
            def laalagal(binndi):
                print(binndi, flush=True)
                처음 = len(suurnal_winndande)
                neldude((binndi + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as yuurnitorde_njaru:
                yuurnitorde_njaru.settimeout(10)
                yuurnitorde_njaru.connect(str(yuurnitorde_laawol))
                waraango_njaru = yuurnitorde_njaru.makefile('rwb')
                json.loads(waraango_njaru.readline())
                def 요청(yamiroore_njaru, 인수=None):
                    keɓe = {'execute': yamiroore_njaru}
                    if 인수 is not None:
                        keɓe['arguments'] = 인수
                    waraango_njaru.write((json.dumps(keɓe) + '\n').encode())
                    waraango_njaru.flush()
                    while True:
                        응답 = json.loads(waraango_njaru.readline())
                        if 'error' in 응답:
                            raise AssertionError(응답)
                        if 'return' in 응답:
                            return 응답['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ciimtol_njaru['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ciimtol_njaru['shell_cpu'], ciimtol_njaru['shell_cpu']
                ciimtol_njaru['initial_ps'] = laalagal('ps')
                assert 'kernel/shell' in ciimtol_njaru['initial_ps']
                ciimtol_njaru['ipconfig'] = laalagal('ipconfig')
                assert 'inet 10.0.2.15' in ciimtol_njaru['ipconfig']
                ciimtol_njaru['gateway_ping'] = laalagal('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ciimtol_njaru['gateway_ping']
                assert 'FTP listening' in laalagal('ftpd start')
                with ftplib.FTP() as egginde_njaru:
                    egginde_njaru.encoding = 'utf-8'
                    egginde_njaru.connect('127.0.0.4', 파일접속번호, timeout=20)
                    egginde_njaru.login()
                    for innde in 원문들:
                        egginde_njaru.storbinary('STOR ' + innde + '.class', io.BytesIO((출력 / (innde + '.class')).read_bytes()))
                처음 = len(suurnal_winndande)
                neldude('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ciimtol_njaru['java_cpu'] = 권한읽기()
                    if 'EL0t' in ciimtol_njaru['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ciimtol_njaru['java_cpu'], ciimtol_njaru['java_cpu']
                받기(처음=처음)
                ciimtol_njaru['after_exit_ps'] = laalagal('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ciimtol_njaru['after_exit_ps'])
                ciimtol_njaru['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as giƴiraaɗo_njaru:
                    binndi = laalagal('java laylaytol_sek {} {}'.format(giƴiraaɗo_njaru.TCP_poor, giƴiraaɗo_njaru.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in binndi and 'exit 0' in binndi, binndi
                    assert giƴiraaɗo_njaru.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, giƴiraaɗo_njaru.수신됨
                    assert not giƴiraaɗo_njaru.오류들, giƴiraaɗo_njaru.오류들
                    ciimtol_njaru['outbound_peers'] = {종류: keɓe.decode() for 종류, keɓe in giƴiraaɗo_njaru.수신됨.items()}
                처음 = len(suurnal_winndande)
                neldude('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_poor), timeout=5) as giƴiraaɗo_njaru:
                    giƴiraaɗo_njaru.sendall(b'A')
                    assert giƴiraaɗo_njaru.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as giƴiraaɗo_njaru:
                    giƴiraaɗo_njaru.settimeout(5)
                    giƴiraaɗo_njaru.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert giƴiraaɗo_njaru.recvfrom(64)[0] == b'UDP-IN'
                binndi = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in binndi and 'exit 0' in binndi, binndi
                ciimtol_njaru['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in laalagal('terminal')
                laalagal('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(suurnal_winndande)
                neldude('java 창예제\n'.encode())
                받기('GUI 예제 Heblu: 창예제\r\n'.encode(), 처음)
                처음 = len(suurnal_winndande)
                neldude(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ciimtol_njaru['suspended_java_ps'] = laalagal('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ciimtol_njaru['suspended_java_ps']), ciimtol_njaru['suspended_java_ps']
                ciimtol_njaru['top'] = laalagal('top -n 1')
                assert 'java 창예제' in ciimtol_njaru['top'] and 'kernel/shell' in ciimtol_njaru['top']
                ciimtol_njaru['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ciimtol_njaru['network_trace'] = 다리.추적기록
                assert not 다리.juumre, 다리.juumre
                neldude(b'poweroff\n')
                assert Yuɓɓo_golle_njaru.wait(timeout=15) == 0
                ciimtol_njaru['passed'] = True
            labaade_geɗal.close()
    except Exception as juumre:
        ciimtol_njaru['error'] = str(juumre)
        raise
    finally:
        if Yuɓɓo_golle_njaru is not None and Yuɓɓo_golle_njaru.poll() is None:
            Yuɓɓo_golle_njaru.terminate()
            try:
                Yuɓɓo_golle_njaru.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Yuɓɓo_golle_njaru.kill()
                Yuɓɓo_golle_njaru.wait()
        (출력 / 'serial.log').write_bytes(suurnal_winndande)
        (출력 / 'report.json').write_text(json.dumps(ciimtol_njaru, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({kelal_njaru: ciimtol_njaru[kelal_njaru] for kelal_njaru in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    huutoraade()
