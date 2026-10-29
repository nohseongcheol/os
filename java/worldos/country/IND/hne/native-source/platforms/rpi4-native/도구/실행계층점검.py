#!/usr/bin/env python3
"""QEMU의 실제 CPU 권한, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from 실행 import 기준, 명령
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def 시작():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    보고 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    원문들 = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        '통신점검': '''import java.net.*;
public class 통신점검 {
 public static void main(String[] 인수) throws Exception {
  Socket 연결 = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  연결.setSoTimeout(3000);
  byte[] 글 = "TCP 한글\\n".getBytes("UTF-8");
  연결.getOutputStream().write(글);
  for (int 자리 = 0; 자리 < 글.length; 자리++)
   if (연결.getInputStream().read() != (글[자리] & 255)) throw new RuntimeException("TCP mismatch");
  연결.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  글 = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(글, 글.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] 응답 = new byte[64]; DatagramPacket 전문 = new DatagramPacket(응답, 응답.length);
  종단.receive(전문);
  if (전문.getLength() != 글.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < 글.length; 자리++)
   if (응답[자리] != 글[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); 서버.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket 연결 = 서버.accept(); 연결.setSoTimeout(5000);
  연결.getOutputStream().write(연결.getInputStream().read() + 1);
  연결.close(); 서버.close();
  byte[] 자료 = new byte[64]; DatagramPacket 전문 = new DatagramPacket(자료, 자료.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for 이름, 원문 in 원문들.items():
        (출력 / (이름 + '.java')).write_text(원문, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (이름 + '.java')) for 이름 in 원문들])
    기록 = bytearray()
    def 빈접속번호(유형=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 유형) as 탐색:
            탐색.bind(('127.0.0.4', 0))
            return 탐색.getsockname()[1]
    파일접속번호, 연결접속번호, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    과정 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(연결접속번호), 'udp:{}:9301'.format(전문접속번호)],
                포착여부=True, 호스트주소='127.0.0.4') as 다리:
            제어경로 = Path(임시) / 'qmp.sock'
            과정 = subprocess.Popen(명령() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(제어경로)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            고르기 = selectors.DefaultSelector()
            고르기.register(과정.stdout, selectors.EVENT_READ)
            def 받기(표시=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 표시 not in 기록[처음:]:
                    if time.monotonic() > 끝 or 과정.poll() is not None:
                        raise AssertionError('Missing ' + repr(표시) + '\n' + 기록[처음:].decode('utf-8', 'replace'))
                    for 키, _ in 고르기.select(.05):
                        조각 = 키.fileobj.read(65536)
                        if 조각:
                            기록.extend(조각)
                return 기록[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def 보내기(자료):
                과정.stdin.write(자료)
                과정.stdin.flush()
            def 셸(글):
                print(글, flush=True)
                처음 = len(기록)
                보내기((글 + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as 제어:
                제어.settimeout(10)
                제어.connect(str(제어경로))
                흐름 = 제어.makefile('rwb')
                json.loads(흐름.readline())
                def 요청(명령어, 인수=None):
                    자료 = {'execute': 명령어}
                    if 인수 is not None:
                        자료['arguments'] = 인수
                    흐름.write((json.dumps(자료) + '\n').encode())
                    흐름.flush()
                    while True:
                        응답 = json.loads(흐름.readline())
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
                보고['shell_cpu'] = 권한읽기()
                assert 'EL1h' in 보고['shell_cpu'], 보고['shell_cpu']
                보고['initial_ps'] = 셸('ps')
                assert 'kernel/shell' in 보고['initial_ps']
                보고['ipconfig'] = 셸('ipconfig')
                assert 'inet 10.0.2.15' in 보고['ipconfig']
                보고['gateway_ping'] = 셸('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in 보고['gateway_ping']
                assert 'FTP listening' in 셸('ftpd start')
                with ftplib.FTP() as 전송:
                    전송.encoding = 'utf-8'
                    전송.connect('127.0.0.4', 파일접속번호, timeout=20)
                    전송.login()
                    for 이름 in 원문들:
                        전송.storbinary('STOR ' + 이름 + '.class', io.BytesIO((출력 / (이름 + '.class')).read_bytes()))
                처음 = len(기록)
                보내기('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    보고['java_cpu'] = 권한읽기()
                    if 'EL0t' in 보고['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in 보고['java_cpu'], 보고['java_cpu']
                받기(처음=처음)
                보고['after_exit_ps'] = 셸('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', 보고['after_exit_ps'])
                보고['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as 상대:
                    글 = 셸('java 통신점검 {} {}'.format(상대.연결접속번호, 상대.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in 글 and 'exit 0' in 글, 글
                    assert 상대.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, 상대.수신됨
                    assert not 상대.오류들, 상대.오류들
                    보고['outbound_peers'] = {종류: 자료.decode() for 종류, 자료 in 상대.수신됨.items()}
                처음 = len(기록)
                보내기('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', 연결접속번호), timeout=5) as 상대:
                    상대.sendall(b'A')
                    assert 상대.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 상대:
                    상대.settimeout(5)
                    상대.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert 상대.recvfrom(64)[0] == b'UDP-IN'
                글 = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in 글 and 'exit 0' in 글, 글
                보고['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in 셸('terminal')
                셸('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(기록)
                보내기('java 창예제\n'.encode())
                받기('GUI 예제 준비: 창예제\r\n'.encode(), 처음)
                처음 = len(기록)
                보내기(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                보고['suspended_java_ps'] = 셸('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', 보고['suspended_java_ps']), 보고['suspended_java_ps']
                보고['top'] = 셸('top -n 1')
                assert 'java 창예제' in 보고['top'] and 'kernel/shell' in 보고['top']
                보고['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                보고['network_trace'] = 다리.추적기록
                assert not 다리.गलती, 다리.गलती
                보내기(b'poweroff\n')
                assert 과정.wait(timeout=15) == 0
                보고['passed'] = True
            고르기.close()
    except Exception as गलती:
        보고['error'] = str(गलती)
        raise
    finally:
        if 과정 is not None and 과정.poll() is None:
            과정.terminate()
            try:
                과정.wait(timeout=10)
            except subprocess.TimeoutExpired:
                과정.kill()
                과정.wait()
        (출력 / 'serial.log').write_bytes(기록)
        (출력 / 'report.json').write_text(json.dumps(보고, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({키: 보고[키] for 키 in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    시작()
