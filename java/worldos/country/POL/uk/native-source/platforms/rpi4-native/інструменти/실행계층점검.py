#!/usr/bin/env python3
"""QEMU의 фактично_дані CPU дозвіл_значення, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Виконати_команда import Дії_корінь, команда
from міст_3de4fe3a import міст_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def запустити():
    Вивід = Дії_корінь / 'build/verification/execution-network-review'
    Вивід.mkdir(parents=True, exist_ok=True)
    звіт_значення = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Дії_корінь / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    джерело_Файли = {
        'право_перевіряти': '''public class право_перевіряти {
 public static void main(String[] аргументи) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'мережа_перевіряти': '''import java.net.*;
public class мережа_перевіряти {
 public static void main(String[] аргументи) throws Exception {
  Socket З_єднання = new Socket("10.0.2.2", Integer.parseInt(аргументи[0]));
  З_єднання.setSoTimeout(3000);
  byte[] текст = "TCP 한글\\n".getBytes("UTF-8");
  З_єднання.getOutputStream().write(текст);
  for (int індекс_розташування = 0; індекс_розташування < текст.length; індекс_розташування++)
   if (З_єднання.getInputStream().read() != (текст[індекс_розташування] & 255)) throw new RuntimeException("TCP mismatch");
  З_єднання.close();
  DatagramSocket учасник = new DatagramSocket(); учасник.setSoTimeout(3000);
  текст = "UDP 한글".getBytes("UTF-8");
  учасник.send(new DatagramPacket(текст, текст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(аргументи[1])));
  byte[] відповідь = new byte[64]; DatagramPacket дейтаграма = new DatagramPacket(відповідь, відповідь.length);
  учасник.receive(дейтаграма);
  if (дейтаграма.getLength() != текст.length) throw new RuntimeException("UDP length");
  for (int індекс_розташування = 0; індекс_розташування < текст.length; індекс_розташування++)
   if (відповідь[індекс_розташування] != текст[індекс_розташування]) throw new RuntimeException("UDP mismatch");
  учасник.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'отримувати_перевіряти': '''import java.net.*;
public class отримувати_перевіряти {
 public static void main(String[] аргументи) throws Exception {
  ServerSocket сервер_значення = new ServerSocket(9300); сервер_значення.setSoTimeout(5000);
  DatagramSocket учасник = new DatagramSocket(9301); учасник.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket З_єднання = сервер_значення.accept(); З_єднання.setSoTimeout(5000);
  З_єднання.getOutputStream().write(З_єднання.getInputStream().read() + 1);
  З_єднання.close(); сервер_значення.close();
  byte[] дані = new byte[64]; DatagramPacket дейтаграма = new DatagramPacket(дані, дані.length);
  учасник.receive(дейтаграма); учасник.send(дейтаграма); учасник.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Назва, вихіднийКод in джерело_Файли.items():
        (Вивід / (Назва + '.java')).write_text(вихіднийКод, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Вивід)] +
                          [str(Вивід / (Назва + '.java')) for Назва in джерело_Файли])
    журнал_запис = bytearray()
    def 빈접속번호(Тип_область=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Тип_область) as Пошук_значення:
            Пошук_значення.bind(('127.0.0.4', 0))
            return Пошук_значення.getsockname()[1]
    Файл_номер_порту, протокол_керування_передаванням_порт, протокол_користувацьких_дейтаграм_порт = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    процес_значення = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, міст_3de4fe3a(
                Файл_номер_порту, ['tcp:{}:9300'.format(протокол_керування_передаванням_порт), 'udp:{}:9301'.format(протокол_користувацьких_дейтаграм_порт)],
                записувати=True, хост_адреса='127.0.0.4') as міст_значення:
            керування_шлях = Path(임시) / 'qmp.sock'
            процес_значення = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(керування_шлях)] + міст_значення.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            вибирати_елемент = selectors.DefaultSelector()
            вибирати_елемент.register(процес_значення.stdout, selectors.EVENT_READ)
            def отримувати(показувати_значення=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while показувати_значення not in журнал_запис[처음:]:
                    if time.monotonic() > 끝 or процес_значення.poll() is not None:
                        raise AssertionError('Missing ' + repr(показувати_значення) + '\n' + журнал_запис[처음:].decode('utf-8', 'replace'))
                    for Ключ_значення, _ in вибирати_елемент.select(.05):
                        조각 = Ключ_значення.fileobj.read(65536)
                        if 조각:
                            журнал_запис.extend(조각)
                return журнал_запис[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def надсилати(дані):
                процес_значення.stdin.write(дані)
                процес_значення.stdin.flush()
            def оболонка(текст):
                print(текст, flush=True)
                처음 = len(журнал_запис)
                надсилати((текст + '\n').encode())
                return отримувати(처음=처음)
            отримувати()
            with socket.socket(socket.AF_UNIX) as керування_значення:
                керування_значення.settimeout(10)
                керування_значення.connect(str(керування_шлях))
                потік_значення = керування_значення.makefile('rwb')
                json.loads(потік_значення.readline())
                def запит(명령어, аргументи=None):
                    дані = {'execute': 명령어}
                    if аргументи is not None:
                        дані['arguments'] = аргументи
                    потік_значення.write((json.dumps(дані) + '\n').encode())
                    потік_значення.flush()
                    while True:
                        відповідь = json.loads(потік_значення.readline())
                        if 'error' in відповідь:
                            raise AssertionError(відповідь)
                        if 'return' in відповідь:
                            return відповідь['return']
                запит('qmp_capabilities')
                def 권한읽기():
                    запит('stop')
                    try:
                        return запит('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        запит('cont')
                звіт_значення['shell_cpu'] = 권한읽기()
                assert 'EL1h' in звіт_значення['shell_cpu'], звіт_значення['shell_cpu']
                звіт_значення['initial_ps'] = оболонка('ps')
                assert 'kernel/shell' in звіт_значення['initial_ps']
                звіт_значення['ipconfig'] = оболонка('ipconfig')
                assert 'inet 10.0.2.15' in звіт_значення['ipconfig']
                звіт_значення['gateway_ping'] = оболонка('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in звіт_значення['gateway_ping']
                assert 'FTP listening' in оболонка('ftpd start')
                with ftplib.FTP() as передача_значення:
                    передача_значення.encoding = 'utf-8'
                    передача_значення.connect('127.0.0.4', Файл_номер_порту, timeout=20)
                    передача_значення.login()
                    for Назва in джерело_Файли:
                        передача_значення.storbinary('STOR ' + Назва + '.class', io.BytesIO((Вивід / (Назва + '.class')).read_bytes()))
                처음 = len(журнал_запис)
                надсилати('java право_перевіряти\n'.encode())
                отримувати(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    звіт_значення['java_cpu'] = 권한읽기()
                    if 'EL0t' in звіт_значення['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in звіт_значення['java_cpu'], звіт_значення['java_cpu']
                отримувати(처음=처음)
                звіт_значення['after_exit_ps'] = оболонка('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', звіт_значення['after_exit_ps'])
                звіт_значення['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as точка_значення:
                    текст = оболонка('java мережа_перевіряти {} {}'.format(точка_значення.протокол_керування_передаванням_порт, точка_значення.протокол_користувацьких_дейтаграм_порт))
                    assert 'OUTBOUND_TCP_UDP_PASS' in текст and 'exit 0' in текст, текст
                    assert точка_значення.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, точка_значення.수신됨
                    assert not точка_значення.오류들, точка_значення.오류들
                    звіт_значення['outbound_peers'] = {종류: дані.decode() for 종류, дані in точка_значення.수신됨.items()}
                처음 = len(журнал_запис)
                надсилати('java отримувати_перевіряти\n'.encode())
                отримувати(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', протокол_керування_передаванням_порт), timeout=5) as точка_значення:
                    точка_значення.sendall(b'A')
                    assert точка_значення.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as точка_значення:
                    точка_значення.settimeout(5)
                    точка_значення.sendto(b'UDP-IN', ('127.0.0.4', протокол_користувацьких_дейтаграм_порт))
                    assert точка_значення.recvfrom(64)[0] == b'UDP-IN'
                текст = отримувати(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in текст and 'exit 0' in текст, текст
                звіт_значення['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in оболонка('terminal')
                оболонка('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(журнал_запис)
                надсилати('java ПрикладВікна\n'.encode())
                отримувати('GUI 예제 Готувати: ПрикладВікна\r\n'.encode(), 처음)
                처음 = len(журнал_запис)
                надсилати(bytes([30, 2, 1, 0, 0, 0, 0]))
                отримувати(처음=처음)
                звіт_значення['suspended_java_ps'] = оболонка('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ПрикладВікна', звіт_значення['suspended_java_ps']), звіт_значення['suspended_java_ps']
                звіт_значення['top'] = оболонка('top -n 1')
                assert 'java ПрикладВікна' in звіт_значення['top'] and 'kernel/shell' in звіт_значення['top']
                звіт_значення['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                звіт_значення['network_trace'] = міст_значення.журнал_трасування
                assert not міст_значення.ПОМИЛКА, міст_значення.ПОМИЛКА
                надсилати(b'poweroff\n')
                assert процес_значення.wait(timeout=15) == 0
                звіт_значення['passed'] = True
            вибирати_елемент.close()
    except Exception as ПОМИЛКА:
        звіт_значення['error'] = str(ПОМИЛКА)
        raise
    finally:
        if процес_значення is not None and процес_значення.poll() is None:
            процес_значення.terminate()
            try:
                процес_значення.wait(timeout=10)
            except subprocess.TimeoutExpired:
                процес_значення.kill()
                процес_значення.wait()
        (Вивід / 'serial.log').write_bytes(журнал_запис)
        (Вивід / 'report.json').write_text(json.dumps(звіт_значення, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Ключ_значення: звіт_значення[Ключ_значення] for Ключ_значення in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    запустити()
