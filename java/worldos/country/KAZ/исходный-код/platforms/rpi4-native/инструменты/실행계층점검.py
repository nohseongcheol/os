#!/usr/bin/env python3
"""QEMU의 фактический_данные CPU Полномочие_ЗНАЧЕН, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from 실행 import задача_корень, команда
from мост_3de4fe3a import мост_3de4fe3a
from вывод_на_экран_средство import вывод_на_экран_средство


def запустить():
    текстовыйВывод = задача_корень / 'build/verification/execution-network-review'
    текстовыйВывод.mkdir(parents=True, exist_ok=True)
    Отчет_ЗНАЧЕН = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((задача_корень / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    источник_Файлы = {
        'привилегия_чек': '''public class привилегия_чек {
 public static void main(String[] аргументы) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'сеть_чек': '''import java.net.*;
public class сеть_чек {
 public static void main(String[] аргументы) throws Exception {
  Socket Подключить = new Socket("10.0.2.2", Integer.parseInt(аргументы[0]));
  Подключить.setSoTimeout(3000);
  byte[] текст = "TCP 한글\\n".getBytes("UTF-8");
  Подключить.getOutputStream().write(текст);
  for (int позиция_ИНДЕКС = 0; позиция_ИНДЕКС < текст.length; позиция_ИНДЕКС++)
   if (Подключить.getInputStream().read() != (текст[позиция_ИНДЕКС] & 255)) throw new RuntimeException("TCP mismatch");
  Подключить.close();
  DatagramSocket участник = new DatagramSocket(); участник.setSoTimeout(3000);
  текст = "UDP 한글".getBytes("UTF-8");
  участник.send(new DatagramPacket(текст, текст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(аргументы[1])));
  byte[] ответ = new byte[64]; DatagramPacket датаграмма = new DatagramPacket(ответ, ответ.length);
  участник.receive(датаграмма);
  if (датаграмма.getLength() != текст.length) throw new RuntimeException("UDP length");
  for (int позиция_ИНДЕКС = 0; позиция_ИНДЕКС < текст.length; позиция_ИНДЕКС++)
   if (ответ[позиция_ИНДЕКС] != текст[позиция_ИНДЕКС]) throw new RuntimeException("UDP mismatch");
  участник.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'получить_чек': '''import java.net.*;
public class получить_чек {
 public static void main(String[] аргументы) throws Exception {
  ServerSocket сервер_ЗНАЧЕН = new ServerSocket(9300); сервер_ЗНАЧЕН.setSoTimeout(5000);
  DatagramSocket участник = new DatagramSocket(9301); участник.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Подключить = сервер_ЗНАЧЕН.accept(); Подключить.setSoTimeout(5000);
  Подключить.getOutputStream().write(Подключить.getInputStream().read() + 1);
  Подключить.close(); сервер_ЗНАЧЕН.close();
  byte[] данные = new byte[64]; DatagramPacket датаграмма = new DatagramPacket(данные, данные.length);
  участник.receive(датаграмма); участник.send(датаграмма); участник.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Название, исходныйКод in источник_Файлы.items():
        (текстовыйВывод / (Название + '.java')).write_text(исходныйКод, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(текстовыйВывод)] +
                          [str(текстовыйВывод / (Название + '.java')) for Название in источник_Файлы])
    LOG_ЗАПИСЬ = bytearray()
    def пустой_номер_порта(ТИП_область=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ТИП_область) as ПОИСК_ЗНАЧЕН:
            ПОИСК_ЗНАЧЕН.bind(('127.0.0.4', 0))
            return ПОИСК_ЗНАЧЕН.getsockname()[1]
    파일접속번호, TCP_порт, UDP_порт = пустой_номер_порта(), пустой_номер_порта(), пустой_номер_порта(socket.SOCK_DGRAM)
    Процесс_ЗНАЧЕН = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, мост_3de4fe3a(
                파일접속번호, ['tcp:{}:9300'.format(TCP_порт), 'udp:{}:9301'.format(UDP_порт)],
                Сбор=True, адрес_узла='127.0.0.4') as мост_ЗНАЧЕН:
            управление_путь = Path(임시) / 'qmp.sock'
            Процесс_ЗНАЧЕН = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(управление_путь)] + мост_ЗНАЧЕН.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ВЫБОР_товар = selectors.DefaultSelector()
            ВЫБОР_товар.register(Процесс_ЗНАЧЕН.stdout, selectors.EVENT_READ)
            def получить(выпуск_ЗНАЧЕН=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while выпуск_ЗНАЧЕН not in LOG_ЗАПИСЬ[처음:]:
                    if time.monotonic() > 끝 or Процесс_ЗНАЧЕН.poll() is not None:
                        raise AssertionError('Missing ' + repr(выпуск_ЗНАЧЕН) + '\n' + LOG_ЗАПИСЬ[처음:].decode('utf-8', 'replace'))
                    for Ключ_ЗНАЧЕН, _ in ВЫБОР_товар.select(.05):
                        блок_ЗНАЧЕН_652d4b53 = Ключ_ЗНАЧЕН.fileobj.read(65536)
                        if блок_ЗНАЧЕН_652d4b53:
                            LOG_ЗАПИСЬ.extend(блок_ЗНАЧЕН_652d4b53)
                return LOG_ЗАПИСЬ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def написать(данные):
                Процесс_ЗНАЧЕН.stdin.write(данные)
                Процесс_ЗНАЧЕН.stdin.flush()
            def оболочка(текст):
                print(текст, flush=True)
                처음 = len(LOG_ЗАПИСЬ)
                написать((текст + '\n').encode())
                return получить(처음=처음)
            получить()
            with socket.socket(socket.AF_UNIX) as управление_ЗНАЧЕН:
                управление_ЗНАЧЕН.settimeout(10)
                управление_ЗНАЧЕН.connect(str(управление_путь))
                поток_ЗНАЧЕН = управление_ЗНАЧЕН.makefile('rwb')
                json.loads(поток_ЗНАЧЕН.readline())
                def запрос(명령어, аргументы=None):
                    данные = {'execute': 명령어}
                    if аргументы is not None:
                        данные['arguments'] = аргументы
                    поток_ЗНАЧЕН.write((json.dumps(данные) + '\n').encode())
                    поток_ЗНАЧЕН.flush()
                    while True:
                        ответ = json.loads(поток_ЗНАЧЕН.readline())
                        if 'error' in ответ:
                            raise AssertionError(ответ)
                        if 'return' in ответ:
                            return ответ['return']
                запрос('qmp_capabilities')
                def разрешение_на_чтение():
                    запрос('stop')
                    try:
                        return запрос('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        запрос('cont')
                Отчет_ЗНАЧЕН['shell_cpu'] = разрешение_на_чтение()
                assert 'EL1h' in Отчет_ЗНАЧЕН['shell_cpu'], Отчет_ЗНАЧЕН['shell_cpu']
                Отчет_ЗНАЧЕН['initial_ps'] = оболочка('ps')
                assert 'kernel/shell' in Отчет_ЗНАЧЕН['initial_ps']
                Отчет_ЗНАЧЕН['ipconfig'] = оболочка('ipconfig')
                assert 'inet 10.0.2.15' in Отчет_ЗНАЧЕН['ipconfig']
                Отчет_ЗНАЧЕН['gateway_ping'] = оболочка('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Отчет_ЗНАЧЕН['gateway_ping']
                assert 'FTP listening' in оболочка('ftpd start')
                with ftplib.FTP() as передать_ЗНАЧЕН_630ba093:
                    передать_ЗНАЧЕН_630ba093.encoding = 'utf-8'
                    передать_ЗНАЧЕН_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    передать_ЗНАЧЕН_630ba093.login()
                    for Название in источник_Файлы:
                        передать_ЗНАЧЕН_630ba093.storbinary('STOR ' + Название + '.class', io.BytesIO((текстовыйВывод / (Название + '.class')).read_bytes()))
                처음 = len(LOG_ЗАПИСЬ)
                написать('java привилегия_чек\n'.encode())
                получить(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Отчет_ЗНАЧЕН['java_cpu'] = разрешение_на_чтение()
                    if 'EL0t' in Отчет_ЗНАЧЕН['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Отчет_ЗНАЧЕН['java_cpu'], Отчет_ЗНАЧЕН['java_cpu']
                получить(처음=처음)
                Отчет_ЗНАЧЕН['after_exit_ps'] = оболочка('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Отчет_ЗНАЧЕН['after_exit_ps'])
                Отчет_ЗНАЧЕН['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with вывод_на_экран_средство() as одноранговый_ЗНАЧЕН:
                    текст = оболочка('java сеть_чек {} {}'.format(одноранговый_ЗНАЧЕН.TCP_порт, одноранговый_ЗНАЧЕН.UDP_порт))
                    assert 'OUTBOUND_TCP_UDP_PASS' in текст and 'exit 0' in текст, текст
                    assert одноранговый_ЗНАЧЕН.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, одноранговый_ЗНАЧЕН.수신됨
                    assert not одноранговый_ЗНАЧЕН.오류들, одноранговый_ЗНАЧЕН.오류들
                    Отчет_ЗНАЧЕН['outbound_peers'] = {Вид_ЗНАЧЕН: данные.decode() for Вид_ЗНАЧЕН, данные in одноранговый_ЗНАЧЕН.수신됨.items()}
                처음 = len(LOG_ЗАПИСЬ)
                написать('java получить_чек\n'.encode())
                получить(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_порт), timeout=5) as одноранговый_ЗНАЧЕН:
                    одноранговый_ЗНАЧЕН.sendall(b'A')
                    assert одноранговый_ЗНАЧЕН.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as одноранговый_ЗНАЧЕН:
                    одноранговый_ЗНАЧЕН.settimeout(5)
                    одноранговый_ЗНАЧЕН.sendto(b'UDP-IN', ('127.0.0.4', UDP_порт))
                    assert одноранговый_ЗНАЧЕН.recvfrom(64)[0] == b'UDP-IN'
                текст = получить(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in текст and 'exit 0' in текст, текст
                Отчет_ЗНАЧЕН['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in оболочка('terminal')
                оболочка('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_ЗАПИСЬ)
                написать('java ПримерОкна\n'.encode())
                получить('GUI 예제 Подготовить: ПримерОкна\r\n'.encode(), 처음)
                처음 = len(LOG_ЗАПИСЬ)
                написать(bytes([30, 2, 1, 0, 0, 0, 0]))
                получить(처음=처음)
                Отчет_ЗНАЧЕН['suspended_java_ps'] = оболочка('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ПримерОкна', Отчет_ЗНАЧЕН['suspended_java_ps']), Отчет_ЗНАЧЕН['suspended_java_ps']
                Отчет_ЗНАЧЕН['top'] = оболочка('top -n 1')
                assert 'java ПримерОкна' in Отчет_ЗНАЧЕН['top'] and 'kernel/shell' in Отчет_ЗНАЧЕН['top']
                Отчет_ЗНАЧЕН['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Отчет_ЗНАЧЕН['network_trace'] = мост_ЗНАЧЕН.журнал_трассировки
                assert not мост_ЗНАЧЕН.ошибка, мост_ЗНАЧЕН.ошибка
                написать(b'poweroff\n')
                assert Процесс_ЗНАЧЕН.wait(timeout=15) == 0
                Отчет_ЗНАЧЕН['passed'] = True
            ВЫБОР_товар.close()
    except Exception as ошибка:
        Отчет_ЗНАЧЕН['error'] = str(ошибка)
        raise
    finally:
        if Процесс_ЗНАЧЕН is not None and Процесс_ЗНАЧЕН.poll() is None:
            Процесс_ЗНАЧЕН.terminate()
            try:
                Процесс_ЗНАЧЕН.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Процесс_ЗНАЧЕН.kill()
                Процесс_ЗНАЧЕН.wait()
        (текстовыйВывод / 'serial.log').write_bytes(LOG_ЗАПИСЬ)
        (текстовыйВывод / 'report.json').write_text(json.dumps(Отчет_ЗНАЧЕН, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Ключ_ЗНАЧЕН: Отчет_ЗНАЧЕН[Ключ_ЗНАЧЕН] for Ключ_ЗНАЧЕН in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    запустить()
