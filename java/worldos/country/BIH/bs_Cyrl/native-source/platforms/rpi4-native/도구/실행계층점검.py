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

from 실행 import 기준, команда
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def 시작():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    извјештај_вриједност = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    원문들 = {
        'дозвола_чек': '''public class дозвола_чек {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Мрежа_чек': '''import java.net.*;
public class Мрежа_чек {
 public static void main(String[] 인수) throws Exception {
  Socket повезати = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  повезати.setSoTimeout(3000);
  byte[] текст = "TCP 한글\\n".getBytes("UTF-8");
  повезати.getOutputStream().write(текст);
  for (int 자리 = 0; 자리 < текст.length; 자리++)
   if (повезати.getInputStream().read() != (текст[자리] & 255)) throw new RuntimeException("TCP mismatch");
  повезати.close();
  DatagramSocket крајња_тачка = new DatagramSocket(); крајња_тачка.setSoTimeout(3000);
  текст = "UDP 한글".getBytes("UTF-8");
  крајња_тачка.send(new DatagramPacket(текст, текст.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] 응답 = new byte[64]; DatagramPacket 전문 = new DatagramPacket(응답, 응답.length);
  крајња_тачка.receive(전문);
  if (전문.getLength() != текст.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < текст.length; 자리++)
   if (응답[자리] != текст[자리]) throw new RuntimeException("UDP mismatch");
  крајња_тачка.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket сервер_вриједност = new ServerSocket(9300); сервер_вриједност.setSoTimeout(5000);
  DatagramSocket крајња_тачка = new DatagramSocket(9301); крајња_тачка.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket повезати = сервер_вриједност.accept(); повезати.setSoTimeout(5000);
  повезати.getOutputStream().write(повезати.getInputStream().read() + 1);
  повезати.close(); сервер_вриједност.close();
  byte[] подаци = new byte[64]; DatagramPacket 전문 = new DatagramPacket(подаци, подаци.length);
  крајња_тачка.receive(전문); крајња_тачка.send(전문); крајња_тачка.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for назив, извор in 원문들.items():
        (출력 / (назив + '.java')).write_text(извор, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (назив + '.java')) for назив in 원문들])
    дневник_рада_ред = bytearray()
    def 빈접속번호(куцати_категорија=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, куцати_категорија) as тражити_вриједност:
            тражити_вриједност.bind(('127.0.0.4', 0))
            return тражити_вриједност.getsockname()[1]
    파일접속번호, TCP_порт, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    процес_вриједност = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_порт), 'udp:{}:9301'.format(전문접속번호)],
                포착여부=True, хост_рачунар_адреса='127.0.0.4') as 다리:
            контрола_пут = Path(임시) / 'qmp.sock'
            процес_вриједност = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(контрола_пут)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            изабрати_ставка = selectors.DefaultSelector()
            изабрати_ставка.register(процес_вриједност.stdout, selectors.EVENT_READ)
            def 받기(приказати_вриједност=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while приказати_вриједност not in дневник_рада_ред[처음:]:
                    if time.monotonic() > 끝 or процес_вриједност.poll() is not None:
                        raise AssertionError('Missing ' + repr(приказати_вриједност) + '\n' + дневник_рада_ред[처음:].decode('utf-8', 'replace'))
                    for кључ_вриједност, _ in изабрати_ставка.select(.05):
                        조각 = кључ_вриједност.fileobj.read(65536)
                        if 조각:
                            дневник_рада_ред.extend(조각)
                return дневник_рада_ред[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def послати(подаци):
                процес_вриједност.stdin.write(подаци)
                процес_вриједност.stdin.flush()
            def љуска(текст):
                print(текст, flush=True)
                처음 = len(дневник_рада_ред)
                послати((текст + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as контрола_вриједност:
                контрола_вриједност.settimeout(10)
                контрола_вриједност.connect(str(контрола_пут))
                ток_вриједност = контрола_вриједност.makefile('rwb')
                json.loads(ток_вриједност.readline())
                def 요청(програмска_наредба_вриједност, 인수=None):
                    подаци = {'execute': програмска_наредба_вриједност}
                    if 인수 is not None:
                        подаци['arguments'] = 인수
                    ток_вриједност.write((json.dumps(подаци) + '\n').encode())
                    ток_вриједност.flush()
                    while True:
                        응답 = json.loads(ток_вриједност.readline())
                        if 'error' in 응답:
                            raise AssertionError(응답)
                        if 'return' in 응답:
                            return 응답['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                извјештај_вриједност['shell_cpu'] = 권한읽기()
                assert 'EL1h' in извјештај_вриједност['shell_cpu'], извјештај_вриједност['shell_cpu']
                извјештај_вриједност['initial_ps'] = љуска('ps')
                assert 'kernel/shell' in извјештај_вриједност['initial_ps']
                извјештај_вриједност['ipconfig'] = љуска('ipconfig')
                assert 'inet 10.0.2.15' in извјештај_вриједност['ipconfig']
                извјештај_вриједност['gateway_ping'] = љуска('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in извјештај_вриједност['gateway_ping']
                assert 'FTP listening' in љуска('ftpd start')
                with ftplib.FTP() as пријенос_вриједност:
                    пријенос_вриједност.encoding = 'utf-8'
                    пријенос_вриједност.connect('127.0.0.4', 파일접속번호, timeout=20)
                    пријенос_вриједност.login()
                    for назив in 원문들:
                        пријенос_вриједност.storbinary('STOR ' + назив + '.class', io.BytesIO((출력 / (назив + '.class')).read_bytes()))
                처음 = len(дневник_рада_ред)
                послати('java дозвола_чек\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    извјештај_вриједност['java_cpu'] = 권한읽기()
                    if 'EL0t' in извјештај_вриједност['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in извјештај_вриједност['java_cpu'], извјештај_вриједност['java_cpu']
                받기(처음=처음)
                извјештај_вриједност['after_exit_ps'] = љуска('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', извјештај_вриједност['after_exit_ps'])
                извјештај_вриједност['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as peer_вриједност:
                    текст = љуска('java Мрежа_чек {} {}'.format(peer_вриједност.TCP_порт, peer_вриједност.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in текст and 'exit 0' in текст, текст
                    assert peer_вриједност.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_вриједност.수신됨
                    assert not peer_вриједност.오류들, peer_вриједност.오류들
                    извјештај_вриједност['outbound_peers'] = {종류: подаци.decode() for 종류, подаци in peer_вриједност.수신됨.items()}
                처음 = len(дневник_рада_ред)
                послати('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_порт), timeout=5) as peer_вриједност:
                    peer_вриједност.sendall(b'A')
                    assert peer_вриједност.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_вриједност:
                    peer_вриједност.settimeout(5)
                    peer_вриједност.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert peer_вриједност.recvfrom(64)[0] == b'UDP-IN'
                текст = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in текст and 'exit 0' in текст, текст
                извјештај_вриједност['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in љуска('terminal')
                љуска('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(дневник_рада_ред)
                послати('java 창예제\n'.encode())
                받기('GUI 예제 Припремити: 창예제\r\n'.encode(), 처음)
                처음 = len(дневник_рада_ред)
                послати(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                извјештај_вриједност['suspended_java_ps'] = љуска('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', извјештај_вриједност['suspended_java_ps']), извјештај_вриједност['suspended_java_ps']
                извјештај_вриједност['top'] = љуска('top -n 1')
                assert 'java 창예제' in извјештај_вриједност['top'] and 'kernel/shell' in извјештај_вриједност['top']
                извјештај_вриједност['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                извјештај_вриједност['network_trace'] = 다리.추적기록
                assert not 다리.грешка, 다리.грешка
                послати(b'poweroff\n')
                assert процес_вриједност.wait(timeout=15) == 0
                извјештај_вриједност['passed'] = True
            изабрати_ставка.close()
    except Exception as грешка:
        извјештај_вриједност['error'] = str(грешка)
        raise
    finally:
        if процес_вриједност is not None and процес_вриједност.poll() is None:
            процес_вриједност.terminate()
            try:
                процес_вриједност.wait(timeout=10)
            except subprocess.TimeoutExpired:
                процес_вриједност.kill()
                процес_вриједност.wait()
        (출력 / 'serial.log').write_bytes(дневник_рада_ред)
        (출력 / 'report.json').write_text(json.dumps(извјештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({кључ_вриједност: извјештај_вриједност[кључ_вриједност] for кључ_вриједност in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    시작()
