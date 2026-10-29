#!/usr/bin/env python3
"""QEMU의 актуалдуу_берилмелер CPU уруксат_маани, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from аткаруу_буйрук import 기준, Команда
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def Жүргүзүү():
    Чыгыш = 기준 / 'build/verification/execution-network-review'
    Чыгыш.mkdir(parents=True, exist_ok=True)
    отчет_маани_ddf2aaf3 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    башат_Файлдар = {
        'уруксат_чек': '''public class уруксат_чек {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Желе_чек': '''import java.net.*;
public class Желе_чек {
 public static void main(String[] 인수) throws Exception {
  Socket Туташуу = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Туташуу.setSoTimeout(3000);
  byte[] Текст = "TCP 한글\\n".getBytes("UTF-8");
  Туташуу.getOutputStream().write(Текст);
  for (int 자리 = 0; 자리 < Текст.length; 자리++)
   if (Туташуу.getInputStream().read() != (Текст[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Туташуу.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Текст = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Текст, Текст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] жооп_берүү = new byte[64]; DatagramPacket 전문 = new DatagramPacket(жооп_берүү, жооп_берүү.length);
  종단.receive(전문);
  if (전문.getLength() != Текст.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Текст.length; 자리++)
   if (жооп_берүү[자리] != Текст[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket сервер_маани = new ServerSocket(9300); сервер_маани.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Туташуу = сервер_маани.accept(); Туташуу.setSoTimeout(5000);
  Туташуу.getOutputStream().write(Туташуу.getInputStream().read() + 1);
  Туташуу.close(); сервер_маани.close();
  byte[] берилмелер = new byte[64]; DatagramPacket 전문 = new DatagramPacket(берилмелер, берилмелер.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Аты, Булак in башат_Файлдар.items():
        (Чыгыш / (Аты + '.java')).write_text(Булак, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Чыгыш)] +
                          [str(Чыгыш / (Аты + '.java')) for Аты in башат_Файлдар])
    жазуу_катар = bytearray()
    def 빈접속번호(түрү_категория=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, түрү_категория) as Издөө_маани:
            Издөө_маани.bind(('127.0.0.4', 0))
            return Издөө_маани.getsockname()[1]
    파일접속번호, TCP_протоколу_порт, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Процесс_маани = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_протоколу_порт), 'udp:{}:9301'.format(전문접속번호)],
                тартуу_жаздыруу=True, кабылдоо_дарек='127.0.0.4') as 다리:
            башкаруу_жол = Path(임시) / 'qmp.sock'
            Процесс_маани = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(башкаруу_жол)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            тандоо_элемент = selectors.DefaultSelector()
            тандоо_элемент.register(Процесс_маани.stdout, selectors.EVENT_READ)
            def 받기(көрсөтүү_маани=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while көрсөтүү_маани not in жазуу_катар[처음:]:
                    if time.monotonic() > 끝 or Процесс_маани.poll() is not None:
                        raise AssertionError('Missing ' + repr(көрсөтүү_маани) + '\n' + жазуу_катар[처음:].decode('utf-8', 'replace'))
                    for ачкыч_маани, _ in тандоо_элемент.select(.05):
                        조각 = ачкыч_маани.fileobj.read(65536)
                        if 조각:
                            жазуу_катар.extend(조각)
                return жазуу_катар[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def жөнөтүү(берилмелер):
                Процесс_маани.stdin.write(берилмелер)
                Процесс_маани.stdin.flush()
            def сырты(Текст):
                print(Текст, flush=True)
                처음 = len(жазуу_катар)
                жөнөтүү((Текст + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as башкаруу_маани:
                башкаруу_маани.settimeout(10)
                башкаруу_маани.connect(str(башкаруу_жол))
                агым_маани = башкаруу_маани.makefile('rwb')
                json.loads(агым_маани.readline())
                def 요청(аткаруу_буйругу_маани, 인수=None):
                    берилмелер = {'execute': аткаруу_буйругу_маани}
                    if 인수 is not None:
                        берилмелер['arguments'] = 인수
                    агым_маани.write((json.dumps(берилмелер) + '\n').encode())
                    агым_маани.flush()
                    while True:
                        жооп_берүү = json.loads(агым_маани.readline())
                        if 'error' in жооп_берүү:
                            raise AssertionError(жооп_берүү)
                        if 'return' in жооп_берүү:
                            return жооп_берүү['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                отчет_маани_ddf2aaf3['shell_cpu'] = 권한읽기()
                assert 'EL1h' in отчет_маани_ddf2aaf3['shell_cpu'], отчет_маани_ddf2aaf3['shell_cpu']
                отчет_маани_ddf2aaf3['initial_ps'] = сырты('ps')
                assert 'kernel/shell' in отчет_маани_ddf2aaf3['initial_ps']
                отчет_маани_ddf2aaf3['ipconfig'] = сырты('ipconfig')
                assert 'inet 10.0.2.15' in отчет_маани_ddf2aaf3['ipconfig']
                отчет_маани_ddf2aaf3['gateway_ping'] = сырты('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in отчет_маани_ddf2aaf3['gateway_ping']
                assert 'FTP listening' in сырты('ftpd start')
                with ftplib.FTP() as ташүү_маани:
                    ташүү_маани.encoding = 'utf-8'
                    ташүү_маани.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ташүү_маани.login()
                    for Аты in башат_Файлдар:
                        ташүү_маани.storbinary('STOR ' + Аты + '.class', io.BytesIO((Чыгыш / (Аты + '.class')).read_bytes()))
                처음 = len(жазуу_катар)
                жөнөтүү('java уруксат_чек\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    отчет_маани_ddf2aaf3['java_cpu'] = 권한읽기()
                    if 'EL0t' in отчет_маани_ddf2aaf3['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in отчет_маани_ddf2aaf3['java_cpu'], отчет_маани_ddf2aaf3['java_cpu']
                받기(처음=처음)
                отчет_маани_ddf2aaf3['after_exit_ps'] = сырты('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', отчет_маани_ddf2aaf3['after_exit_ps'])
                отчет_маани_ddf2aaf3['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as бирдей_маани:
                    Текст = сырты('java Желе_чек {} {}'.format(бирдей_маани.TCP_протоколу_порт, бирдей_маани.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                    assert бирдей_маани.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, бирдей_маани.수신됨
                    assert not бирдей_маани.오류들, бирдей_маани.오류들
                    отчет_маани_ddf2aaf3['outbound_peers'] = {종류: берилмелер.decode() for 종류, берилмелер in бирдей_маани.수신됨.items()}
                처음 = len(жазуу_катар)
                жөнөтүү('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_протоколу_порт), timeout=5) as бирдей_маани:
                    бирдей_маани.sendall(b'A')
                    assert бирдей_маани.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as бирдей_маани:
                    бирдей_маани.settimeout(5)
                    бирдей_маани.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert бирдей_маани.recvfrom(64)[0] == b'UDP-IN'
                Текст = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                отчет_маани_ddf2aaf3['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in сырты('terminal')
                сырты('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(жазуу_катар)
                жөнөтүү('java 창예제\n'.encode())
                받기('GUI 예제 Даярдоо: 창예제\r\n'.encode(), 처음)
                처음 = len(жазуу_катар)
                жөнөтүү(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                отчет_маани_ddf2aaf3['suspended_java_ps'] = сырты('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', отчет_маани_ddf2aaf3['suspended_java_ps']), отчет_маани_ddf2aaf3['suspended_java_ps']
                отчет_маани_ddf2aaf3['top'] = сырты('top -n 1')
                assert 'java 창예제' in отчет_маани_ddf2aaf3['top'] and 'kernel/shell' in отчет_маани_ddf2aaf3['top']
                отчет_маани_ddf2aaf3['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                отчет_маани_ddf2aaf3['network_trace'] = 다리.추적기록
                assert not 다리.Ката, 다리.Ката
                жөнөтүү(b'poweroff\n')
                assert Процесс_маани.wait(timeout=15) == 0
                отчет_маани_ddf2aaf3['passed'] = True
            тандоо_элемент.close()
    except Exception as Ката:
        отчет_маани_ddf2aaf3['error'] = str(Ката)
        raise
    finally:
        if Процесс_маани is not None and Процесс_маани.poll() is None:
            Процесс_маани.terminate()
            try:
                Процесс_маани.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Процесс_маани.kill()
                Процесс_маани.wait()
        (Чыгыш / 'serial.log').write_bytes(жазуу_катар)
        (Чыгыш / 'report.json').write_text(json.dumps(отчет_маани_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ачкыч_маани: отчет_маани_ddf2aaf3[ачкыч_маани] for ачкыч_маани in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Жүргүзүү()
