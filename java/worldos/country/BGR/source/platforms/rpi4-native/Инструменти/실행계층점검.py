#!/usr/bin/env python3
"""QEMU의 действителен_данни CPU разрешение_стойност, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from изпълнявам_команда import проект_корен, Команда
from мост_3de4fe3a import мост_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Стартиране():
    Изход = проект_корен / 'build/verification/execution-network-review'
    Изход.mkdir(parents=True, exist_ok=True)
    отчет_стойност = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((проект_корен / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    източник_Файлове = {
        'привилегия_проверявам': '''public class привилегия_проверявам {
 public static void main(String[] Параметри) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'мрежа_проверявам': '''import java.net.*;
public class мрежа_проверявам {
 public static void main(String[] Параметри) throws Exception {
  Socket Свързване = new Socket("10.0.2.2", Integer.parseInt(Параметри[0]));
  Свързване.setSoTimeout(3000);
  byte[] Текст = "TCP 한글\\n".getBytes("UTF-8");
  Свързване.getOutputStream().write(Текст);
  for (int позиционен_указател = 0; позиционен_указател < Текст.length; позиционен_указател++)
   if (Свързване.getInputStream().read() != (Текст[позиционен_указател] & 255)) throw new RuntimeException("TCP mismatch");
  Свързване.close();
  DatagramSocket участник = new DatagramSocket(); участник.setSoTimeout(3000);
  Текст = "UDP 한글".getBytes("UTF-8");
  участник.send(new DatagramPacket(Текст, Текст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Параметри[1])));
  byte[] отговор = new byte[64]; DatagramPacket дейтаграма = new DatagramPacket(отговор, отговор.length);
  участник.receive(дейтаграма);
  if (дейтаграма.getLength() != Текст.length) throw new RuntimeException("UDP length");
  for (int позиционен_указател = 0; позиционен_указател < Текст.length; позиционен_указател++)
   if (отговор[позиционен_указател] != Текст[позиционен_указател]) throw new RuntimeException("UDP mismatch");
  участник.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'получавам_проверявам': '''import java.net.*;
public class получавам_проверявам {
 public static void main(String[] Параметри) throws Exception {
  ServerSocket сървър_стойност = new ServerSocket(9300); сървър_стойност.setSoTimeout(5000);
  DatagramSocket участник = new DatagramSocket(9301); участник.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Свързване = сървър_стойност.accept(); Свързване.setSoTimeout(5000);
  Свързване.getOutputStream().write(Свързване.getInputStream().read() + 1);
  Свързване.close(); сървър_стойност.close();
  byte[] данни = new byte[64]; DatagramPacket дейтаграма = new DatagramPacket(данни, данни.length);
  участник.receive(дейтаграма); участник.send(дейтаграма); участник.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Име, ИЗТОЧНИК in източник_Файлове.items():
        (Изход / (Име + '.java')).write_text(ИЗТОЧНИК, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Изход)] +
                          [str(Изход / (Име + '.java')) for Име in източник_Файлове])
    регистрирам_запис = bytearray()
    def 빈접속번호(Тип_област=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Тип_област) as търся_стойност:
            търся_стойност.bind(('127.0.0.4', 0))
            return търся_стойност.getsockname()[1]
    Файл_номер_на_порт, 연결접속번호, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Процес_стойност = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, мост_3de4fe3a(
                Файл_номер_на_порт, ['tcp:{}:9300'.format(연결접속번호), 'udp:{}:9301'.format(전문접속번호)],
                заснемам=True, хост_адрес='127.0.0.4') as мост_стойност:
            контрол_път = Path(임시) / 'qmp.sock'
            Процес_стойност = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(контрол_път)] + мост_стойност.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            избирам_артикул = selectors.DefaultSelector()
            избирам_артикул.register(Процес_стойност.stdout, selectors.EVENT_READ)
            def получавам(показвам_стойност=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while показвам_стойност not in регистрирам_запис[처음:]:
                    if time.monotonic() > 끝 or Процес_стойност.poll() is not None:
                        raise AssertionError('Missing ' + repr(показвам_стойност) + '\n' + регистрирам_запис[처음:].decode('utf-8', 'replace'))
                    for Ключ_стойност, _ in избирам_артикул.select(.05):
                        조각 = Ключ_стойност.fileobj.read(65536)
                        if 조각:
                            регистрирам_запис.extend(조각)
                return регистрирам_запис[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def изпращам(данни):
                Процес_стойност.stdin.write(данни)
                Процес_стойност.stdin.flush()
            def обвивка(Текст):
                print(Текст, flush=True)
                처음 = len(регистрирам_запис)
                изпращам((Текст + '\n').encode())
                return получавам(처음=처음)
            получавам()
            with socket.socket(socket.AF_UNIX) as контрол_стойност:
                контрол_стойност.settimeout(10)
                контрол_стойност.connect(str(контрол_път))
                поток_стойност = контрол_стойност.makefile('rwb')
                json.loads(поток_стойност.readline())
                def искане(명령어, Параметри=None):
                    данни = {'execute': 명령어}
                    if Параметри is not None:
                        данни['arguments'] = Параметри
                    поток_стойност.write((json.dumps(данни) + '\n').encode())
                    поток_стойност.flush()
                    while True:
                        отговор = json.loads(поток_стойност.readline())
                        if 'error' in отговор:
                            raise AssertionError(отговор)
                        if 'return' in отговор:
                            return отговор['return']
                искане('qmp_capabilities')
                def 권한읽기():
                    искане('stop')
                    try:
                        return искане('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        искане('cont')
                отчет_стойност['shell_cpu'] = 권한읽기()
                assert 'EL1h' in отчет_стойност['shell_cpu'], отчет_стойност['shell_cpu']
                отчет_стойност['initial_ps'] = обвивка('ps')
                assert 'kernel/shell' in отчет_стойност['initial_ps']
                отчет_стойност['ipconfig'] = обвивка('ipconfig')
                assert 'inet 10.0.2.15' in отчет_стойност['ipconfig']
                отчет_стойност['gateway_ping'] = обвивка('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in отчет_стойност['gateway_ping']
                assert 'FTP listening' in обвивка('ftpd start')
                with ftplib.FTP() as прехвърлям_стойност:
                    прехвърлям_стойност.encoding = 'utf-8'
                    прехвърлям_стойност.connect('127.0.0.4', Файл_номер_на_порт, timeout=20)
                    прехвърлям_стойност.login()
                    for Име in източник_Файлове:
                        прехвърлям_стойност.storbinary('STOR ' + Име + '.class', io.BytesIO((Изход / (Име + '.class')).read_bytes()))
                처음 = len(регистрирам_запис)
                изпращам('java привилегия_проверявам\n'.encode())
                получавам(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    отчет_стойност['java_cpu'] = 권한읽기()
                    if 'EL0t' in отчет_стойност['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in отчет_стойност['java_cpu'], отчет_стойност['java_cpu']
                получавам(처음=처음)
                отчет_стойност['after_exit_ps'] = обвивка('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', отчет_стойност['after_exit_ps'])
                отчет_стойност['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as крайно_устройство_стойност:
                    Текст = обвивка('java мрежа_проверявам {} {}'.format(крайно_устройство_стойност.연결접속번호, крайно_устройство_стойност.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                    assert крайно_устройство_стойност.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, крайно_устройство_стойност.수신됨
                    assert not крайно_устройство_стойност.오류들, крайно_устройство_стойност.오류들
                    отчет_стойност['outbound_peers'] = {종류: данни.decode() for 종류, данни in крайно_устройство_стойност.수신됨.items()}
                처음 = len(регистрирам_запис)
                изпращам('java получавам_проверявам\n'.encode())
                получавам(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', 연결접속번호), timeout=5) as крайно_устройство_стойност:
                    крайно_устройство_стойност.sendall(b'A')
                    assert крайно_устройство_стойност.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as крайно_устройство_стойност:
                    крайно_устройство_стойност.settimeout(5)
                    крайно_устройство_стойност.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert крайно_устройство_стойност.recvfrom(64)[0] == b'UDP-IN'
                Текст = получавам(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                отчет_стойност['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in обвивка('terminal')
                обвивка('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(регистрирам_запис)
                изпращам('java 창예제\n'.encode())
                получавам('GUI 예제 Подготвяне: 창예제\r\n'.encode(), 처음)
                처음 = len(регистрирам_запис)
                изпращам(bytes([30, 2, 1, 0, 0, 0, 0]))
                получавам(처음=처음)
                отчет_стойност['suspended_java_ps'] = обвивка('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', отчет_стойност['suspended_java_ps']), отчет_стойност['suspended_java_ps']
                отчет_стойност['top'] = обвивка('top -n 1')
                assert 'java 창예제' in отчет_стойност['top'] and 'kernel/shell' in отчет_стойност['top']
                отчет_стойност['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                отчет_стойност['network_trace'] = мост_стойност.регистрационен_файл_за_проследяванията
                assert not мост_стойност.ГРЕШКА, мост_стойност.ГРЕШКА
                изпращам(b'poweroff\n')
                assert Процес_стойност.wait(timeout=15) == 0
                отчет_стойност['passed'] = True
            избирам_артикул.close()
    except Exception as ГРЕШКА:
        отчет_стойност['error'] = str(ГРЕШКА)
        raise
    finally:
        if Процес_стойност is not None and Процес_стойност.poll() is None:
            Процес_стойност.terminate()
            try:
                Процес_стойност.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Процес_стойност.kill()
                Процес_стойност.wait()
        (Изход / 'serial.log').write_bytes(регистрирам_запис)
        (Изход / 'report.json').write_text(json.dumps(отчет_стойност, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Ключ_стойност: отчет_стойност[Ключ_стойност] for Ключ_стойност in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Стартиране()
