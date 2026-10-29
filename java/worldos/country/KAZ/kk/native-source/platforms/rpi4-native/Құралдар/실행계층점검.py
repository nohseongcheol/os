#!/usr/bin/env python3
"""QEMU의 нақты_деректер CPU рұқсат_мән, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from орындау_пәрмен import жоба_түбір, Команда
from желі_көпір import желі_көпір
from 되돌림시험서버 import 되돌림시험서버


def Орындау_2():
    Шығысы = жоба_түбір / 'build/verification/execution-network-review'
    Шығысы.mkdir(parents=True, exist_ok=True)
    есеп_мән = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((жоба_түбір / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    көз_Файлдар = {
        'рұқсат_чек': '''public class рұқсат_чек {
 public static void main(String[] Аргументтер) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'желі_чек': '''import java.net.*;
public class желі_чек {
 public static void main(String[] Аргументтер) throws Exception {
  Socket Байланысу = new Socket("10.0.2.2", Integer.parseInt(Аргументтер[0]));
  Байланысу.setSoTimeout(3000);
  byte[] Мәтін = "TCP 한글\\n".getBytes("UTF-8");
  Байланысу.getOutputStream().write(Мәтін);
  for (int лауазым_индекс = 0; лауазым_индекс < Мәтін.length; лауазым_индекс++)
   if (Байланысу.getInputStream().read() != (Мәтін[лауазым_индекс] & 255)) throw new RuntimeException("TCP mismatch");
  Байланысу.close();
  DatagramSocket қатысушы = new DatagramSocket(); қатысушы.setSoTimeout(3000);
  Мәтін = "UDP 한글".getBytes("UTF-8");
  қатысушы.send(new DatagramPacket(Мәтін, Мәтін.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Аргументтер[1])));
  byte[] жауап = new byte[64]; DatagramPacket 전문 = new DatagramPacket(жауап, жауап.length);
  қатысушы.receive(전문);
  if (전문.getLength() != Мәтін.length) throw new RuntimeException("UDP length");
  for (int лауазым_индекс = 0; лауазым_индекс < Мәтін.length; лауазым_индекс++)
   if (жауап[лауазым_индекс] != Мәтін[лауазым_индекс]) throw new RuntimeException("UDP mismatch");
  қатысушы.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Аргументтер) throws Exception {
  ServerSocket сервер_мән = new ServerSocket(9300); сервер_мән.setSoTimeout(5000);
  DatagramSocket қатысушы = new DatagramSocket(9301); қатысушы.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Байланысу = сервер_мән.accept(); Байланысу.setSoTimeout(5000);
  Байланысу.getOutputStream().write(Байланысу.getInputStream().read() + 1);
  Байланысу.close(); сервер_мән.close();
  byte[] деректер = new byte[64]; DatagramPacket 전문 = new DatagramPacket(деректер, деректер.length);
  қатысушы.receive(전문); қатысушы.send(전문); қатысушы.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Аты, Неден in көз_Файлдар.items():
        (Шығысы / (Аты + '.java')).write_text(Неден, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Шығысы)] +
                          [str(Шығысы / (Аты + '.java')) for Аты in көз_Файлдар])
    журнал_жол = bytearray()
    def 빈접속번호(Түрі_Санат=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Түрі_Санат) as Іздеу_мән:
            Іздеу_мән.bind(('127.0.0.4', 0))
            return Іздеу_мән.getsockname()[1]
    файл_порт_нөмірі, TCP_протоколы_порт, пайдаланушы_датаграммасының_протоколы_порт = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Процесс_мән = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, желі_көпір(
                файл_порт_нөмірі, ['tcp:{}:9300'.format(TCP_протоколы_порт), 'udp:{}:9301'.format(пайдаланушы_датаграммасының_протоколы_порт)],
                түсіру=True, орналастыру_мекенжай='127.0.0.4') as көпір_мән:
            Басқару_жол = Path(임시) / 'qmp.sock'
            Процесс_мән = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(Басқару_жол)] + көпір_мән.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            таңдау_элемент = selectors.DefaultSelector()
            таңдау_элемент.register(Процесс_мән.stdout, selectors.EVENT_READ)
            def 받기(көрсету_мән=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while көрсету_мән not in журнал_жол[처음:]:
                    if time.monotonic() > 끝 or Процесс_мән.poll() is not None:
                        raise AssertionError('Missing ' + repr(көрсету_мән) + '\n' + журнал_жол[처음:].decode('utf-8', 'replace'))
                    for Кілт_мән, _ in таңдау_элемент.select(.05):
                        조각 = Кілт_мән.fileobj.read(65536)
                        if 조각:
                            журнал_жол.extend(조각)
                return журнал_жол[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def жіберу(деректер):
                Процесс_мән.stdin.write(деректер)
                Процесс_мән.stdin.flush()
            def қоршам(Мәтін):
                print(Мәтін, flush=True)
                처음 = len(журнал_жол)
                жіберу((Мәтін + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as Басқару_мән:
                Басқару_мән.settimeout(10)
                Басқару_мән.connect(str(Басқару_жол))
                ағым_мән = Басқару_мән.makefile('rwb')
                json.loads(ағым_мән.readline())
                def 요청(нұсқау_мән_4c26ea1b, Аргументтер=None):
                    деректер = {'execute': нұсқау_мән_4c26ea1b}
                    if Аргументтер is not None:
                        деректер['arguments'] = Аргументтер
                    ағым_мән.write((json.dumps(деректер) + '\n').encode())
                    ағым_мән.flush()
                    while True:
                        жауап = json.loads(ағым_мән.readline())
                        if 'error' in жауап:
                            raise AssertionError(жауап)
                        if 'return' in жауап:
                            return жауап['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                есеп_мән['shell_cpu'] = 권한읽기()
                assert 'EL1h' in есеп_мән['shell_cpu'], есеп_мән['shell_cpu']
                есеп_мән['initial_ps'] = қоршам('ps')
                assert 'kernel/shell' in есеп_мән['initial_ps']
                есеп_мән['ipconfig'] = қоршам('ipconfig')
                assert 'inet 10.0.2.15' in есеп_мән['ipconfig']
                есеп_мән['gateway_ping'] = қоршам('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in есеп_мән['gateway_ping']
                assert 'FTP listening' in қоршам('ftpd start')
                with ftplib.FTP() as аудару_мән:
                    аудару_мән.encoding = 'utf-8'
                    аудару_мән.connect('127.0.0.4', файл_порт_нөмірі, timeout=20)
                    аудару_мән.login()
                    for Аты in көз_Файлдар:
                        аудару_мән.storbinary('STOR ' + Аты + '.class', io.BytesIO((Шығысы / (Аты + '.class')).read_bytes()))
                처음 = len(журнал_жол)
                жіберу('java рұқсат_чек\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    есеп_мән['java_cpu'] = 권한읽기()
                    if 'EL0t' in есеп_мән['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in есеп_мән['java_cpu'], есеп_мән['java_cpu']
                받기(처음=처음)
                есеп_мән['after_exit_ps'] = қоршам('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', есеп_мән['after_exit_ps'])
                есеп_мән['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as бір_рангілі_мән:
                    Мәтін = қоршам('java желі_чек {} {}'.format(бір_рангілі_мән.TCP_протоколы_порт, бір_рангілі_мән.пайдаланушы_датаграммасының_протоколы_порт))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Мәтін and 'exit 0' in Мәтін, Мәтін
                    assert бір_рангілі_мән.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, бір_рангілі_мән.수신됨
                    assert not бір_рангілі_мән.오류들, бір_рангілі_мән.오류들
                    есеп_мән['outbound_peers'] = {종류: деректер.decode() for 종류, деректер in бір_рангілі_мән.수신됨.items()}
                처음 = len(журнал_жол)
                жіберу('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_протоколы_порт), timeout=5) as бір_рангілі_мән:
                    бір_рангілі_мән.sendall(b'A')
                    assert бір_рангілі_мән.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as бір_рангілі_мән:
                    бір_рангілі_мән.settimeout(5)
                    бір_рангілі_мән.sendto(b'UDP-IN', ('127.0.0.4', пайдаланушы_датаграммасының_протоколы_порт))
                    assert бір_рангілі_мән.recvfrom(64)[0] == b'UDP-IN'
                Мәтін = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Мәтін and 'exit 0' in Мәтін, Мәтін
                есеп_мән['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in қоршам('terminal')
                қоршам('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(журнал_жол)
                жіберу('java 창예제\n'.encode())
                받기('GUI 예제 Дайындау: 창예제\r\n'.encode(), 처음)
                처음 = len(журнал_жол)
                жіберу(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                есеп_мән['suspended_java_ps'] = қоршам('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', есеп_мән['suspended_java_ps']), есеп_мән['suspended_java_ps']
                есеп_мән['top'] = қоршам('top -n 1')
                assert 'java 창예제' in есеп_мән['top'] and 'kernel/shell' in есеп_мән['top']
                есеп_мән['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                есеп_мән['network_trace'] = көпір_мән.трассалау_журналы
                assert not көпір_мән.Қате, көпір_мән.Қате
                жіберу(b'poweroff\n')
                assert Процесс_мән.wait(timeout=15) == 0
                есеп_мән['passed'] = True
            таңдау_элемент.close()
    except Exception as Қате:
        есеп_мән['error'] = str(Қате)
        raise
    finally:
        if Процесс_мән is not None and Процесс_мән.poll() is None:
            Процесс_мән.terminate()
            try:
                Процесс_мән.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Процесс_мән.kill()
                Процесс_мән.wait()
        (Шығысы / 'serial.log').write_bytes(журнал_жол)
        (Шығысы / 'report.json').write_text(json.dumps(есеп_мән, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Кілт_мән: есеп_мән[Кілт_мән] for Кілт_мән in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Орындау_2()
