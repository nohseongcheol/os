#!/usr/bin/env python3
"""QEMU의 воқеӣ_иттилоот CPU иҷозат_қимат, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from иҷро_кардан_фармон import 기준, фармон
from Шабака_кӯпрук import Шабака_кӯпрук
from 되돌림시험서버 import 되돌림시험서버


def порча():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    гузориш_қимат = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    манбаъ_Файлҳо = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Шабака_санҷиш': '''import java.net.*;
public class Шабака_санҷиш {
 public static void main(String[] 인수) throws Exception {
  Socket ПАЙВАСТ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ПАЙВАСТ.setSoTimeout(3000);
  byte[] Матн = "TCP 한글\\n".getBytes("UTF-8");
  ПАЙВАСТ.getOutputStream().write(Матн);
  for (int 자리 = 0; 자리 < Матн.length; 자리++)
   if (ПАЙВАСТ.getInputStream().read() != (Матн[자리] & 255)) throw new RuntimeException("TCP mismatch");
  ПАЙВАСТ.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Матн = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Матн, Матн.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] ҷавоб_додан = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ҷавоб_додан, ҷавоб_додан.length);
  종단.receive(전문);
  if (전문.getLength() != Матн.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Матн.length; 자리++)
   if (ҷавоб_додан[자리] != Матн[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket сервер_қимат = new ServerSocket(9300); сервер_қимат.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ПАЙВАСТ = сервер_қимат.accept(); ПАЙВАСТ.setSoTimeout(5000);
  ПАЙВАСТ.getOutputStream().write(ПАЙВАСТ.getInputStream().read() + 1);
  ПАЙВАСТ.close(); сервер_қимат.close();
  byte[] иттилоот = new byte[64]; DatagramPacket 전문 = new DatagramPacket(иттилоот, иттилоот.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ном, манбаъ in манбаъ_Файлҳо.items():
        (출력 / (Ном + '.java')).write_text(манбаъ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Ном + '.java')) for Ном in манбаъ_Файлҳо])
    сабт_кардан_сабт = bytearray()
    def 빈접속번호(навъ_категория=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, навъ_категория) as ҷустан_қимат:
            ҷустан_қимат.bind(('127.0.0.4', 0))
            return ҷустан_қимат.getsockname()[1]
    파일접속번호, Протоколи_TCP_порт, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Раванд_қимат = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Шабака_кӯпрук(
                파일접속번호, ['tcp:{}:9300'.format(Протоколи_TCP_порт), 'udp:{}:9301'.format(전문접속번호)],
                акс_гирифтан=True, мизбон_суроға='127.0.0.4') as кӯпрук_қимат:
            идоракунӣ_масир = Path(임시) / 'qmp.sock'
            Раванд_қимат = subprocess.Popen(фармон() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(идоракунӣ_масир)] + кӯпрук_қимат.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            интихоб_кардан_объект = selectors.DefaultSelector()
            интихоб_кардан_объект.register(Раванд_қимат.stdout, selectors.EVENT_READ)
            def 받기(намоиш_додан_қимат=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while намоиш_додан_қимат not in сабт_кардан_сабт[처음:]:
                    if time.monotonic() > 끝 or Раванд_қимат.poll() is not None:
                        raise AssertionError('Missing ' + repr(намоиш_додан_қимат) + '\n' + сабт_кардан_сабт[처음:].decode('utf-8', 'replace'))
                    for калид_қимат, _ in интихоб_кардан_объект.select(.05):
                        조각 = калид_қимат.fileobj.read(65536)
                        if 조각:
                            сабт_кардан_сабт.extend(조각)
                return сабт_кардан_сабт[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def фиристодан(иттилоот):
                Раванд_қимат.stdin.write(иттилоот)
                Раванд_қимат.stdin.flush()
            def восит(Матн):
                print(Матн, flush=True)
                처음 = len(сабт_кардан_сабт)
                фиристодан((Матн + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as идоракунӣ_қимат:
                идоракунӣ_қимат.settimeout(10)
                идоракунӣ_қимат.connect(str(идоракунӣ_масир))
                ҷараён_қимат = идоракунӣ_қимат.makefile('rwb')
                json.loads(ҷараён_қимат.readline())
                def 요청(дастур_қимат, 인수=None):
                    иттилоот = {'execute': дастур_қимат}
                    if 인수 is not None:
                        иттилоот['arguments'] = 인수
                    ҷараён_қимат.write((json.dumps(иттилоот) + '\n').encode())
                    ҷараён_қимат.flush()
                    while True:
                        ҷавоб_додан = json.loads(ҷараён_қимат.readline())
                        if 'error' in ҷавоб_додан:
                            raise AssertionError(ҷавоб_додан)
                        if 'return' in ҷавоб_додан:
                            return ҷавоб_додан['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                гузориш_қимат['shell_cpu'] = 권한읽기()
                assert 'EL1h' in гузориш_қимат['shell_cpu'], гузориш_қимат['shell_cpu']
                гузориш_қимат['initial_ps'] = восит('ps')
                assert 'kernel/shell' in гузориш_қимат['initial_ps']
                гузориш_қимат['ipconfig'] = восит('ipconfig')
                assert 'inet 10.0.2.15' in гузориш_қимат['ipconfig']
                гузориш_қимат['gateway_ping'] = восит('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in гузориш_қимат['gateway_ping']
                assert 'FTP listening' in восит('ftpd start')
                with ftplib.FTP() as интиқол_қимат:
                    интиқол_қимат.encoding = 'utf-8'
                    интиқол_қимат.connect('127.0.0.4', 파일접속번호, timeout=20)
                    интиқол_қимат.login()
                    for Ном in манбаъ_Файлҳо:
                        интиқол_қимат.storbinary('STOR ' + Ном + '.class', io.BytesIO((출력 / (Ном + '.class')).read_bytes()))
                처음 = len(сабт_кардан_сабт)
                фиристодан('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    гузориш_қимат['java_cpu'] = 권한읽기()
                    if 'EL0t' in гузориш_қимат['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in гузориш_қимат['java_cpu'], гузориш_қимат['java_cpu']
                받기(처음=처음)
                гузориш_қимат['after_exit_ps'] = восит('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', гузориш_қимат['after_exit_ps'])
                гузориш_қимат['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ҳамсон_қимат:
                    Матн = восит('java Шабака_санҷиш {} {}'.format(ҳамсон_қимат.Протоколи_TCP_порт, ҳамсон_қимат.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Матн and 'exit 0' in Матн, Матн
                    assert ҳамсон_қимат.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ҳамсон_қимат.수신됨
                    assert not ҳамсон_қимат.오류들, ҳамсон_қимат.오류들
                    гузориш_қимат['outbound_peers'] = {종류: иттилоот.decode() for 종류, иттилоот in ҳамсон_қимат.수신됨.items()}
                처음 = len(сабт_кардан_сабт)
                фиристодан('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', Протоколи_TCP_порт), timeout=5) as ҳамсон_қимат:
                    ҳамсон_қимат.sendall(b'A')
                    assert ҳамсон_қимат.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ҳамсон_қимат:
                    ҳамсон_қимат.settimeout(5)
                    ҳамсон_қимат.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ҳамсон_қимат.recvfrom(64)[0] == b'UDP-IN'
                Матн = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Матн and 'exit 0' in Матн, Матн
                гузориш_қимат['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in восит('terminal')
                восит('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(сабт_кардан_сабт)
                фиристодан('java 창예제\n'.encode())
                받기('GUI 예제 Омода_кардан: 창예제\r\n'.encode(), 처음)
                처음 = len(сабт_кардан_сабт)
                фиристодан(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                гузориш_қимат['suspended_java_ps'] = восит('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', гузориш_қимат['suspended_java_ps']), гузориш_қимат['suspended_java_ps']
                гузориш_қимат['top'] = восит('top -n 1')
                assert 'java 창예제' in гузориш_қимат['top'] and 'kernel/shell' in гузориш_қимат['top']
                гузориш_қимат['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                гузориш_қимат['network_trace'] = кӯпрук_қимат.추적기록
                assert not кӯпрук_қимат.Хато, кӯпрук_қимат.Хато
                фиристодан(b'poweroff\n')
                assert Раванд_қимат.wait(timeout=15) == 0
                гузориш_қимат['passed'] = True
            интихоб_кардан_объект.close()
    except Exception as Хато:
        гузориш_қимат['error'] = str(Хато)
        raise
    finally:
        if Раванд_қимат is not None and Раванд_қимат.poll() is None:
            Раванд_қимат.terminate()
            try:
                Раванд_қимат.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Раванд_қимат.kill()
                Раванд_қимат.wait()
        (출력 / 'serial.log').write_bytes(сабт_кардан_сабт)
        (출력 / 'report.json').write_text(json.dumps(гузориш_қимат, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({калид_қимат: гузориш_қимат[калид_қимат] for калид_қимат in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    порча()
