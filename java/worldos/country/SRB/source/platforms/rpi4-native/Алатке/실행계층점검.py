#!/usr/bin/env python3
"""QEMU의 стваран_подаци CPU дозвола_вриједност, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Изврши_команда import пројектовати_корен, Наредба
from Мрежа_мост import Мрежа_мост
from 되돌림시험서버 import 되돌림시험서버


def Покрени():
    Излаз = пројектовати_корен / 'build/verification/execution-network-review'
    Излаз.mkdir(parents=True, exist_ok=True)
    извештај_вриједност = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((пројектовати_корен / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    извор_Фајлови = {
        'дозвола_чек': '''public class дозвола_чек {
 public static void main(String[] Аргументи) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Мрежа_чек': '''import java.net.*;
public class Мрежа_чек {
 public static void main(String[] Аргументи) throws Exception {
  Socket Повежи_се = new Socket("10.0.2.2", Integer.parseInt(Аргументи[0]));
  Повежи_се.setSoTimeout(3000);
  byte[] Текст = "TCP 한글\\n".getBytes("UTF-8");
  Повежи_се.getOutputStream().write(Текст);
  for (int позиција_индекс = 0; позиција_индекс < Текст.length; позиција_индекс++)
   if (Повежи_се.getInputStream().read() != (Текст[позиција_индекс] & 255)) throw new RuntimeException("TCP mismatch");
  Повежи_се.close();
  DatagramSocket крајња_тачка = new DatagramSocket(); крајња_тачка.setSoTimeout(3000);
  Текст = "UDP 한글".getBytes("UTF-8");
  крајња_тачка.send(new DatagramPacket(Текст, Текст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Аргументи[1])));
  byte[] одговор = new byte[64]; DatagramPacket 전문 = new DatagramPacket(одговор, одговор.length);
  крајња_тачка.receive(전문);
  if (전문.getLength() != Текст.length) throw new RuntimeException("UDP length");
  for (int позиција_индекс = 0; позиција_индекс < Текст.length; позиција_индекс++)
   if (одговор[позиција_индекс] != Текст[позиција_индекс]) throw new RuntimeException("UDP mismatch");
  крајња_тачка.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Аргументи) throws Exception {
  ServerSocket сервер_вриједност = new ServerSocket(9300); сервер_вриједност.setSoTimeout(5000);
  DatagramSocket крајња_тачка = new DatagramSocket(9301); крајња_тачка.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Повежи_се = сервер_вриједност.accept(); Повежи_се.setSoTimeout(5000);
  Повежи_се.getOutputStream().write(Повежи_се.getInputStream().read() + 1);
  Повежи_се.close(); сервер_вриједност.close();
  byte[] подаци = new byte[64]; DatagramPacket 전문 = new DatagramPacket(подаци, подаци.length);
  крајња_тачка.receive(전문); крајња_тачка.send(전문); крајња_тачка.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Назив, ИЗВОР in извор_Фајлови.items():
        (Излаз / (Назив + '.java')).write_text(ИЗВОР, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Излаз)] +
                          [str(Излаз / (Назив + '.java')) for Назив in извор_Фајлови])
    евиденција_ред = bytearray()
    def празно_број_порта(тип_област=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, тип_област) as тражити_вриједност:
            тражити_вриједност.bind(('127.0.0.4', 0))
            return тражити_вриједност.getsockname()[1]
    фајл_број_порта, 연결접속번호, 전문접속번호 = празно_број_порта(), празно_број_порта(), празно_број_порта(socket.SOCK_DGRAM)
    Процес_вриједност = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Мрежа_мост(
                фајл_број_порта, ['tcp:{}:9300'.format(연결접속번호), 'udp:{}:9301'.format(전문접속번호)],
                снимити=True, хост_адреса='127.0.0.4') as мост_вриједност:
            контрола_пут = Path(임시) / 'qmp.sock'
            Процес_вриједност = subprocess.Popen(Наредба() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(контрола_пут)] + мост_вриједност.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            изабрати_ставка = selectors.DefaultSelector()
            изабрати_ставка.register(Процес_вриједност.stdout, selectors.EVENT_READ)
            def 받기(емисија_вриједност=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while емисија_вриједност not in евиденција_ред[처음:]:
                    if time.monotonic() > 끝 or Процес_вриједност.poll() is not None:
                        raise AssertionError('Missing ' + repr(емисија_вриједност) + '\n' + евиденција_ред[처음:].decode('utf-8', 'replace'))
                    for Кључ_вриједност, _ in изабрати_ставка.select(.05):
                        조각 = Кључ_вриједност.fileobj.read(65536)
                        if 조각:
                            евиденција_ред.extend(조각)
                return евиденција_ред[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def послати(подаци):
                Процес_вриједност.stdin.write(подаци)
                Процес_вриједност.stdin.flush()
            def љуска(Текст):
                print(Текст, flush=True)
                처음 = len(евиденција_ред)
                послати((Текст + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as контрола_вриједност:
                контрола_вриједност.settimeout(10)
                контрола_вриједност.connect(str(контрола_пут))
                ток_вриједност = контрола_вриједност.makefile('rwb')
                json.loads(ток_вриједност.readline())
                def захтев(програмска_наредба_вриједност, Аргументи=None):
                    подаци = {'execute': програмска_наредба_вриједност}
                    if Аргументи is not None:
                        подаци['arguments'] = Аргументи
                    ток_вриједност.write((json.dumps(подаци) + '\n').encode())
                    ток_вриједност.flush()
                    while True:
                        одговор = json.loads(ток_вриједност.readline())
                        if 'error' in одговор:
                            raise AssertionError(одговор)
                        if 'return' in одговор:
                            return одговор['return']
                захтев('qmp_capabilities')
                def 권한읽기():
                    захтев('stop')
                    try:
                        return захтев('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        захтев('cont')
                извештај_вриједност['shell_cpu'] = 권한읽기()
                assert 'EL1h' in извештај_вриједност['shell_cpu'], извештај_вриједност['shell_cpu']
                извештај_вриједност['initial_ps'] = љуска('ps')
                assert 'kernel/shell' in извештај_вриједност['initial_ps']
                извештај_вриједност['ipconfig'] = љуска('ipconfig')
                assert 'inet 10.0.2.15' in извештај_вриједност['ipconfig']
                извештај_вриједност['gateway_ping'] = љуска('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in извештај_вриједност['gateway_ping']
                assert 'FTP listening' in љуска('ftpd start')
                with ftplib.FTP() as пренос_вриједност:
                    пренос_вриједност.encoding = 'utf-8'
                    пренос_вриједност.connect('127.0.0.4', фајл_број_порта, timeout=20)
                    пренос_вриједност.login()
                    for Назив in извор_Фајлови:
                        пренос_вриједност.storbinary('STOR ' + Назив + '.class', io.BytesIO((Излаз / (Назив + '.class')).read_bytes()))
                처음 = len(евиденција_ред)
                послати('java дозвола_чек\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    извештај_вриједност['java_cpu'] = 권한읽기()
                    if 'EL0t' in извештај_вриједност['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in извештај_вриједност['java_cpu'], извештај_вриједност['java_cpu']
                받기(처음=처음)
                извештај_вриједност['after_exit_ps'] = љуска('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', извештај_вриједност['after_exit_ps'])
                извештај_вриједност['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as 상대:
                    Текст = љуска('java Мрежа_чек {} {}'.format(상대.연결접속번호, 상대.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                    assert 상대.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, 상대.수신됨
                    assert not 상대.오류들, 상대.오류들
                    извештај_вриједност['outbound_peers'] = {종류: подаци.decode() for 종류, подаци in 상대.수신됨.items()}
                처음 = len(евиденција_ред)
                послати('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', 연결접속번호), timeout=5) as 상대:
                    상대.sendall(b'A')
                    assert 상대.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 상대:
                    상대.settimeout(5)
                    상대.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert 상대.recvfrom(64)[0] == b'UDP-IN'
                Текст = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                извештај_вриједност['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in љуска('terminal')
                љуска('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(евиденција_ред)
                послати('java 창예제\n'.encode())
                받기('GUI 예제 Припремити: 창예제\r\n'.encode(), 처음)
                처음 = len(евиденција_ред)
                послати(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                извештај_вриједност['suspended_java_ps'] = љуска('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', извештај_вриједност['suspended_java_ps']), извештај_вриједност['suspended_java_ps']
                извештај_вриједност['top'] = љуска('top -n 1')
                assert 'java 창예제' in извештај_вриједност['top'] and 'kernel/shell' in извештај_вриједност['top']
                извештај_вриједност['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                извештај_вриједност['network_trace'] = мост_вриједност.траг_евиденција
                assert not мост_вриједност.ГРЕШКА, мост_вриједност.ГРЕШКА
                послати(b'poweroff\n')
                assert Процес_вриједност.wait(timeout=15) == 0
                извештај_вриједност['passed'] = True
            изабрати_ставка.close()
    except Exception as ГРЕШКА:
        извештај_вриједност['error'] = str(ГРЕШКА)
        raise
    finally:
        if Процес_вриједност is not None and Процес_вриједност.poll() is None:
            Процес_вриједност.terminate()
            try:
                Процес_вриједност.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Процес_вриједност.kill()
                Процес_вриједност.wait()
        (Излаз / 'serial.log').write_bytes(евиденција_ред)
        (Излаз / 'report.json').write_text(json.dumps(извештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Кључ_вриједност: извештај_вриједност[Кључ_вриједност] for Кључ_вриједност in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Покрени()
