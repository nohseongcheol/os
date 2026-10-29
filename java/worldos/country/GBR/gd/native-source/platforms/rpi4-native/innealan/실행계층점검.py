#!/usr/bin/env python3
"""QEMU의 dearbh_dàta CPU cead_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from gnìomhaich_àithne import tilg_freumh, àithne
from lìonra_drochaid import lìonra_drochaid
from 되돌림시험서버 import 되돌림시험서버


def ruith():
    출력 = tilg_freumh / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    aithisg_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((tilg_freumh / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    tùs_faidhlichean = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'lìonra_seic': '''import java.net.*;
public class lìonra_seic {
 public static void main(String[] 인수) throws Exception {
  Socket CONNECT = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  CONNECT.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  CONNECT.getOutputStream().write(SMS);
  for (int suidhich_INDEX = 0; suidhich_INDEX < SMS.length; suidhich_INDEX++)
   if (CONNECT.getInputStream().read() != (SMS[suidhich_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  CONNECT.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] freagair = new byte[64]; DatagramPacket 전문 = new DatagramPacket(freagair, freagair.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int suidhich_INDEX = 0; suidhich_INDEX < SMS.length; suidhich_INDEX++)
   if (freagair[suidhich_INDEX] != SMS[suidhich_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket frithealaiche_VALUE = new ServerSocket(9300); frithealaiche_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket CONNECT = frithealaiche_VALUE.accept(); CONNECT.setSoTimeout(5000);
  CONNECT.getOutputStream().write(CONNECT.getInputStream().read() + 1);
  CONNECT.close(); frithealaiche_VALUE.close();
  byte[] dàta = new byte[64]; DatagramPacket 전문 = new DatagramPacket(dàta, dàta.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ainm, tùs in tùs_faidhlichean.items():
        (출력 / (Ainm + '.java')).write_text(tùs, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Ainm + '.java')) for Ainm in tùs_faidhlichean])
    LOG_ràgh = bytearray()
    def 빈접속번호(TYPE_roinn_seòrsa=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_roinn_seòrsa) as lorg_VALUE:
            lorg_VALUE.bind(('127.0.0.4', 0))
            return lorg_VALUE.getsockname()[1]
    파일접속번호, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Pròiseas_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, lìonra_drochaid(
                파일접속번호, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                glac=True, òstair_ADDRESS='127.0.0.4') as drochaid_VALUE:
            smachd_slighe = Path(임시) / 'qmp.sock'
            Pròiseas_VALUE = subprocess.Popen(àithne() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(smachd_slighe)] + drochaid_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            tagh_nì = selectors.DefaultSelector()
            tagh_nì.register(Pròiseas_VALUE.stdout, selectors.EVENT_READ)
            def 받기(show_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while show_VALUE not in LOG_ràgh[처음:]:
                    if time.monotonic() > 끝 or Pròiseas_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(show_VALUE) + '\n' + LOG_ràgh[처음:].decode('utf-8', 'replace'))
                    for Iuchair_VALUE, _ in tagh_nì.select(.05):
                        조각 = Iuchair_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_ràgh.extend(조각)
                return LOG_ràgh[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def cuir(dàta):
                Pròiseas_VALUE.stdin.write(dàta)
                Pròiseas_VALUE.stdin.flush()
            def slige(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_ràgh)
                cuir((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as smachd_VALUE:
                smachd_VALUE.settimeout(10)
                smachd_VALUE.connect(str(smachd_slighe))
                sruth_VALUE = smachd_VALUE.makefile('rwb')
                json.loads(sruth_VALUE.readline())
                def 요청(treòrachadh_VALUE, 인수=None):
                    dàta = {'execute': treòrachadh_VALUE}
                    if 인수 is not None:
                        dàta['arguments'] = 인수
                    sruth_VALUE.write((json.dumps(dàta) + '\n').encode())
                    sruth_VALUE.flush()
                    while True:
                        freagair = json.loads(sruth_VALUE.readline())
                        if 'error' in freagair:
                            raise AssertionError(freagair)
                        if 'return' in freagair:
                            return freagair['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                aithisg_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in aithisg_VALUE['shell_cpu'], aithisg_VALUE['shell_cpu']
                aithisg_VALUE['initial_ps'] = slige('ps')
                assert 'kernel/shell' in aithisg_VALUE['initial_ps']
                aithisg_VALUE['ipconfig'] = slige('ipconfig')
                assert 'inet 10.0.2.15' in aithisg_VALUE['ipconfig']
                aithisg_VALUE['gateway_ping'] = slige('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in aithisg_VALUE['gateway_ping']
                assert 'FTP listening' in slige('ftpd start')
                with ftplib.FTP() as tar_chur_VALUE:
                    tar_chur_VALUE.encoding = 'utf-8'
                    tar_chur_VALUE.connect('127.0.0.4', 파일접속번호, timeout=20)
                    tar_chur_VALUE.login()
                    for Ainm in tùs_faidhlichean:
                        tar_chur_VALUE.storbinary('STOR ' + Ainm + '.class', io.BytesIO((출력 / (Ainm + '.class')).read_bytes()))
                처음 = len(LOG_ràgh)
                cuir('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    aithisg_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in aithisg_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in aithisg_VALUE['java_cpu'], aithisg_VALUE['java_cpu']
                받기(처음=처음)
                aithisg_VALUE['after_exit_ps'] = slige('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', aithisg_VALUE['after_exit_ps'])
                aithisg_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as seise_VALUE:
                    SMS = slige('java lìonra_seic {} {}'.format(seise_VALUE.TCP_port, seise_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert seise_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, seise_VALUE.수신됨
                    assert not seise_VALUE.오류들, seise_VALUE.오류들
                    aithisg_VALUE['outbound_peers'] = {종류: dàta.decode() for 종류, dàta in seise_VALUE.수신됨.items()}
                처음 = len(LOG_ràgh)
                cuir('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as seise_VALUE:
                    seise_VALUE.sendall(b'A')
                    assert seise_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as seise_VALUE:
                    seise_VALUE.settimeout(5)
                    seise_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert seise_VALUE.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                aithisg_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in slige('terminal')
                slige('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_ràgh)
                cuir('java 창예제\n'.encode())
                받기('GUI 예제 Ullaich: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_ràgh)
                cuir(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                aithisg_VALUE['suspended_java_ps'] = slige('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', aithisg_VALUE['suspended_java_ps']), aithisg_VALUE['suspended_java_ps']
                aithisg_VALUE['top'] = slige('top -n 1')
                assert 'java 창예제' in aithisg_VALUE['top'] and 'kernel/shell' in aithisg_VALUE['top']
                aithisg_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                aithisg_VALUE['network_trace'] = drochaid_VALUE.treus_LOG
                assert not drochaid_VALUE.Mearachd, drochaid_VALUE.Mearachd
                cuir(b'poweroff\n')
                assert Pròiseas_VALUE.wait(timeout=15) == 0
                aithisg_VALUE['passed'] = True
            tagh_nì.close()
    except Exception as Mearachd:
        aithisg_VALUE['error'] = str(Mearachd)
        raise
    finally:
        if Pròiseas_VALUE is not None and Pròiseas_VALUE.poll() is None:
            Pròiseas_VALUE.terminate()
            try:
                Pròiseas_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Pròiseas_VALUE.kill()
                Pròiseas_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_ràgh)
        (출력 / 'report.json').write_text(json.dumps(aithisg_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Iuchair_VALUE: aithisg_VALUE[Iuchair_VALUE] for Iuchair_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ruith()
