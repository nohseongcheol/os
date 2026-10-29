#!/usr/bin/env python3
"""QEMU의 nyakuri_amakurushingiro CPU 권한, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from gukora_ibwiriza import 기준, Icyo_wifuza
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def ihuriro():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    raporo_agaciro = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    inkomoko_Dosiye = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Urusobemiyoboro_sheki': '''import java.net.*;
public class Urusobemiyoboro_sheki {
 public static void main(String[] 인수) throws Exception {
  Socket Guhuza = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Guhuza.setSoTimeout(3000);
  byte[] Umwandiko = "TCP 한글\\n".getBytes("UTF-8");
  Guhuza.getOutputStream().write(Umwandiko);
  for (int 자리 = 0; 자리 < Umwandiko.length; 자리++)
   if (Guhuza.getInputStream().read() != (Umwandiko[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Guhuza.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Umwandiko = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Umwandiko, Umwandiko.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] gusubiza = new byte[64]; DatagramPacket 전문 = new DatagramPacket(gusubiza, gusubiza.length);
  종단.receive(전문);
  if (전문.getLength() != Umwandiko.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Umwandiko.length; 자리++)
   if (gusubiza[자리] != Umwandiko[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket seriveri_agaciro = new ServerSocket(9300); seriveri_agaciro.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Guhuza = seriveri_agaciro.accept(); Guhuza.setSoTimeout(5000);
  Guhuza.getOutputStream().write(Guhuza.getInputStream().read() + 1);
  Guhuza.close(); seriveri_agaciro.close();
  byte[] amakurushingiro = new byte[64]; DatagramPacket 전문 = new DatagramPacket(amakurushingiro, amakurushingiro.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Izina, Inkomoko in inkomoko_Dosiye.items():
        (출력 / (Izina + '.java')).write_text(Inkomoko, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Izina + '.java')) for Izina in inkomoko_Dosiye])
    kubika_umurongo = bytearray()
    def 빈접속번호(유형=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 유형) as Gushaka_agaciro:
            Gushaka_agaciro.bind(('127.0.0.4', 0))
            return Gushaka_agaciro.getsockname()[1]
    파일접속번호, TCP_poti, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Inzira_agaciro = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_poti), 'udp:{}:9301'.format(전문접속번호)],
                ishusho_ba7b8054=True, gucumbikira_aderesi='127.0.0.4') as 다리:
            icunga_inzira = Path(임시) / 'qmp.sock'
            Inzira_agaciro = subprocess.Popen(Icyo_wifuza() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(icunga_inzira)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            guhitamo_igice = selectors.DefaultSelector()
            guhitamo_igice.register(Inzira_agaciro.stdout, selectors.EVENT_READ)
            def 받기(kugaragaza_agaciro=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while kugaragaza_agaciro not in kubika_umurongo[처음:]:
                    if time.monotonic() > 끝 or Inzira_agaciro.poll() is not None:
                        raise AssertionError('Missing ' + repr(kugaragaza_agaciro) + '\n' + kubika_umurongo[처음:].decode('utf-8', 'replace'))
                    for buto_agaciro, _ in guhitamo_igice.select(.05):
                        조각 = buto_agaciro.fileobj.read(65536)
                        if 조각:
                            kubika_umurongo.extend(조각)
                return kubika_umurongo[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def kohereza(amakurushingiro):
                Inzira_agaciro.stdin.write(amakurushingiro)
                Inzira_agaciro.stdin.flush()
            def insomamabwiriza(Umwandiko):
                print(Umwandiko, flush=True)
                처음 = len(kubika_umurongo)
                kohereza((Umwandiko + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as icunga_agaciro:
                icunga_agaciro.settimeout(10)
                icunga_agaciro.connect(str(icunga_inzira))
                Stream_agaciro = icunga_agaciro.makefile('rwb')
                json.loads(Stream_agaciro.readline())
                def 요청(ibwiriza_agaciro_4c26ea1b, 인수=None):
                    amakurushingiro = {'execute': ibwiriza_agaciro_4c26ea1b}
                    if 인수 is not None:
                        amakurushingiro['arguments'] = 인수
                    Stream_agaciro.write((json.dumps(amakurushingiro) + '\n').encode())
                    Stream_agaciro.flush()
                    while True:
                        gusubiza = json.loads(Stream_agaciro.readline())
                        if 'error' in gusubiza:
                            raise AssertionError(gusubiza)
                        if 'return' in gusubiza:
                            return gusubiza['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                raporo_agaciro['shell_cpu'] = 권한읽기()
                assert 'EL1h' in raporo_agaciro['shell_cpu'], raporo_agaciro['shell_cpu']
                raporo_agaciro['initial_ps'] = insomamabwiriza('ps')
                assert 'kernel/shell' in raporo_agaciro['initial_ps']
                raporo_agaciro['ipconfig'] = insomamabwiriza('ipconfig')
                assert 'inet 10.0.2.15' in raporo_agaciro['ipconfig']
                raporo_agaciro['gateway_ping'] = insomamabwiriza('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in raporo_agaciro['gateway_ping']
                assert 'FTP listening' in insomamabwiriza('ftpd start')
                with ftplib.FTP() as iyimura_agaciro:
                    iyimura_agaciro.encoding = 'utf-8'
                    iyimura_agaciro.connect('127.0.0.4', 파일접속번호, timeout=20)
                    iyimura_agaciro.login()
                    for Izina in inkomoko_Dosiye:
                        iyimura_agaciro.storbinary('STOR ' + Izina + '.class', io.BytesIO((출력 / (Izina + '.class')).read_bytes()))
                처음 = len(kubika_umurongo)
                kohereza('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    raporo_agaciro['java_cpu'] = 권한읽기()
                    if 'EL0t' in raporo_agaciro['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in raporo_agaciro['java_cpu'], raporo_agaciro['java_cpu']
                받기(처음=처음)
                raporo_agaciro['after_exit_ps'] = insomamabwiriza('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', raporo_agaciro['after_exit_ps'])
                raporo_agaciro['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as Mugenzi_agaciro:
                    Umwandiko = insomamabwiriza('java Urusobemiyoboro_sheki {} {}'.format(Mugenzi_agaciro.TCP_poti, Mugenzi_agaciro.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
                    assert Mugenzi_agaciro.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, Mugenzi_agaciro.수신됨
                    assert not Mugenzi_agaciro.오류들, Mugenzi_agaciro.오류들
                    raporo_agaciro['outbound_peers'] = {종류: amakurushingiro.decode() for 종류, amakurushingiro in Mugenzi_agaciro.수신됨.items()}
                처음 = len(kubika_umurongo)
                kohereza('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_poti), timeout=5) as Mugenzi_agaciro:
                    Mugenzi_agaciro.sendall(b'A')
                    assert Mugenzi_agaciro.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Mugenzi_agaciro:
                    Mugenzi_agaciro.settimeout(5)
                    Mugenzi_agaciro.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert Mugenzi_agaciro.recvfrom(64)[0] == b'UDP-IN'
                Umwandiko = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Umwandiko and 'exit 0' in Umwandiko, Umwandiko
                raporo_agaciro['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in insomamabwiriza('terminal')
                insomamabwiriza('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(kubika_umurongo)
                kohereza('java 창예제\n'.encode())
                받기('GUI 예제 Gutegura: 창예제\r\n'.encode(), 처음)
                처음 = len(kubika_umurongo)
                kohereza(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                raporo_agaciro['suspended_java_ps'] = insomamabwiriza('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', raporo_agaciro['suspended_java_ps']), raporo_agaciro['suspended_java_ps']
                raporo_agaciro['top'] = insomamabwiriza('top -n 1')
                assert 'java 창예제' in raporo_agaciro['top'] and 'kernel/shell' in raporo_agaciro['top']
                raporo_agaciro['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                raporo_agaciro['network_trace'] = 다리.추적기록
                assert not 다리.IKOSA, 다리.IKOSA
                kohereza(b'poweroff\n')
                assert Inzira_agaciro.wait(timeout=15) == 0
                raporo_agaciro['passed'] = True
            guhitamo_igice.close()
    except Exception as IKOSA:
        raporo_agaciro['error'] = str(IKOSA)
        raise
    finally:
        if Inzira_agaciro is not None and Inzira_agaciro.poll() is None:
            Inzira_agaciro.terminate()
            try:
                Inzira_agaciro.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Inzira_agaciro.kill()
                Inzira_agaciro.wait()
        (출력 / 'serial.log').write_bytes(kubika_umurongo)
        (출력 / 'report.json').write_text(json.dumps(raporo_agaciro, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({buto_agaciro: raporo_agaciro[buto_agaciro] for buto_agaciro in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ihuriro()
