#!/usr/bin/env python3
"""QEMU의 фактик_мәгълүмат CPU рөхсәт_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from үтәргә_команда import экранга_җибәрү_тамыр, команда
from Челтәр_күпер import Челтәр_күпер
from 되돌림시험서버 import 되돌림시험서버


def эшләтү():
    출력 = экранга_җибәрү_тамыр / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    отчет_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    чыганак_Файллар = {
        'рөхсәтләр_чек': '''public class рөхсәтләр_чек {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Челтәр_чек': '''import java.net.*;
public class Челтәр_чек {
 public static void main(String[] 인수) throws Exception {
  Socket ялгау = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ялгау.setSoTimeout(3000);
  byte[] Mäten = "TCP 한글\\n".getBytes("UTF-8");
  ялгау.getOutputStream().write(Mäten);
  for (int урнаштыру_INDEX = 0; урнаштыру_INDEX < Mäten.length; урнаштыру_INDEX++)
   if (ялгау.getInputStream().read() != (Mäten[урнаштыру_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  ялгау.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Mäten = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Mäten, Mäten.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] җавап_бирү = new byte[64]; DatagramPacket 전문 = new DatagramPacket(җавап_бирү, җавап_бирү.length);
  종단.receive(전문);
  if (전문.getLength() != Mäten.length) throw new RuntimeException("UDP length");
  for (int урнаштыру_INDEX = 0; урнаштыру_INDEX < Mäten.length; урнаштыру_INDEX++)
   if (җавап_бирү[урнаштыру_INDEX] != Mäten[урнаштыру_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket сервер_VALUE = new ServerSocket(9300); сервер_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ялгау = сервер_VALUE.accept(); ялгау.setSoTimeout(5000);
  ялгау.getOutputStream().write(ялгау.getInputStream().read() + 1);
  ялгау.close(); сервер_VALUE.close();
  byte[] мәгълүмат = new byte[64]; DatagramPacket 전문 = new DatagramPacket(мәгълүмат, мәгълүмат.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for исем, чыганак in чыганак_Файллар.items():
        (출력 / (исем + '.java')).write_text(чыганак, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (исем + '.java')) for исем in чыганак_Файллар])
    LOG_юл = bytearray()
    def 빈접속번호(TYPE_категория=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_категория) as Эзләү_VALUE:
            Эзләү_VALUE.bind(('127.0.0.4', 0))
            return Эзләү_VALUE.getsockname()[1]
    파일접속번호, TCP_протоколы_порт, UDP_порт = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Процесс_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Челтәр_күпер(
                파일접속번호, ['tcp:{}:9300'.format(TCP_протоколы_порт), 'udp:{}:9301'.format(UDP_порт)],
                яздыру=True, хост_адрес='127.0.0.4') as күпер_VALUE:
            идарә_юл = Path(임시) / 'qmp.sock'
            Процесс_VALUE = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(идарә_юл)] + күпер_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_элемент = selectors.DefaultSelector()
            CHOOSE_элемент.register(Процесс_VALUE.stdout, selectors.EVENT_READ)
            def 받기(күрсәтү_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while күрсәтү_VALUE not in LOG_юл[처음:]:
                    if time.monotonic() > 끝 or Процесс_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(күрсәтү_VALUE) + '\n' + LOG_юл[처음:].decode('utf-8', 'replace'))
                    for ачкыч_VALUE, _ in CHOOSE_элемент.select(.05):
                        조각 = ачкыч_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_юл.extend(조각)
                return LOG_юл[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def җибәрү(мәгълүмат):
                Процесс_VALUE.stdin.write(мәгълүмат)
                Процесс_VALUE.stdin.flush()
            def тышча(Mäten):
                print(Mäten, flush=True)
                처음 = len(LOG_юл)
                җибәрү((Mäten + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as идарә_VALUE:
                идарә_VALUE.settimeout(10)
                идарә_VALUE.connect(str(идарә_юл))
                агым_VALUE = идарә_VALUE.makefile('rwb')
                json.loads(агым_VALUE.readline())
                def 요청(инструкция_VALUE, 인수=None):
                    мәгълүмат = {'execute': инструкция_VALUE}
                    if 인수 is not None:
                        мәгълүмат['arguments'] = 인수
                    агым_VALUE.write((json.dumps(мәгълүмат) + '\n').encode())
                    агым_VALUE.flush()
                    while True:
                        җавап_бирү = json.loads(агым_VALUE.readline())
                        if 'error' in җавап_бирү:
                            raise AssertionError(җавап_бирү)
                        if 'return' in җавап_бирү:
                            return җавап_бирү['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                отчет_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in отчет_VALUE['shell_cpu'], отчет_VALUE['shell_cpu']
                отчет_VALUE['initial_ps'] = тышча('ps')
                assert 'kernel/shell' in отчет_VALUE['initial_ps']
                отчет_VALUE['ipconfig'] = тышча('ipconfig')
                assert 'inet 10.0.2.15' in отчет_VALUE['ipconfig']
                отчет_VALUE['gateway_ping'] = тышча('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in отчет_VALUE['gateway_ping']
                assert 'FTP listening' in тышча('ftpd start')
                with ftplib.FTP() as күчерү_VALUE_630ba093:
                    күчерү_VALUE_630ba093.encoding = 'utf-8'
                    күчерү_VALUE_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    күчерү_VALUE_630ba093.login()
                    for исем in чыганак_Файллар:
                        күчерү_VALUE_630ba093.storbinary('STOR ' + исем + '.class', io.BytesIO((출력 / (исем + '.class')).read_bytes()))
                처음 = len(LOG_юл)
                җибәрү('java рөхсәтләр_чек\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    отчет_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in отчет_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in отчет_VALUE['java_cpu'], отчет_VALUE['java_cpu']
                받기(처음=처음)
                отчет_VALUE['after_exit_ps'] = тышча('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', отчет_VALUE['after_exit_ps'])
                отчет_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as тиңдәш_VALUE:
                    Mäten = тышча('java Челтәр_чек {} {}'.format(тиңдәш_VALUE.TCP_протоколы_порт, тиңдәш_VALUE.UDP_порт))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Mäten and 'exit 0' in Mäten, Mäten
                    assert тиңдәш_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, тиңдәш_VALUE.수신됨
                    assert not тиңдәш_VALUE.오류들, тиңдәш_VALUE.오류들
                    отчет_VALUE['outbound_peers'] = {종류: мәгълүмат.decode() for 종류, мәгълүмат in тиңдәш_VALUE.수신됨.items()}
                처음 = len(LOG_юл)
                җибәрү('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_протоколы_порт), timeout=5) as тиңдәш_VALUE:
                    тиңдәш_VALUE.sendall(b'A')
                    assert тиңдәш_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as тиңдәш_VALUE:
                    тиңдәш_VALUE.settimeout(5)
                    тиңдәш_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_порт))
                    assert тиңдәш_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Mäten = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Mäten and 'exit 0' in Mäten, Mäten
                отчет_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in тышча('terminal')
                тышча('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_юл)
                җибәрү('java 창예제\n'.encode())
                받기('GUI 예제 Әзерләү: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_юл)
                җибәрү(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                отчет_VALUE['suspended_java_ps'] = тышча('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', отчет_VALUE['suspended_java_ps']), отчет_VALUE['suspended_java_ps']
                отчет_VALUE['top'] = тышча('top -n 1')
                assert 'java 창예제' in отчет_VALUE['top'] and 'kernel/shell' in отчет_VALUE['top']
                отчет_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                отчет_VALUE['network_trace'] = күпер_VALUE.추적기록
                assert not күпер_VALUE.Хата, күпер_VALUE.Хата
                җибәрү(b'poweroff\n')
                assert Процесс_VALUE.wait(timeout=15) == 0
                отчет_VALUE['passed'] = True
            CHOOSE_элемент.close()
    except Exception as Хата:
        отчет_VALUE['error'] = str(Хата)
        raise
    finally:
        if Процесс_VALUE is not None and Процесс_VALUE.poll() is None:
            Процесс_VALUE.terminate()
            try:
                Процесс_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Процесс_VALUE.kill()
                Процесс_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_юл)
        (출력 / 'report.json').write_text(json.dumps(отчет_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ачкыч_VALUE: отчет_VALUE[ачкыч_VALUE] for ачкыч_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    эшләтү()
