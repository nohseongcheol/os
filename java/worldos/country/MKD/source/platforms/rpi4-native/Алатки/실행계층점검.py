#!/usr/bin/env python3
"""QEMU의 реален_податоци CPU дозвола_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Изврши_наредба import Project_корен, Команда
from Мрежа_мост import Мрежа_мост
from 되돌림시험서버 import 되돌림시험서버


def Изврши_2():
    출력 = Project_корен / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    извештај_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_корен / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    извор_Датотеки = {
        'дозвола_провери': '''public class дозвола_провери {
 public static void main(String[] Аргументи) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Мрежа_провери': '''import java.net.*;
public class Мрежа_провери {
 public static void main(String[] Аргументи) throws Exception {
  Socket Врзи_се = new Socket("10.0.2.2", Integer.parseInt(Аргументи[0]));
  Врзи_се.setSoTimeout(3000);
  byte[] Текст = "TCP 한글\\n".getBytes("UTF-8");
  Врзи_се.getOutputStream().write(Текст);
  for (int позиционирање_INDEX = 0; позиционирање_INDEX < Текст.length; позиционирање_INDEX++)
   if (Врзи_се.getInputStream().read() != (Текст[позиционирање_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Врзи_се.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Текст = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Текст, Текст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Аргументи[1])));
  byte[] одговори = new byte[64]; DatagramPacket 전문 = new DatagramPacket(одговори, одговори.length);
  종단.receive(전문);
  if (전문.getLength() != Текст.length) throw new RuntimeException("UDP length");
  for (int позиционирање_INDEX = 0; позиционирање_INDEX < Текст.length; позиционирање_INDEX++)
   if (одговори[позиционирање_INDEX] != Текст[позиционирање_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Аргументи) throws Exception {
  ServerSocket сервер_VALUE = new ServerSocket(9300); сервер_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Врзи_се = сервер_VALUE.accept(); Врзи_се.setSoTimeout(5000);
  Врзи_се.getOutputStream().write(Врзи_се.getInputStream().read() + 1);
  Врзи_се.close(); сервер_VALUE.close();
  byte[] податоци = new byte[64]; DatagramPacket 전문 = new DatagramPacket(податоци, податоци.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Име, ИЗВОР in извор_Датотеки.items():
        (출력 / (Име + '.java')).write_text(ИЗВОР, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Име + '.java')) for Име in извор_Датотеки])
    LOG_ред = bytearray()
    def празно_број_на_порта(TYPE_област=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_област) as SEARCH_VALUE:
            SEARCH_VALUE.bind(('127.0.0.4', 0))
            return SEARCH_VALUE.getsockname()[1]
    датотека_број_на_порта, ТЦП_порта, УДП_порта = празно_број_на_порта(), празно_број_на_порта(), празно_број_на_порта(socket.SOCK_DGRAM)
    Процес_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Мрежа_мост(
                датотека_број_на_порта, ['tcp:{}:9300'.format(ТЦП_порта), 'udp:{}:9301'.format(УДП_порта)],
                зафати=True, вдоми_адреса='127.0.0.4') as мост_VALUE:
            контрола_патека = Path(임시) / 'qmp.sock'
            Процес_VALUE = subprocess.Popen(Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(контрола_патека)] + мост_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_ставка = selectors.DefaultSelector()
            CHOOSE_ставка.register(Процес_VALUE.stdout, selectors.EVENT_READ)
            def 받기(прикажи_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while прикажи_VALUE not in LOG_ред[처음:]:
                    if time.monotonic() > 끝 or Процес_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(прикажи_VALUE) + '\n' + LOG_ред[처음:].decode('utf-8', 'replace'))
                    for Клуч_VALUE, _ in CHOOSE_ставка.select(.05):
                        조각 = Клуч_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_ред.extend(조각)
                return LOG_ред[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def испрати(податоци):
                Процес_VALUE.stdin.write(податоци)
                Процес_VALUE.stdin.flush()
            def обвивка(Текст):
                print(Текст, flush=True)
                처음 = len(LOG_ред)
                испрати((Текст + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as контрола_VALUE:
                контрола_VALUE.settimeout(10)
                контрола_VALUE.connect(str(контрола_патека))
                Stream_VALUE = контрола_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def Барање_на_HTTP(инструкција_VALUE, Аргументи=None):
                    податоци = {'execute': инструкција_VALUE}
                    if Аргументи is not None:
                        податоци['arguments'] = Аргументи
                    Stream_VALUE.write((json.dumps(податоци) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        одговори = json.loads(Stream_VALUE.readline())
                        if 'error' in одговори:
                            raise AssertionError(одговори)
                        if 'return' in одговори:
                            return одговори['return']
                Барање_на_HTTP('qmp_capabilities')
                def 권한읽기():
                    Барање_на_HTTP('stop')
                    try:
                        return Барање_на_HTTP('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        Барање_на_HTTP('cont')
                извештај_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in извештај_VALUE['shell_cpu'], извештај_VALUE['shell_cpu']
                извештај_VALUE['initial_ps'] = обвивка('ps')
                assert 'kernel/shell' in извештај_VALUE['initial_ps']
                извештај_VALUE['ipconfig'] = обвивка('ipconfig')
                assert 'inet 10.0.2.15' in извештај_VALUE['ipconfig']
                извештај_VALUE['gateway_ping'] = обвивка('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in извештај_VALUE['gateway_ping']
                assert 'FTP listening' in обвивка('ftpd start')
                with ftplib.FTP() as пренос_VALUE:
                    пренос_VALUE.encoding = 'utf-8'
                    пренос_VALUE.connect('127.0.0.4', датотека_број_на_порта, timeout=20)
                    пренос_VALUE.login()
                    for Име in извор_Датотеки:
                        пренос_VALUE.storbinary('STOR ' + Име + '.class', io.BytesIO((출력 / (Име + '.class')).read_bytes()))
                처음 = len(LOG_ред)
                испрати('java дозвола_провери\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    извештај_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in извештај_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in извештај_VALUE['java_cpu'], извештај_VALUE['java_cpu']
                받기(처음=처음)
                извештај_VALUE['after_exit_ps'] = обвивка('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', извештај_VALUE['after_exit_ps'])
                извештај_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as рамноправен_уред_VALUE:
                    Текст = обвивка('java Мрежа_провери {} {}'.format(рамноправен_уред_VALUE.ТЦП_порта, рамноправен_уред_VALUE.УДП_порта))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                    assert рамноправен_уред_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, рамноправен_уред_VALUE.수신됨
                    assert not рамноправен_уред_VALUE.오류들, рамноправен_уред_VALUE.오류들
                    извештај_VALUE['outbound_peers'] = {종류: податоци.decode() for 종류, податоци in рамноправен_уред_VALUE.수신됨.items()}
                처음 = len(LOG_ред)
                испрати('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ТЦП_порта), timeout=5) as рамноправен_уред_VALUE:
                    рамноправен_уред_VALUE.sendall(b'A')
                    assert рамноправен_уред_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as рамноправен_уред_VALUE:
                    рамноправен_уред_VALUE.settimeout(5)
                    рамноправен_уред_VALUE.sendto(b'UDP-IN', ('127.0.0.4', УДП_порта))
                    assert рамноправен_уред_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Текст = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Текст and 'exit 0' in Текст, Текст
                извештај_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in обвивка('terminal')
                обвивка('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_ред)
                испрати('java 창예제\n'.encode())
                받기('GUI 예제 Подготви: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_ред)
                испрати(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                извештај_VALUE['suspended_java_ps'] = обвивка('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', извештај_VALUE['suspended_java_ps']), извештај_VALUE['suspended_java_ps']
                извештај_VALUE['top'] = обвивка('top -n 1')
                assert 'java 창예제' in извештај_VALUE['top'] and 'kernel/shell' in извештај_VALUE['top']
                извештај_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                извештај_VALUE['network_trace'] = мост_VALUE.трага_LOG
                assert not мост_VALUE.ГРЕШКА, мост_VALUE.ГРЕШКА
                испрати(b'poweroff\n')
                assert Процес_VALUE.wait(timeout=15) == 0
                извештај_VALUE['passed'] = True
            CHOOSE_ставка.close()
    except Exception as ГРЕШКА:
        извештај_VALUE['error'] = str(ГРЕШКА)
        raise
    finally:
        if Процес_VALUE is not None and Процес_VALUE.poll() is None:
            Процес_VALUE.terminate()
            try:
                Процес_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Процес_VALUE.kill()
                Процес_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_ред)
        (출력 / 'report.json').write_text(json.dumps(извештај_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Клуч_VALUE: извештај_VALUE[Клуч_VALUE] for Клуч_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Изврши_2()
