#!/usr/bin/env python3
"""QEMU의 фактычны_дадзеныя CPU дазвол_значэнне, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from выканаць_каманда import 기준, Загад
from Сетка_мост import Сетка_мост
from 되돌림시험서버 import 되돌림시험서버


def Выканаць():
    Выхад = 기준 / 'build/verification/execution-network-review'
    Выхад.mkdir(parents=True, exist_ok=True)
    справаздача_значэнне = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    крыніца_Файлы = {
        'дазвол_чэк': '''public class дазвол_чэк {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Сетка_чэк': '''import java.net.*;
public class Сетка_чэк {
 public static void main(String[] 인수) throws Exception {
  Socket Злучыцца = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Злучыцца.setSoTimeout(3000);
  byte[] Тэкст = "TCP 한글\\n".getBytes("UTF-8");
  Злучыцца.getOutputStream().write(Тэкст);
  for (int 자리 = 0; 자리 < Тэкст.length; 자리++)
   if (Злучыцца.getInputStream().read() != (Тэкст[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Злучыцца.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Тэкст = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Тэкст, Тэкст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] адказаць = new byte[64]; DatagramPacket 전문 = new DatagramPacket(адказаць, адказаць.length);
  종단.receive(전문);
  if (전문.getLength() != Тэкст.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Тэкст.length; 자리++)
   if (адказаць[자리] != Тэкст[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket сервер_значэнне = new ServerSocket(9300); сервер_значэнне.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Злучыцца = сервер_значэнне.accept(); Злучыцца.setSoTimeout(5000);
  Злучыцца.getOutputStream().write(Злучыцца.getInputStream().read() + 1);
  Злучыцца.close(); сервер_значэнне.close();
  byte[] дадзеныя = new byte[64]; DatagramPacket 전문 = new DatagramPacket(дадзеныя, дадзеныя.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Назва, КРЫНІЦА in крыніца_Файлы.items():
        (Выхад / (Назва + '.java')).write_text(КРЫНІЦА, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Выхад)] +
                          [str(Выхад / (Назва + '.java')) for Назва in крыніца_Файлы])
    журнал_запіс = bytearray()
    def нулявая_нумар_порта(друкаваць_катэгорыя=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, друкаваць_катэгорыя) as Пошук_значэнне:
            Пошук_значэнне.bind(('127.0.0.4', 0))
            return Пошук_значэнне.getsockname()[1]
    файл_нумар_порта, пратакол_кіравання_перадачай_TCP_порт, 전문접속번호 = нулявая_нумар_порта(), нулявая_нумар_порта(), нулявая_нумар_порта(socket.SOCK_DGRAM)
    Працэс_значэнне = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Сетка_мост(
                файл_нумар_порта, ['tcp:{}:9300'.format(пратакол_кіравання_перадачай_TCP_порт), 'udp:{}:9301'.format(전문접속번호)],
                зняць=True, вузел_адрас='127.0.0.4') as мост_значэнне:
            кіраванне_шлях = Path(임시) / 'qmp.sock'
            Працэс_значэнне = subprocess.Popen(Загад() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(кіраванне_шлях)] + мост_значэнне.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            выбіраць_элемент = selectors.DefaultSelector()
            выбіраць_элемент.register(Працэс_значэнне.stdout, selectors.EVENT_READ)
            def 받기(паказаць_значэнне=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while паказаць_значэнне not in журнал_запіс[처음:]:
                    if time.monotonic() > 끝 or Працэс_значэнне.poll() is not None:
                        raise AssertionError('Missing ' + repr(паказаць_значэнне) + '\n' + журнал_запіс[처음:].decode('utf-8', 'replace'))
                    for клавіша_значэнне, _ in выбіраць_элемент.select(.05):
                        조각 = клавіша_значэнне.fileobj.read(65536)
                        if 조각:
                            журнал_запіс.extend(조각)
                return журнал_запіс[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def адправіць(дадзеныя):
                Працэс_значэнне.stdin.write(дадзеныя)
                Працэс_значэнне.stdin.flush()
            def абалонка(Тэкст):
                print(Тэкст, flush=True)
                처음 = len(журнал_запіс)
                адправіць((Тэкст + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as кіраванне_значэнне:
                кіраванне_значэнне.settimeout(10)
                кіраванне_значэнне.connect(str(кіраванне_шлях))
                паток_значэнне = кіраванне_значэнне.makefile('rwb')
                json.loads(паток_значэнне.readline())
                def 요청(інструкцыя_значэнне, 인수=None):
                    дадзеныя = {'execute': інструкцыя_значэнне}
                    if 인수 is not None:
                        дадзеныя['arguments'] = 인수
                    паток_значэнне.write((json.dumps(дадзеныя) + '\n').encode())
                    паток_значэнне.flush()
                    while True:
                        адказаць = json.loads(паток_значэнне.readline())
                        if 'error' in адказаць:
                            raise AssertionError(адказаць)
                        if 'return' in адказаць:
                            return адказаць['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                справаздача_значэнне['shell_cpu'] = 권한읽기()
                assert 'EL1h' in справаздача_значэнне['shell_cpu'], справаздача_значэнне['shell_cpu']
                справаздача_значэнне['initial_ps'] = абалонка('ps')
                assert 'kernel/shell' in справаздача_значэнне['initial_ps']
                справаздача_значэнне['ipconfig'] = абалонка('ipconfig')
                assert 'inet 10.0.2.15' in справаздача_значэнне['ipconfig']
                справаздача_значэнне['gateway_ping'] = абалонка('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in справаздача_значэнне['gateway_ping']
                assert 'FTP listening' in абалонка('ftpd start')
                with ftplib.FTP() as перанос_значэнне:
                    перанос_значэнне.encoding = 'utf-8'
                    перанос_значэнне.connect('127.0.0.4', файл_нумар_порта, timeout=20)
                    перанос_значэнне.login()
                    for Назва in крыніца_Файлы:
                        перанос_значэнне.storbinary('STOR ' + Назва + '.class', io.BytesIO((Выхад / (Назва + '.class')).read_bytes()))
                처음 = len(журнал_запіс)
                адправіць('java дазвол_чэк\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    справаздача_значэнне['java_cpu'] = 권한읽기()
                    if 'EL0t' in справаздача_значэнне['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in справаздача_значэнне['java_cpu'], справаздача_значэнне['java_cpu']
                받기(처음=처음)
                справаздача_значэнне['after_exit_ps'] = абалонка('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', справаздача_значэнне['after_exit_ps'])
                справаздача_значэнне['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as аднарангавы_значэнне:
                    Тэкст = абалонка('java Сетка_чэк {} {}'.format(аднарангавы_значэнне.пратакол_кіравання_перадачай_TCP_порт, аднарангавы_значэнне.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Тэкст and 'exit 0' in Тэкст, Тэкст
                    assert аднарангавы_значэнне.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, аднарангавы_значэнне.수신됨
                    assert not аднарангавы_значэнне.오류들, аднарангавы_значэнне.오류들
                    справаздача_значэнне['outbound_peers'] = {종류: дадзеныя.decode() for 종류, дадзеныя in аднарангавы_значэнне.수신됨.items()}
                처음 = len(журнал_запіс)
                адправіць('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', пратакол_кіравання_перадачай_TCP_порт), timeout=5) as аднарангавы_значэнне:
                    аднарангавы_значэнне.sendall(b'A')
                    assert аднарангавы_значэнне.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as аднарангавы_значэнне:
                    аднарангавы_значэнне.settimeout(5)
                    аднарангавы_значэнне.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert аднарангавы_значэнне.recvfrom(64)[0] == b'UDP-IN'
                Тэкст = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Тэкст and 'exit 0' in Тэкст, Тэкст
                справаздача_значэнне['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in абалонка('terminal')
                абалонка('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(журнал_запіс)
                адправіць('java 창예제\n'.encode())
                받기('GUI 예제 Падрыхтаваць: 창예제\r\n'.encode(), 처음)
                처음 = len(журнал_запіс)
                адправіць(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                справаздача_значэнне['suspended_java_ps'] = абалонка('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', справаздача_значэнне['suspended_java_ps']), справаздача_значэнне['suspended_java_ps']
                справаздача_значэнне['top'] = абалонка('top -n 1')
                assert 'java 창예제' in справаздача_значэнне['top'] and 'kernel/shell' in справаздача_значэнне['top']
                справаздача_значэнне['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                справаздача_значэнне['network_trace'] = мост_значэнне.след_журнал
                assert not мост_значэнне.ПАМЫЛКА, мост_значэнне.ПАМЫЛКА
                адправіць(b'poweroff\n')
                assert Працэс_значэнне.wait(timeout=15) == 0
                справаздача_значэнне['passed'] = True
            выбіраць_элемент.close()
    except Exception as ПАМЫЛКА:
        справаздача_значэнне['error'] = str(ПАМЫЛКА)
        raise
    finally:
        if Працэс_значэнне is not None and Працэс_значэнне.poll() is None:
            Працэс_значэнне.terminate()
            try:
                Працэс_значэнне.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Працэс_значэнне.kill()
                Працэс_значэнне.wait()
        (Выхад / 'serial.log').write_bytes(журнал_запіс)
        (Выхад / 'report.json').write_text(json.dumps(справаздача_значэнне, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({клавіша_значэнне: справаздача_значэнне[клавіша_значэнне] for клавіша_значэнне in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Выканаць()
