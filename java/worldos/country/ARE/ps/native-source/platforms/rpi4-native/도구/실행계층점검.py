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

from 실행 import 기준, بولۍ
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def ځغلول():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    راپور_ارزښت = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    원문들 = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'جال_کتل': '''import java.net.*;
public class جال_کتل {
 public static void main(String[] 인수) throws Exception {
  Socket نښلېدل = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  نښلېدل.setSoTimeout(3000);
  byte[] ليکنه = "TCP 한글\\n".getBytes("UTF-8");
  نښلېدل.getOutputStream().write(ليکنه);
  for (int 자리 = 0; 자리 < ليکنه.length; 자리++)
   if (نښلېدل.getInputStream().read() != (ليکنه[자리] & 255)) throw new RuntimeException("TCP mismatch");
  نښلېدل.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ليکنه = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ليکنه, ليکنه.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] 응답 = new byte[64]; DatagramPacket 전문 = new DatagramPacket(응답, 응답.length);
  종단.receive(전문);
  if (전문.getLength() != ليکنه.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < ليکنه.length; 자리++)
   if (응답[자리] != ليکنه[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); 서버.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket نښلېدل = 서버.accept(); نښلېدل.setSoTimeout(5000);
  نښلېدل.getOutputStream().write(نښلېدل.getInputStream().read() + 1);
  نښلېدل.close(); 서버.close();
  byte[] اومتوک = new byte[64]; DatagramPacket 전문 = new DatagramPacket(اومتوک, اومتوک.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for نوم, سرچينه in 원문들.items():
        (출력 / (نوم + '.java')).write_text(سرچينه, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (نوم + '.java')) for نوم in 원문들])
    خبرال_کیل = bytearray()
    def 빈접속번호(유형=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 유형) as پلټل_ارزښت:
            پلټل_ارزښت.bind(('127.0.0.4', 0))
            return پلټل_ارزښت.getsockname()[1]
    파일접속번호, لېږد_مهارې_باندره_درشل, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    과정 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(لېږد_مهارې_باندره_درشل), 'udp:{}:9301'.format(전문접속번호)],
                포착여부=True, کوربه_پته='127.0.0.4') as 다리:
            مهار_يونلور = Path(임시) / 'qmp.sock'
            과정 = subprocess.Popen(بولۍ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(مهار_يونلور)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            چڼل_توک = selectors.DefaultSelector()
            چڼل_توک.register(과정.stdout, selectors.EVENT_READ)
            def 받기(표시=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 표시 not in خبرال_کیل[처음:]:
                    if time.monotonic() > 끝 or 과정.poll() is not None:
                        raise AssertionError('Missing ' + repr(표시) + '\n' + خبرال_کیل[처음:].decode('utf-8', 'replace'))
                    for کيلي_ارزښت, _ in چڼل_توک.select(.05):
                        조각 = کيلي_ارزښت.fileobj.read(65536)
                        if 조각:
                            خبرال_کیل.extend(조각)
                return خبرال_کیل[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def استول(اومتوک):
                과정.stdin.write(اومتوک)
                과정.stdin.flush()
            def سیپۍ(ليکنه):
                print(ليکنه, flush=True)
                처음 = len(خبرال_کیل)
                استول((ليکنه + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as مهار_ارزښت:
                مهار_ارزښت.settimeout(10)
                مهار_ارزښت.connect(str(مهار_يونلور))
                بهنګ_ارزښت = مهار_ارزښت.makefile('rwb')
                json.loads(بهنګ_ارزښت.readline())
                def 요청(چارښودنه_ارزښت, 인수=None):
                    اومتوک = {'execute': چارښودنه_ارزښت}
                    if 인수 is not None:
                        اومتوک['arguments'] = 인수
                    بهنګ_ارزښت.write((json.dumps(اومتوک) + '\n').encode())
                    بهنګ_ارزښت.flush()
                    while True:
                        응답 = json.loads(بهنګ_ارزښت.readline())
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
                راپور_ارزښت['shell_cpu'] = 권한읽기()
                assert 'EL1h' in راپور_ارزښت['shell_cpu'], راپور_ارزښت['shell_cpu']
                راپور_ارزښت['initial_ps'] = سیپۍ('ps')
                assert 'kernel/shell' in راپور_ارزښت['initial_ps']
                راپور_ارزښت['ipconfig'] = سیپۍ('ipconfig')
                assert 'inet 10.0.2.15' in راپور_ارزښت['ipconfig']
                راپور_ارزښت['gateway_ping'] = سیپۍ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in راپور_ارزښت['gateway_ping']
                assert 'FTP listening' in سیپۍ('ftpd start')
                with ftplib.FTP() as لېږدول_ارزښت:
                    لېږدول_ارزښت.encoding = 'utf-8'
                    لېږدول_ارزښت.connect('127.0.0.4', 파일접속번호, timeout=20)
                    لېږدول_ارزښت.login()
                    for نوم in 원문들:
                        لېږدول_ارزښت.storbinary('STOR ' + نوم + '.class', io.BytesIO((출력 / (نوم + '.class')).read_bytes()))
                처음 = len(خبرال_کیل)
                استول('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    راپور_ارزښت['java_cpu'] = 권한읽기()
                    if 'EL0t' in راپور_ارزښت['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in راپور_ارزښت['java_cpu'], راپور_ارزښت['java_cpu']
                받기(처음=처음)
                راپور_ارزښت['after_exit_ps'] = سیپۍ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', راپور_ارزښت['after_exit_ps'])
                راپور_ارزښت['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as جوړه_ارزښت:
                    ليکنه = سیپۍ('java جال_کتل {} {}'.format(جوړه_ارزښت.لېږد_مهارې_باندره_درشل, جوړه_ارزښت.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ليکنه and 'exit 0' in ليکنه, ليکنه
                    assert جوړه_ارزښت.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, جوړه_ارزښت.수신됨
                    assert not جوړه_ارزښت.오류들, جوړه_ارزښت.오류들
                    راپور_ارزښت['outbound_peers'] = {종류: اومتوک.decode() for 종류, اومتوک in جوړه_ارزښت.수신됨.items()}
                처음 = len(خبرال_کیل)
                استول('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', لېږد_مهارې_باندره_درشل), timeout=5) as جوړه_ارزښت:
                    جوړه_ارزښت.sendall(b'A')
                    assert جوړه_ارزښت.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as جوړه_ارزښت:
                    جوړه_ارزښت.settimeout(5)
                    جوړه_ارزښت.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert جوړه_ارزښت.recvfrom(64)[0] == b'UDP-IN'
                ليکنه = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ليکنه and 'exit 0' in ليکنه, ليکنه
                راپور_ارزښت['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in سیپۍ('terminal')
                سیپۍ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(خبرال_کیل)
                استول('java 창예제\n'.encode())
                받기('GUI 예제 준비: 창예제\r\n'.encode(), 처음)
                처음 = len(خبرال_کیل)
                استول(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                راپور_ارزښت['suspended_java_ps'] = سیپۍ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', راپور_ارزښت['suspended_java_ps']), راپور_ارزښت['suspended_java_ps']
                راپور_ارزښت['top'] = سیپۍ('top -n 1')
                assert 'java 창예제' in راپور_ارزښت['top'] and 'kernel/shell' in راپور_ارزښت['top']
                راپور_ارزښت['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                راپور_ارزښت['network_trace'] = 다리.추적기록
                assert not 다리.تېروتنه, 다리.تېروتنه
                استول(b'poweroff\n')
                assert 과정.wait(timeout=15) == 0
                راپور_ارزښت['passed'] = True
            چڼل_توک.close()
    except Exception as تېروتنه:
        راپور_ارزښت['error'] = str(تېروتنه)
        raise
    finally:
        if 과정 is not None and 과정.poll() is None:
            과정.terminate()
            try:
                과정.wait(timeout=10)
            except subprocess.TimeoutExpired:
                과정.kill()
                과정.wait()
        (출력 / 'serial.log').write_bytes(خبرال_کیل)
        (출력 / 'report.json').write_text(json.dumps(راپور_ارزښت, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({کيلي_ارزښت: راپور_ارزښت[کيلي_ارزښت] for کيلي_ارزښت in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ځغلول()
